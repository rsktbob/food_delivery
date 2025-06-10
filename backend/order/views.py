from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.db import transaction

from .models import Order
from .models import *
from .serializer import CartItemSerializer,OrderSerializer, CartSerializer


class OrderController:
    
    @staticmethod
    @api_view(['POST'])
    def courier_take_order(request):
        print("take try")
        order_id = request.data.get('order_id')
        courier_id = request.data.get('user_id')
        order = Order.objects.get(id = order_id)
        courier = CourierUser.objects.get(id=courier_id)
        courier.take_order(order)
        return Response({'success': True}, status=status.HTTP_200_OK)
    
    @staticmethod
    @api_view(['GET'])
    def list_available_orders_for_courier(request):
        user = request.user
        courier = CourierUser.objects.filter(id=user.id).first()
        orders = Order.objects.filter(status='accepted')
        

        # 使用字典推導式構建數據
        orders_data = [{
            'id': order.id,
            'customer_name': order.customer.username,
            'restaurant': order.restaurant.name,
            'distance': round(order.get_total_distance(courier.latitude, courier.longitude), 2),
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

        cart, created = Cart.objects.get_or_create(customer=customer, restaurant=restaurant)
        Cart.objects.exclude(customer=customer, restaurant=restaurant).delete()
        
        cart.add_item(food_id, quantity)

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
    @api_view(['GET'])
    def get_cart(request):
        user = request.user
        customer = CustomerUser.objects.get(id=user.id)
        cart = customer.get_cart()        
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)
    

    # @staticmethod
    # @api_view(['POST'])
    # def update_order_status(request, order_id):
    #     new_status = request.data.get('status', '')
    #     order = Order.objects.get(id=order_id)
    #     order.change_status(new_status)
    #     return Response({"message" : "已成功設定訂單狀態"}, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def restaurant_accept_order(request, order_id):
        order = Order.objects.get(id=order_id)
        order.change_status('accepted')
        return Response({"message" : "已成功設定訂單狀態"}, status=status.HTTP_200_OK)
    
    @staticmethod
    @api_view(['POST'])
    def restaurant_reject_order(request, order_id):
        order = Order.objects.get(id=order_id)
        order.change_status('rejected')
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
        return Response({"message": "cart item的數量成功改變"}, status=status.HTTP_200_OK)

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
        customer = CustomerUser.objects.get(id=user.id)
        cart = customer.get_cart()
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
        customer = CustomerUser.objects.get(id=user.id)
        order = customer.get_latest_order()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def customer_done_order(request):
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        order.change_status('done')
        return Response(status=status.HTTP_200_OK)
