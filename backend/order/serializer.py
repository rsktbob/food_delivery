from rest_framework import serializers
from .models import *
from Restaurant.serializer import FoodItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    foodItem = FoodItemSerializer(source="food_item")
    
    class Meta:
        model = CartItem
        fields = ['id', 'foodItem', 'quantity', 'special_instructions']