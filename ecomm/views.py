from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from numpy import product
from .models import *


# Create your views here.
class Page:    
    def home(request):
        try:
            if getActiveUser():
                return render(request, 'index.html', {'cart_num': getCartNum()})
        except User.DoesNotExist:
            msg = 'Login to access the store.'
            return render(request, 'login.html', {'msg': msg})

    def shop(request):
        prod = Product.objects.all()
        img = ProdImage.objects.all()
        products = []
        for i in range(len(prod)):
            products.append([prod[i], img[i]])
        return render(request, 'shop.html', {'cart_num': getCartNum(), 'products': products})

    def contact(request):
        return render(request, 'contact.html', {'cart_num': getCartNum()})

    def about(request):
        return render(request, 'about.html', {'cart_num': getCartNum()})
        
    def product_dis(request):
        if request.method == 'GET':
            pid = request.GET.get('pid')
            product = Product.objects.get(product_id=pid)
            prodimg = ProdImage.objects.get(id=product)
        return render(request, 'product.html', {'cart_num': getCartNum(), 'product': product, 'prodimg': prodimg})
    
    def loginPage(request):
        try:
            if getActiveUser():
                userP = getActiveUser()
                userP.log_status = 0
                userP.save()
        except:
            pass
        return render(request, 'login.html', {'msg': ''})
    
    def registerPage(request):
        return render(request, 'register.html', {'msg': ''})

    def thankyou(request):
        if place_order():
            return render(request, 'thankyou.html', {'cart_num': getCartNum()})
        else:
            return HttpResponseRedirect('/cart/')
    
    def showOrder(request):
        if request.method=='GET':
            oid = int(request.GET.get('oid'))
            order = Order.objects.get(order_id=oid)
            orderProd = OrderProd.objects.filter(order_id=order)
            total = 0
            orderDet = []
            for prod in orderProd:
                orderDet.append([prod.product_id, prod.quantity])
                total+= orderDet[-1][0].price * orderDet[-1][1]
            return render(request, 'order.html', {'orderDet': orderDet, 'oid': oid, 'total': total, 'cart_num': getCartNum()})

    def account(request):
        user = getActiveUser()
        userEm = UserEmail.objects.get(user_id=user)
        orders = Order.objects.filter(user_id=user)
        return render(request, 'account.html', {'user': user, 'userEm': userEm, 'cart_num': getCartNum(), 'orders': orders})
    
    def checkout(request):
        cart, total, num = getCart()
        return render(request, 'checkout.html', {'cart_num': getCartNum(), 'cart': cart, 'total': total, 'num': num})
    
def getActiveUser():
    user = User.objects.get(log_status=1)
    return user

def getProduct(pid):
    product = Product.objects.get(product_id=pid)
    return product

def getCartNum():
    try:
        user = getActiveUser()
        return user.cart_num
    except User.DoesNotExist:
        return 0

def search(request):
    if request.method=='GET':
        searchKey = request.GET.get('search')
        prod = Product.objects.filter(product_name__icontains=searchKey)
        products=[]
        for i in range(len(prod)):
            img = ProdImage.objects.get(id=prod[i])
            products.append([prod[i], img])
        return render(request, 'shop.html', {'cart_num': getCartNum(), 'products': products})


def loginUser(request):
    if request.method=='POST':
        form = request.POST
        email, pwd = form.get('c_uname'), form.get('pass')
        try:
            if getActiveUser():
                userP = getActiveUser()
                userP.log_status = 0
                userP.save()
        except:
            pass
        try:
            user_em = UserEmail.objects.get(email=email)
            if user_em.user_id.password == pwd:
                user_em.user_id.log_status = 1
                user_em.user_id.save()
                return HttpResponseRedirect('/home/')
            else:
                msg = "Invalid Password"
                return render(request, 'login.html', {'msg': msg})
        except UserEmail.DoesNotExist:
            msg = "User Does Not Exist, Try Registering"
            return render(request, 'login.html', {'msg': msg})

def place_order():
    cart, total, num = getCart()
    for item in cart:
        product = getProduct(item[0].product_id)
        quantity = item[1].quantity
        if product.stock >= quantity:
            user = getActiveUser()
            order = Order(user_id=user)
            order.save()

            orderP = OrderProd(order_id=order, product_id=product, quantity=quantity)
            orderP.save()
            product.stock-=quantity
            product.save()
    
            Cart.objects.get(user_id=user, product_id=product).delete()
            user.cart_num = 0
            user.save()
    return True

def registerUser(request):
    if request.method=='POST':
        form = request.POST
        try:
            temp_user = UserEmail.objects.get(email=form.get('email'))
            temp_user.user_id

            msg = "User already registered, Log in"
            return render(request, 'register.html', {'msg': msg, 'cart_num': getCartNum()})
        except UserEmail.DoesNotExist:
            user = User(first_name=form.get('c_diff_fname'), last_name=form.get('c_diff_lname'), phone_num=form.get('phone'), password=form.get('pass'))
            user_em = UserEmail(email=form.get('email'))
            try:
                if getActiveUser():
                    userP = getActiveUser()
                    userP.log_status = 0
                    userP.save()
            except:
                pass
            user.log_status = 1
            user.save()
            user_em.user_id = user
            user_em.save()
            return HttpResponseRedirect('/home/')

def addToCart(request):
    if request.method=='GET':
        quantity = int(request.GET.get('quantity'))

        product = getProduct(pid=int(request.GET.get('pid')))
        user = getActiveUser()

        if quantity<=product.stock:
            msg = ''
            try:
                cart = Cart.objects.get(user_id=user, product_id=product)
                cart.quantity+=quantity
                cart.save()
            except:
                cart = Cart(user_id=user, product_id=product, quantity=quantity)
                cart.save()

            user.cart_num+=quantity
            user.save()
        else:
            msg = 'Please enter quantity within stock limit.'

        pid = request.GET.get('pid')
        product = Product.objects.get(product_id=pid)
        prodimg = ProdImage.objects.get(id=product)
        return render(request, 'product.html', {'cart_num': getCartNum(), 'product': product, 'prodimg': prodimg, 'msg': msg})

def cart(request):
    cart, total, num = getCart()
    return render(request, 'cart.html', {'cart_num': getCartNum(), 'cart': cart, 'total': total})

def getCart():
    cartItems = Cart.objects.filter(user_id=getActiveUser())
    cart = []
    total = 0
    num = 0
    for item in cartItems:
        cart.append([item.product_id, item, item.product_id.price*item.quantity])
        total+=cart[-1][2]
        num+=item.quantity
    return cart, total, num

def filter(request):
    if request.method=='GET':
        filter = request.GET.get('filter')
        if filter == 'women':
            prod = Product.objects.filter(product_name__icontains=filter)
        elif filter == 'men':
            prod = Product.objects.filter(product_name__icontains=' men')
        products = []
        for i in range(len(prod)):
            img = ProdImage.objects.get(id=prod[i])
            products.append([prod[i], img])
        return render(request, 'shop.html', {'cart_num': getCartNum(), 'products': products})

def removeItem(request):
    if request.method=='GET':
        pid = int(request.GET.get('pid'))
        user = getActiveUser()
        item = Cart.objects.get(user_id=user, product_id=getProduct(pid))

        user.cart_num-=item.quantity
        user.save()
        item.delete()

        return HttpResponseRedirect('/cart/')

def logout(request):
    try:
        user = getActiveUser()
        user.log_status = 0
        user.save()
    except:
        pass
    return render(request, 'login.html', {'msg': ''})