from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from phone_field import PhoneField
from datetime import datetime


class MyUser(AbstractUser):
    address = models.CharField(max_length=150,default=' ')
    mobile = PhoneField(blank=True, help_text='Contact phone number')
    country = models.CharField(max_length=30,default=' ')
    city = models.CharField(max_length=30,default=' ')
    state = models.CharField(max_length=30,default=' ')
    image = models.ImageField(upload_to='static/img/users')


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    # created = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField()
    text = models.TextField(max_length=150)
    product = models.ForeignKey('product' , on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name.username} : {self.text[0:20]}...'



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

    @property
    def get_items_num(self):
        return self.items.count()

    def __str__(self):
        return f'{self.customer} cart'



class Cart_Products(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['products__time_added']

    # @property
    # def total(self):
    #     return float(self.quantity * self.products.price)
    
    @property
    def add_item(self):
        self.quantity = self.quantity + 1
        self.save()

    @property
    def sub_item(self):
        self.quantity = self.quantity - 1
        self.save()

    def __str__(self):
        return self.cart.customer.username



class Order(models.Model):
    customer = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total = models.FloatField(default=0.00)
    order_time = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=50, default='Cash')

    def __str__(self):
        return f'{self.customer} order'
    


class WhishList(models.Model):
    customer = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    items = models.ManyToManyField(Product , through='Wish_products')

    @property
    def items_num(self):
        return self.items.count()

    def __str__(self):
        return f'{self.customer} wishlist'



class Wish_products(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    wish_list = models.ForeignKey(WhishList, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['products__time_added']

    @property
    def add_item(self):
        self.quantity = self.quantity + 1
        self.save()

    @property
    def sub_item(self):
        self.quantity = self.quantity - 1
        self.save()

    def __str__(self):
        return self.products.name
