from rest_framework.serializers import ModelSerializer
from rest_framework import serializers 
from base.models import *
from django.contrib.auth import authenticate , login , logout


class UserSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['username','email','password','password2']

    def validate(self,data):
        if data['password'] != data['password2']:
            return serializers.ValidationError("passwords don't match")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        user = MyUser.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        login(request,user)
        return user


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['name' , 'text' , 'rating']


class ProductSerializer(ModelSerializer):
    reviews = ReviewSerializer(source='review_set',many=True , read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class Product_CategorySerializer(ModelSerializer):
    class Meta:
        model = Product_Category
        fields = '__all__'






