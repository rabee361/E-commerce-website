from django.urls import path
from .views import *

urlpatterns = [
    path('categories/' , Categories.as_view() , name="categories"),
    path('v1/sign-up/' , SignUp.as_view() , name="sign-up"),
    path('v2/sign-up/' , SignUp2.as_view() , name="sign-up2"),
    path('user/' , UserName.as_view()),
    path('logout/' , Logout.as_view()),
    path('login/' , Login.as_view()),
    path('info/' , Info.as_view()),
    path('product/<str:pk>' , ProductDetail2.as_view()),
    path('related-products/<str:pk>' , RelatedProducts.as_view())

]