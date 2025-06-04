from rest_framework import serializers
from .models import *
from Restaurant.serializer import FoodItemSerializer,RestaurantSerializer
from account.serializer import CourierSerializer

class CartItemSerializer(serializers.ModelSerializer):
    foodItem = FoodItemSerializer(source="food_item")
    
    class Meta:
        model = CartItem
        fields = ['id', 'foodItem', 'quantity', 'special_instructions']

class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='menu_item.name', read_only=True)
    food_price = serializers.DecimalField(source='unit_price', max_digits=8, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['id', 'food_name', 'quantity', 'food_price']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    courier = CourierSerializer(read_only=True, allow_null=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'restaurant', 'courier' ,
            'status', 'total_price', 'delivery_fee', 'is_paid',
            'items', 'latitude', 'longitude'
        ]