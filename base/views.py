from django.shortcuts import render , redirect
from .forms import *
from .models import *
from django.db.models import F , Q ,Avg , Sum ,Max , Min ,ExpressionWrapper , FloatField
from django.contrib.auth import authenticate , login , logout
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required
from datetime import timedelta , datetime


def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('index')

    return render(request , 'base/authentication-login.html' , {})




def auth_register(request):
    form = NewUser()
    if request.method == 'POST':
        form = NewUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
    context = {
        'form' : form
    }
    return render(request, 'base/authentication-register.html', context)




@login_required(login_url='auth-login')
def index(request):
    reviews = Review.objects.select_related('name').\
                            only('name__username','text','profession','rating').\
                            all()[:3]
    
    products = Product.objects.only('name','price','images').\
                                prefetch_related('images').\
                                annotate(stars = Avg(F('review__rating'))).\
                                all()[:8]
    context = {
        'products' : products,
        'reviews' : reviews,
    }
    return render(request,'base/index.html' , context)




@login_required(login_url='auth-login')
def contact(request):
    return render(request,'base/contact.html' , {})

@login_required(login_url='auth-login')
def checkout(request):
    return render(request, 'base/checkout.html' , {})


@login_required(login_url='auth-login')
def wishlist(request):
    return render(request, 'base/wishlist.html' , {})


# def product_list(request):
#     context = {
#         'sizes' : sizes
#     }
#     return render(request, 'base/product-list.html' , {})


# class product_list(ListView):###### use only() and function based views instead
#     model = Product
#     template_name = 'base/product-list.html'
#     paginate_by = 3
#     context_object_name = 'products'

def product_list(request , page):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(name__contains = q)
    )
    paginator = Paginator(products, 3)
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products' : products,
    }
    return render(request,'base/product-list.html' , context)



@login_required(login_url='auth-login')
def account(request):
    return render(request, 'base/my-account.html' , {})


@login_required(login_url='auth-login')
def product_detail(request , pk):
    product = Product.objects.get(id=pk)
    rating = product.review_set.only('rating').aggregate(avg_rating=Avg('rating'))['avg_rating']

    related_products = Product.objects.only('name','price','images')\
                                        .prefetch_related('images')\
                                        .filter(product_type=product.product_type)
    new_price = 0.00
    if product.discount != 0.00:
        new_price = product.price * product.discount

    context = {
        'product' : product,
        'new_price' : new_price,
        'related_products' : related_products,
        'rating' : rating
    }
    return render(request, 'base/product-detail.html' , context)


@login_required(login_url='auth-login')
def cart(request):
    # coupon = 0.0
    shipping = 20.0
    # if request.method == 'POST':
    #     coupon = request.POST['coupon']
    cart_items = Cart_Products.objects.select_related('products')\
                                    .only('products__name','products__price','quantity','cart__customer')\
                                    .select_related('cart__customer')\
                                    .prefetch_related('products__images')\
                                    .filter(cart__customer=request.user).annotate(
                                        total = ExpressionWrapper(
                                        F('products__price')*F('quantity'), output_field=FloatField()
                                        ))
    sub_total = cart_items.aggregate(sub_total = Sum('total'))['sub_total']
    grand_total =  sub_total + shipping 

    context = {
        'cart_items' : cart_items,
        'sub_total' : sub_total,
        'grand_total' : grand_total
    }
    return render(request, 'base/cart.html' , context)


@login_required(login_url='auth-login')
def cart_item_number(request):
    user = request.user
    cart_items = Cart.objects.get(customer=user).items
    context = {
        'cart_items' : cart_items
    }
    return render(request , 'base/navbar.html' , context)


def logoutUser(request):
    logout(request)
    return redirect('auth-login')


def RemoveItem(request , pk):
    item = Cart_Products.objects.get(id=pk)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def quantity_handler(request,pk,pk2):
    item = Cart_Products.objects.get(id=pk)
    if pk2 == 'add':
        item.add_item
    else:
        item.sub_item

    return redirect(request.META.get('HTTP_REFERER'))


def wish_handler(request,pk,pk2):
    item = Wish_products.objects.get(id=pk)
    if pk2 == 'add':
        item.add_item
    else:
        item.sub_item

    return redirect(request.META.get('HTTP_REFERER'))




def wishlist(request):
    wishlist = Wish_products.objects.select_related('products')\
                                    .only('products__name','products__price','quantity')\
                                    .prefetch_related('products__images')\
                                    .filter(wish_list__customer=request.user)
    context = {
        'wishlist' : wishlist
    }
    return render(request, 'base/wishlist.html' , context)