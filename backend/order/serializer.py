from rest_framework import serializers

from .models import Order

from .models import Order
from .models import *
from Restaurant.serializer import FoodItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    foodItem = FoodItemSerializer(source="food_item")
    
    class Meta:
        model = CartItem
        fields = ['id', 'foodItem', 'quantity', 'special_instructions']


class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='menu_item.name', read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'food_name', 'quantity', 'unit_price', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    restaurant = serializers.StringRelatedField(read_only=True)
    courier = serializers.StringRelatedField(read_only=True, allow_null=True)
    items = OrderItemSerializer(many=True, read_only=True)  # ← 加這個

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'restaurant', 'courier',
            'status', 'total_price', 'delivery_fee', 'is_paid',
            'items'
        ]