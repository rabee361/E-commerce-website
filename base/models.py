from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wish_list = models.ManyToManyField('Product')
    cart = models.ForeignKey('Cart',related_name='user',on_delete=models.RESTRICT , blank=True)



class Review(models.Model):
    name = models.CharField(max_length=30)
    time = models.DateField()
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


class Product(models.Model):
    CHOICES = (
        ('Fashion & Beauty','Fashion & Beauty'),
        ('Kids & Babies Cloths','Kids & Babies Cloths'),
        ('Men & Women Cloths','Men & Women Cloths'),
        ('Gadget & Accessories','Gadget & Accessories'),
        ('Electronics','Electronics')
    )
    name = models.CharField(max_length=50)
    decription = models.TextField(max_length=200 , null=True)
    time_added = models.DateTimeField()
    rating = models.PositiveIntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to='static/img/')
    product_type = models.CharField(choices=CHOICES , max_length=40)
    discount = models.FloatField(default=0.00)
    colors = models.ManyToManyField('Color')
    sizes = models.ManyToManyField('Size')

    def __str__(self):
        return self.name




class Cart(models.Model):
    customer = models.ForeignKey(Customer, related_name='+' , on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='Cart_Products')
    # total = models.FloatField()

    def __str__(self):
        return self.user.username



class Cart_Products(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)





