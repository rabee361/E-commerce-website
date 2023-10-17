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


def product_detail(request , pk):
    product = Product.objects.get(id=pk)
    product_type = product.product_type
    related_products = Product.objects.filter(product_type=product_type)
    print(product.name)
    new_price = 0.00
    if product.discount != 0.00:
        new_price = product.price * product.discount

    context = {
        'product' : product,
        'new_price' : new_price,
        'related_products' : related_products
    }
    return render(request, 'base/product-detail.html' , context)


def cart(request):
    return render(request, 'base/cart.html' , {})