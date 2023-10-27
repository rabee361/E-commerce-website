from .models import *
from django.db.models import Sum

def navbar(request):
    user_cart = None
    user_wishlist = None
    cart_items_num = None
    wishlist_items_num = None
    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(customer=request.user).first()
        user_wishlist = WhishList.objects.filter(customer=request.user).first()

        cart_items_num = user_cart.items.aggregate(Sum('cart_products__quantity'))['cart_products__quantity__sum'] or 0
        wishlist_items_num = user_wishlist.items.aggregate(Sum('wish_products__quantity'))['wish_products__quantity__sum'] or 0
        
    return {'cart_items_num': cart_items_num , 'wishlist_items_num' : wishlist_items_num}

