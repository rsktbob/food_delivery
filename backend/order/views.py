from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.db import transaction

from .models import Order

from .models import Order
from .models import *
from .serializer import CartItemSerializer,OrderSerializer



def set_order_state(order, status):
    try:
        order.status = status
        order.save()
        return True
    except:
        return False

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

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
    return Response(response)

@api_view(['GET'])
def courierCheckOrder(request):
    user = request.user
    courier = CourierUser.objects.get(id = user.id)
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
    } for order in orders if order.check_distance(courier.latitude,courier.longitude,5)]
    
    return Response(orders_data)  # 直接返回數組


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

@api_view(['GET'])
def get_cart_items(request):
    user = request.user
    customer = CustomerUser.objects.get(id=user.id)

    cart = Cart.objects.filter(customer=customer).first()
    cart_items = [] if cart is None else cart.cart_items.all()
    serializer = CartItemSerializer(cart_items, many=True, context={'request': request})
    
    return Response(serializer.data)
    
@api_view(['POST'])
def set_order_status(request, order_id):
    new_status = request.data.get('status', '')
    order = Order.objects.get(id=order_id)
    order.status = new_status
    order.save()

    return Response({"message" : "已成功設定訂單狀態"}, status=status.HTTP_200_OK)
    
    

@api_view(['DELETE'])
def delete_cart_items(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()

    return Response({"message": "餐點成功刪除"}, status=status.HTTP_200_OK)    

@api_view(['POST'])
def update_cart_item_quantity(request, cart_item_id): 
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=404)

    new_quantity = int(request.data.get("quantity", 0))
    if new_quantity >= 1:
        cart_item.quantity = new_quantity
        cart_item.save()
    return Response({"success": True, "new_quantity": new_quantity})


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


@api_view(['POST'])
def createOrders(request):
    user = request.user
    cart = Cart.objects.get(customer_id=user.id)
    pos = request.data.get('pos')
    lat = pos.get('lat')
    lng = pos.get('lng')
    address = request.data.get('address')
    payment = request.data.get('payment')

    order = Order.objects.create(
        customer_id = user.id,
        restaurant = cart.restaurant,
        delivery_address = address,
        latitude = lat,
        longitude = lng,
        status = 'Created',
        payment_method = payment,
        total_price = 100,
        delivery_fee = 100
    )

    for item in cart.cart_items.all():
        OrderItem.objects.create(
            order = order,
            menu_item = item.food_item,
            quantity = item.quantity,
            unit_price = item.food_item.price
        )
        item.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def CustomerGetOrder(request):
    user = request.user
    order = Order.objects.filter(customer_id=user.id).exclude(status='Done').exclude(status='reject').first()
    serializer = OrderSerializer(order)
    print(order)
    return Response(serializer.data)

@api_view(['POST'])
def CustomerDoneOrder(request):
    order_id = request.data.get('order_id')
    order = Order.objects.get(id=order_id)
    if order.status == "Finish":
        set_order_state(order, 'Done')
    return Response(status=status.HTTP_200_OK)
