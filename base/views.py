from django.shortcuts import render
from .models import *

def index(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request,'base/index.html' , context)


def contact(request):
    return render(request,'base/contact.html' , {})


def checkout(request):
    return render(request, 'base/checkout.html' , {})


def wishlist(request):
    return render(request, 'base/wishlist.html' , {})


def login(request):
    return render(request, 'base/login.html' , {})


def product_list(request):
    return render(request, 'base/product-list.html' , {})


def account(request):
    return render(request, 'base/my-account.html' , {})


def product_detail(request):
    return render(request, 'base/product-detail.html' , {})


def cart(request):
    return render(request, 'base/cart.html' , {})