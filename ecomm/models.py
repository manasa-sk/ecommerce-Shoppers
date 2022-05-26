from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    user_id = models.AutoField(auto_created=True, primary_key=True, unique=True, serialize=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_num = models.PositiveBigIntegerField(null=False, default=0)
    address = models.TextField(null=False, default="-")
    last_login = models.DateTimeField(auto_now=True)
    cart_num = models.PositiveSmallIntegerField(null=False, default=0)
    log_status = models.PositiveSmallIntegerField(null=False, default=0)
    # password is default

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)


    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email'] # username & password are required by default.

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin



class UserEmail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, primary_key=True)

class Product(models.Model):
    product_id= models.IntegerField(primary_key=True, auto_created=True, serialize=True)
    product_name = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=100)

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

class Category(models.Model):
    cat_id = models.AutoField(auto_created=True, serialize=True, primary_key=True)
    cat_name = models.CharField(max_length=50)

class ProdCat(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('cat_id', 'product_id'),)