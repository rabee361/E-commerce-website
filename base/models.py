from django.db import models
from django.contrib.auth.models import AbstractUser



class Address(models.Model):
    city = models.CharField(max_length=40)
    neighborhood = models.CharField(max_length=40)
    detail = models.CharField(max_length=80)
    building_num = models.IntegerField()

    def __str__(self):
        return f'{self.city},{self.neighborhood},{self.detail[0:20]}...'


class MyUser(AbstractUser):
    address = models.ForeignKey(Address, on_delete=models.CASCADE , null=True)






class Review(models.Model):
    name = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField()
    text = models.TextField(max_length=150)
    product = models.ForeignKey('Product' , on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} : {self.text[0:20]}...'



class Size(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name




class Color(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
    


class Product_Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category




class Image(models.Model):
    image = models.ImageField(upload_to='static/img/')

    def __str__(self):
        return self.image.url



class Product(models.Model):

    name = models.CharField(max_length=50 , db_index=True)
    decription = models.TextField(max_length=200 , null=True)
    time_added = models.DateTimeField(auto_now_add=True , db_index=True)
    price = models.FloatField()
    images = models.ManyToManyField(Image)
    product_type = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    discount = models.FloatField(default=0.00)
    colors = models.ManyToManyField('Color')
    sizes = models.ManyToManyField('Size')

    class Meta:
        ordering = ['-time_added']

    def __str__(self):
        return self.name



class Cart(models.Model):
    customer = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    items = models.ManyToManyField(Product ,through='Cart_Products')


    def __str__(self):
        return f'{self.customer} cart'



class Cart_Products(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.cart.customer.username



class Order(models.Model):
    customer = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    shipping_cost = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)
    # order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer
    


class WhishList(models.Model):
    customer = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)