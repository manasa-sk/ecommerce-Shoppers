from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(auto_created=True, primary_key=True, unique=True, serialize=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_num = models.PositiveBigIntegerField(null=False, default=0)
    address = models.TextField(null=False, default="-")
    password = models.CharField(editable=False, max_length=20)
    cart_num = models.PositiveSmallIntegerField(null=False, default=0)
    log_status = models.PositiveSmallIntegerField(null=False, default=0)

class UserEmail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, primary_key=True)

class Product(models.Model):
    product_id= models.IntegerField(primary_key=True, auto_created=True, serialize=True)
    product_name = models.CharField(max_length=30)
    price = models.PositiveIntegerField()

class ProdImage(models.Model):
    id = models.OneToOneField('Product', on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='images/')

class Cart(models.Model):
    user_id = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=False, default=1)

    class Meta:
        unique_together = (('user_id', 'product_id'),)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True, auto_created=True, serialize=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_placed = models.DateTimeField(auto_now_add=True)

class OrderProd(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=False, default=1)

    class Meta:
        unique_together = (('order_id', 'product_id'),)
