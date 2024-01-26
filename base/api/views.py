from rest_framework.response import Response
from .serializers import *
from base.models import Cart
from rest_framework.views import APIView
from django.db.models import F , Q ,Avg , Sum ,Max , Min ,ExpressionWrapper , FloatField , Count
from rest_framework.generics import CreateAPIView , ListAPIView , RetrieveAPIView
from django.contrib.auth import authenticate , login , logout
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.shortcuts import redirect


### for testing #####
class UserName(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.is_authenticated:
            username = request.user.username
            return Response(username)
        return Response('hello')


class Login(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        return Response('hello , you can login here')
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username , password=password)
        if user:
            login(request,user)
            return redirect('user')
        

class SignUp(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        context = {'request':request}
        serializer = UserSerializer(data=request.data , context=context)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUp2(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    

class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        logout(request)
        return Response('done')


##### handle one product with reviews as read_only #####
class ProductDetail(APIView):
    def get(self,request,pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product , many=False)
        return Response(serializer.data)

##### same as above but simpler #####
class ProductDetail2(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


##### get related products from the same type as the product #####
class RelatedProducts(APIView):
    def get(self,request,pk):
        product = Product.objects.get(id=pk)
        related_products = Product.objects.only('name','price','images').prefetch_related('images')\
                                                            .filter(product_type=product.product_type)\
                                                        .annotate(stars = Avg(F('review__rating')))
        serializer = ProductSerializer(related_products,many=True)
        return Response(serializer.data)


##### view to handle reviews separetly #####
class ReviewProduct(APIView):
    def get(self,request,pk):
        product = Product.objects.get(id=pk)
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews , many=True)
        return Response(serializer.data)

##### header info about the cart and wishlist #####
class Info(APIView):
    def get(self,request):
        user_cart = None
        user_wishlist = None
        cart_items_num = None
        wishlist_items_num = None
        if request.user.is_authenticated:
            user_cart , created = Cart.objects.get_or_create(customer=request.user)
            user_wishlist, created = WhishList.objects.get_or_create(customer=request.user)

            cart_items_num = user_cart.items.aggregate(Sum('cart_products__quantity'))['cart_products__quantity__sum'] or 0
            wishlist_items_num = user_wishlist.items.aggregate(Sum('wish_products__quantity'))['wish_products__quantity__sum'] or 0
    
        return Response({'cart_items_num': cart_items_num , 'wishlist_items_num' : wishlist_items_num})



class Categories(ListAPIView):
    queryset = Product_Category.objects.all()
    serializer_class = Product_CategorySerializer



# class Products(ListAPIView):
#     pagination_class = Paginator()
#     def get(self,request,page):
#         q = request.GET.get('q') if request.GET.get('q') != None else ''
#         if q=='rating':
#             products = Product.objects.annotate(rating = Sum(F('review__rating')))\
#                                         .annotate(stars = Avg(F('review__rating'))).all().order_by('-rating')
#         elif q=='old':
#             products = Product.objects.annotate(rating = Sum(F('review__rating')))\
#                                         .annotate(stars = Avg(F('review__rating'))).all().order_by('rating')
            
#         # elif q=='sale':
#         #     products = Product.objects.annotate(sale = Count('order__'))\
#         #                                 .annotate(stars = Avg(F('review__rating'))).all()

#         else:
#             products = Product.objects.filter(Q(name__contains = q) | Q(product_type__category__contains = q))\
#                                         .annotate(stars = Avg(F('review__rating'))).order_by('-time_added')
        
#         # serializer = 
#     def post(self,request):
#         pass

