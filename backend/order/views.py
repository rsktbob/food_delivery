from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.db import transaction

from .models import Order

from .models import Order
from .models import *
from .serializer import CartItemSerializer,OrderSerializer


class OrderController:
    
    @staticmethod
    @api_view(['POST'])
    def courier_take_order(request):
        order_id = request.data.get('order_id')
        courier_id = request.data.get('user_id')
        courier = CourierUser.objects.get(id=courier_id)
        courier.take_order(order_id)
        return Response({'message': "courier取單成功"}, status=status.HTTP_200_OK)
    
    @staticmethod
    @api_view(['GET'])
    def list_available_orders_for_courier(request):
        user = request.user
        courier = CourierUser.objects.filter(id=user.id).first()
        orders = Order.objects.filter(status='Accepted')
        

        # 使用字典推導式構建數據
        orders_data = [{
            'id': order.id,
            'customer_name': order.customer.username,
            'restaurant': order.restaurant.name,
            'distance': 100,
            'fee': 100,
            'restaurant_position': {
                'lat': float(order.restaurant.latitude),
                'lng': float(order.restaurant.longitude)
            },
            # 新增顧客位置信息  
            'customer_position': {
                'lat': float(order.latitude),
                'lng': float(order.longitude)
            }
        } for order in orders if order.is_in_delivery_distance(courier.latitude,courier.longitude,5)]

        return Response(orders_data)  # 直接返回數組

    @staticmethod
    @api_view(['POST'])
    def add_to_cart(request, restaurant_id):
        user = request.user
        customer = CustomerUser.objects.get(id=user.id)
        restaurant = Restaurant.objects.get(id=restaurant_id)
        food_id = request.data.get('food_id')
        quantity = request.data.get('quantity', 1)

        if not food_id or quantity <= 0:
            return Response({'error': '資料不正確'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            food_item = FoodItem.objects.get(id=food_id)
        except FoodItem.DoesNotExist:
            return Response({'error': '找不到該食物'}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(customer=customer, restaurant=restaurant)
        Cart.objects.exclude(customer=customer, restaurant=restaurant).delete()

        # 檢查是否已經存在購物車項目
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            food_item=food_item
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'message': "加入到購物車成功"}, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['GET'])
    def list_cart_items(request):
        user = request.user
        customer = CustomerUser.objects.get(id=user.id)

        if customer.has_cart():
            cart = customer.cart
            cart_items = cart.items.all()
        else:
            cart_items = []
        
        serializer = CartItemSerializer(cart_items, many=True, context={'request': request})
        
        return Response(serializer.data)
    
    @staticmethod
    @api_view(['POST'])
    def update_order_status(request, order_id):
        new_status = request.data.get('status', '')
        order = Order.objects.get(id=order_id)
        order.change_status(new_status)
        return Response({"message" : "已成功設定訂單狀態"}, status=status.HTTP_200_OK)

    @staticmethod    
    @api_view(['DELETE'])
    def delete_cart_items(request, cart_item_id):
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()

        return Response({"message": "餐點成功刪除"}, status=status.HTTP_200_OK)    

    @staticmethod
    @api_view(['POST'])
    def update_cart_item_quantity(request, cart_item_id): 
        new_quantity = int(request.data.get("quantity", 0))
        user = request.user
        customer = CustomerUser.objects.get(id=user.id)
        cart = customer.cart
        cart.set_item_quantity(cart_item_id, new_quantity)

    @staticmethod
    @api_view(['POST'])
    def courier_pick_up_meal(request):
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        order.change_status('picked_up')
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def courier_finish_Order(request):
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)        
        order.change_status('finish')
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def create_order(request):
        user = request.user
        cart = Cart.objects.get(customer_id=user.id)
        pos = request.data.get('pos')
        lat = pos.get('lat')
        lng = pos.get('lng')
        address = request.data.get('address')
        payment = request.data.get('payment')

        cart.create_order(lat, lng, address, payment)

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['GET'])
    def customer_get_order(request):
        user = request.user
        customer = CustomerUser.objects.filter(id=user.id)
        order = customer.get_latest_order()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def mark_order_done(request):
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        order.change_status('Done')
        return Response(status=status.HTTP_200_OK)
