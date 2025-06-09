from rest_framework import serializers
from .models import *


# class MenuItemSerializer(serializers.ModelSerializer):
#     image_url = serializers.SerializerMethodField()

#     class Meta:
#         model = MenuItem
#         fields = ['id', 'name', 'price', 'image']


class RestaurantSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'image', 'latitude', 
                  'longitude', 'phone_number', 'category']

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'image']

class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['id', 'name', 'image']