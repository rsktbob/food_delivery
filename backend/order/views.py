from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import *
def set_order_state(order, status):
    try:
        order.status = status
        order.save()
        return True
    except:
        return False


@api_view(['POST'])
def courierTakeOrder(request):
    order_id = request.data.get('order_id')
    courier_id = request.data.get('user_id')
    order = Order.objects.get(id=order_id)
    courier = CourierUser.objects.get(id=courier_id)
    
    response = {'success': True }
    if order.status == "Accepted":
        set_order_state(order, 'Assigned')
        order.courier = courier
        order.save()
        response['success'] = True
    else:
        response['success'] = False
    print(order.courier.id) 
    return Response(response)

@api_view(['GET'])
def courierCheckOrder(request):
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
    } for order in orders]
    
    return Response(orders_data)  # 直接返回數組

@api_view(['POST'])
def courierPickUpMeal(request):
    order_id = request.data.get('order_id')
    order = Order.objects.get(id=order_id)
    if order.status == "Assigned":
        set_order_state(order, 'Picked_Up')
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def courierFinishOrder(request):
    order_id = request.data.get('order_id')
    order = Order.objects.get(id=order_id)  
    if order.status == "Picked_Up":
        set_order_state(order, 'Finish')
    return Response(status=status.HTTP_200_OK)