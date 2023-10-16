from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index , name="index"),
    path('contact/',  contact , name="contact"),
    path('checkout/' , checkout , name="checkout"),
    path('account/' , account , name="account"),
    path('product-detail/' , product_detail , name="product-detail"),
    path('product-list/' , product_list , name="product-list"),
    path('wishlist/' , wishlist , name="wishlist"),
    path('cart/' , cart , name="cart"),
    path('login/' , login , name="login")



]