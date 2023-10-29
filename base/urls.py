from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index , name="index"),
    path('contact/',  contact , name="contact"),
    path('checkout/' , checkout , name="checkout"),
    path('account/' , account , name="account"),
    path('product-detail/<str:pk>' , product_detail , name="product-detail"),
    path('product-list/<int:page>' , product_list , name="product-list"),
    path('wishlist/' , wishlist , name="wishlist"),
    path('cart/' , cart , name="cart"),
    # path('login/' , login , name="login"),
    path('cart_items' , cart_item_number , name="cart_item"),
    path('auth-login/' , auth_login , name="auth-login"),
    path('auth-register/' , auth_register , name="auth-register"),
    path('logout/' , logoutUser , name="logout"),
    path('remove-item/<str:pk>' , RemoveItem , name="remove-item"),
    path('quantity_handler/<str:pk>/<str:pk2>' , quantity_handler , name="quantity_handler"),
    path('wish-handler/<str:pk>/<str:pk2>' , wish_handler , name="wish_handler"),
    path('add-to-cart/<str:pk>' , add_to_cart, name="add-to-cart"),
    path('add-to-wishes/<str:pk>' , add_to_wishes, name="add-to-wishes"),
    path('remove-wish/<str:pk>' , Remove_Wish , name="remove-wish"),
    path('buy-now/<str:pk>', buy_now , name="buy-now")





]