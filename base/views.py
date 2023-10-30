from django.shortcuts import render , redirect
from .forms import *
from .models import *
from django.db.models import F , Q ,Avg , Sum ,Max , Min ,ExpressionWrapper , FloatField
from django.contrib.auth import authenticate , login , logout
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required


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
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Product_Category.objects.all()
    reviews = Review.objects.select_related('name').\
                            only('name__username','text','rating').\
                            all()[:3]
    
    products = Product.objects.only('name','price','images').\
                                prefetch_related('images').\
                                annotate(stars = Avg(F('review__rating'))).\
                                filter(Q(name__contains = q) | Q(product_type__category__contains = q))[:8]
    context = {
        'products' : products,
        'reviews' : reviews,
        'categories' : categories
    }
    return render(request,'base/index.html' , context)




@login_required(login_url='auth-login')
def contact(request):
    return render(request,'base/contact.html' , {})

@login_required(login_url='auth-login')
def checkout(request):
    form = BillingForm(instance=request.user) 
    sub_total = 0.00
    shipping = 20.00
    cart_items = Cart_Products.objects.select_related('products','cart__customer')\
                                    .only('products__name','products__price','quantity','cart__customer')\
                                    .prefetch_related('products__images')\
                                    .filter(cart__customer=request.user).annotate(
                                        total = ExpressionWrapper(
                                        F('products__price')*F('quantity'), output_field=FloatField()
                                        ))
    if cart_items.aggregate(sub_total = Sum('total'))['sub_total'] : 
        sub_total = cart_items.aggregate(sub_total = Sum('total'))['sub_total'] 

    grand_total =  sub_total + shipping 
    if request.method=='POST':
        form = BillingForm(request.POST, instance=request.user)
        if form.is_valid():
            cart = Cart.objects.get(customer=request.user)
            products = cart.items.all()
            order = Order.objects.create(customer=request.user, payment=form.cleaned_data['payment'])
            order.products.set(products)
            order.total = grand_total
            order.save()
            form.save()
            cart.delete()

            return redirect('account')
        
    context = {
        'cart_items' : cart_items,
        'sub_total' : sub_total,
        'grand_total' : grand_total,
        'form' : form
    }
    return render(request, 'base/checkout.html' , context)


@login_required(login_url='auth-login')
def wishlist(request):
    return render(request, 'base/wishlist.html' , {})


def product_list(request , page):
    categories = Product_Category.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(Q(name__contains = q) | Q(product_type__category__contains = q)).annotate(stars = Avg(F('review__rating')))
    paginator = Paginator(products, 2)
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products' : products,
        'categories' : categories
    }
    return render(request,'base/product-list.html' , context)



@login_required(login_url='auth-login')
def account(request):
    orders = Order.objects.filter(customer=request.user)
    context = {
        'orders' : orders
    }
    return render(request, 'base/my-account.html' , context)


@login_required(login_url='auth-login')
def product_detail(request , pk):
    form = ReviewForm()
    product = Product.objects.get(id=pk)
    reviews = Review.objects.filter(product=product)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            review = form.save(commit=False)
            review.name = request.user
            review.product = product
            print(review)
            review.save()
            return redirect(request.path_info)

    related_products = Product.objects.only('name','price','images').prefetch_related('images')\
                                                                .filter(product_type=product.product_type)\
                                                            .annotate(stars = Avg(F('review__rating')))
    context = {
    'product' : product,
    'related_products' : related_products,
    'form' : form,
    'reviews' : reviews
    }
    try:
        quantity = Cart_Products.objects.select_related('cart').get(products=product,cart__customer=request.user)
        context['quantity'] = quantity

    except(Product.DoesNotExist ,Cart_Products.DoesNotExist):
        pass

    return render(request, 'base/product-detail.html' , context)


@login_required(login_url='auth-login')
def cart(request):
    sub_total = 0.0
    shipping = 20.0
    cart_items = Cart_Products.objects.select_related('products')\
                                    .only('products__name','products__price','quantity','cart__customer')\
                                    .select_related('cart__customer')\
                                    .prefetch_related('products__images')\
                                    .filter(cart__customer=request.user).annotate(
                                        total = ExpressionWrapper(
                                        F('products__price')*F('quantity'), output_field=FloatField()
                                        ))
    if cart_items.aggregate(sub_total = Sum('total'))['sub_total'] : 
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


def Remove_Wish(request , pk):
    item = Wish_products.objects.get(id=pk)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def buy_now(request,pk):
    item = Product.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_products, created = Cart_Products.objects.get_or_create(products=item, cart=cart)
    if not created:
        Cart_Products.objects.filter(products=item, cart=cart).\
                                update(quantity=F('quantity') + 1)
    return redirect('cart')




def quantity_handler(request,pk,pk2):
    item = Cart_Products.objects.get(id=pk)
    if pk2 == 'add':
        item.add_item
    else:
        if item.quantity == 1:
            item.sub_item
            item.delete()

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


def add_to_cart(request,pk):
    item = Product.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_products, created = Cart_Products.objects.get_or_create(products=item, cart=cart)
    if not created:
        Cart_Products.objects.filter(products=item, cart=cart).\
                                update(quantity=F('quantity') + 1)
    return redirect(request.META.get('HTTP_REFERER'))


def add_to_wishes(request,pk):
    item = Product.objects.get(id=pk)
    wish_list, created = WhishList.objects.get_or_create(customer=request.user)
    wish_products, created = Wish_products.objects.get_or_create(products=item, wish_list=wish_list)
    if not created:
        Wish_products.objects.filter(products=item, wish_list=wish_list).\
                                update(quantity=F('quantity') + 1)

    return redirect(request.META.get('HTTP_REFERER'))

