from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from django.db.models import F
from django.db.models import ExpressionWrapper , FloatField



def index(request):
    user = request.user
    cart_items = Cart.objects.get(customer=user).items.count()
    products = Product.objects.only('name','price','images').\
                                prefetch_related('images').\
                                    all()[:8]
    recent_products = Product.objects.only('name','price','images').\
                                        prefetch_related('images').\
                                            all()[:8]
    context = {
        'products' : products,
        'recent_products' : recent_products,
        'cart_items' : cart_items
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


# def product_list(request):
#     context = {
#         'sizes' : sizes
#     }
#     return render(request, 'base/product-list.html' , {})


class product_list(ListView):###### use only() and function based views instead
    model = Product
    template_name = 'base/product-list.html'
    paginate_by = 3
    context_object_name = 'products'

def account(request):
    return render(request, 'base/my-account.html' , {})


def product_detail(request , pk):
    product = Product.objects.get(id=pk)
    related_products = Product.objects.only('name','price','images')\
                                        .prefetch_related('images')\
                                            .filter(product_type=product.product_type)
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
    cart_items = Cart_Products.objects.select_related('products')\
                                        .only('products__name','products__price','quantity')\
                                            .prefetch_related('products__images').all()
    context = {
        'cart_items' : cart_items
    }
    return render(request, 'base/cart.html' , context)


def cart_item_number(request):
    user = request.user
    cart_items = Cart.objects.get(customer=user).items
    context = {
        'cart_items' : cart_items
    }
    return render(request , 'base/navbar.html' , context)