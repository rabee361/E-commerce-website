from .models import Cart , WhishList

def navbar(request):
    user_cart = 0
    user_wishlist = 0
    if request.user:
        user_cart = Cart.objects.get(customer=request.user)
        user_wishlist = WhishList.objects.get(customer=request.user)
    return {'user_cart': user_cart , 'user_wishlist' : user_wishlist}


