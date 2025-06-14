from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login

from .models import Order, Cart, CartItem
from .serializer import CartItemSerializer, OrderSerializer, CartSerializer


class OrderController:
    
    @staticmethod
    @api_view(['POST'])
    def courier_take_order(request):
        """
        Controller: 只處理 HTTP 請求，委託給 Order 處理業務邏輯
        """
        order_id = request.data.get('order_id')
        courier_id = request.data.get('user_id')
        
        order = Order.objects.get(id=order_id)
        success = order.assign_courier(courier_id)
        
        return Response({'success': success}, status=status.HTTP_200_OK)
    
    @staticmethod
    @api_view(['GET'])
    def list_available_orders_for_courier(request):
        """
        Controller: 委託給 Order 處理查詢邏輯
        """
        courier_id = request.user.id
        orders_data = Order.get_available_orders_for_courier(courier_id)
        return Response(orders_data)

    @staticmethod
    @api_view(['POST'])
    def add_to_cart(request, restaurant_id):
        """
        Controller: 委託給 Cart 處理購物車邏輯
        """
        customer_id = request.user.id
        food_id = request.data.get('food_id')
        quantity = request.data.get('quantity', 1)

        cart = Cart.get_or_create_for_customer(customer_id, restaurant_id)
        cart.add_item(food_id, quantity)

        return Response({'message': "加入到購物車成功"}, status=status.HTTP_200_OK)

    # @staticmethod
    # @api_view(['GET'])
    # def list_cart_items(request):
    #     """
    #     Controller: 簡單的查詢，委託給 Cart
    #     """
    #     customer_id = request.user.id
        
    #     try:
    #         from account.models import CustomerUser
    #         customer = CustomerUser.objects.get(id=customer_id)
    #         cart = customer.cart
    #         cart_items = cart.items.all()
    #     except:
    #         cart_items = []
        
    #     serializer = CartItemSerializer(cart_items, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    @staticmethod
    @api_view(['GET'])
    def get_cart(request):
        """
        Controller: 簡單的查詢，委託給 Cart
        """
        customer_id = request.user.id
        
        try:
            cart = Cart.objects.get(customer_id=customer_id)
        except Cart.DoesNotExist:
            cart = None
            
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def restaurant_accept_order(request, order_id):
        """
        Controller: 委託給 Order 處理狀態變更
        """
        order = Order.objects.get(id=order_id)
        success = order.change_status('accepted')
        
        message = "已成功設定訂單狀態" if success else "狀態變更失敗"
        return Response({"message": message}, status=status.HTTP_200_OK)
    
    @staticmethod
    @api_view(['POST'])
    def restaurant_reject_order(request, order_id):
        """
        Controller: 委託給 Order 處理狀態變更
        """
        order = Order.objects.get(id=order_id)
        success = order.change_status('rejected')
        
        message = "已成功設定訂單狀態" if success else "狀態變更失敗"
        return Response({"message": message}, status=status.HTTP_200_OK)

    @staticmethod    
    @api_view(['DELETE'])
    def delete_cart_items(request, cart_item_id):
        """
        Controller: 簡單的刪除操作
        """
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()

        return Response({"message": "餐點成功刪除"}, status=status.HTTP_200_OK)    

    @staticmethod
    @api_view(['POST'])
    def update_cart_item_quantity(request, cart_item_id): 
        """
        Controller: 委託給 Cart 處理數量變更
        """
        new_quantity = int(request.data.get("quantity", 0))
        customer_id = request.user.id
        
        cart = Cart.objects.get(customer_id=customer_id)
        cart.set_item_quantity(cart_item_id, new_quantity)
        
        return Response({"message": "cart item的數量成功改變"}, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def courier_pick_up_meal(request):
        """
        Controller: 委託給 Order 處理狀態變更
        """
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        order.change_status('picked_up')
        
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def courier_finish_Order(request):
        """
        Controller: 委託給 Order 處理狀態變更
        """
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)        
        order.change_status('finish')
        
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def create_order(request):
        """
        Controller: 委託給 Cart 處理訂單創建
        """
        customer_id = request.user.id
        cart = Cart.objects.get(customer_id=customer_id)
        
        delivery_info = {
            'lat': request.data.get('pos')['lat'],
            'lng': request.data.get('pos')['lng'],
            'address': request.data.get('address'),
            'payment': request.data.get('payment')
        }
        
        order = cart.create_order(delivery_info)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['GET'])
    def customer_get_order(request):
        """
        Controller: 委託給 Order 處理查詢
        """
        customer_id = request.user.id
        order = Order.get_latest_order_for_customer(customer_id)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def customer_done_order(request):
        """
        Controller: 委託給 Order 處理狀態變更
        """
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        order.change_status('done')
        
        return Response(status=status.HTTP_200_OK)