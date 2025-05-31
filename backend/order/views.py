from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import *
from .serializer import CartItemSerializer

def set_order_state(order_id, status):
    try:
        order = Order.objects.get(id=order_id)
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
        set_order_state(order_id, 'Assigned')
        order.courier = courier
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
    } for order in orders]
    
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
        food_item=food_item,
        quantity=quantity
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
    
    
@api_view(['DELETE'])
def delete_cart_items(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()

    return Response({"message": "餐點成功刪除"}, status=status.HTTP_200_OK)    

# class OrderManageHandler:
#     CustomerOrderService = CustomerOrderService()
#     VendorOrderService = VendorOrderService()
#     CourierOrderService = CourierOrderService()

#     @classmethod
#     def createOrder(cls, request, restaurant_id):
#         if request.method == "GET":
#             form = OrderForm()
#             context = {"form" : form}
#             return render(request, "order/create_order.html", context)
#         elif request.method == "POST":
#             customer = request.user.customer_profile
#             restaurant = Restaurant.objects.get(id=restaurant_id)
#             cart = Cart.objects.filter(customer=customer, restaurant=restaurant).first()
#             cart_items = cart.cart_items.all()
            
#             form = OrderForm(request.POST)
#             if form.is_valid() and not cart_items:
#                 order = form.save(commit=False)
                
#                 order.total_price = sum(cart_item.get_total_price() for cart_item in cart_items)
#                 order.restaurant = restaurant
#                 order.customer = customer
#                 order.save()                
#                 cart.delete()
#                 print(order)
                
#                 return redirect("home")
#             else:
#                 form = OrderForm()
#                 context = {"form" : form}
#                 return render(request, "order/create_order.html", context)
  
#     @classmethod
#     def setOrderState(cls, request):
#         order_id = request.POST.get('order_id')  # 假設訂單 ID 傳遞過來
#         state = request.POST.get('state')  # 新的訂單狀態
        
#         success = cls.CustomerOrderService.set_order_state(order_id, state)
#         if success:
#             return JsonResponse({'status': 'success', 'message': 'Order state updated successfully!'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Failed to update order state.'}, status=400)
        
    
#     @classmethod
#     def getOrderState(cls, request):
#         # 從 POST 請求中獲取訂單 ID
#         order_id = request.POST.get('order_id')
        
#         order_state = cls.CustomerOrderService.get_order_state(order_id)
#         if order_state is not None:
#             return JsonResponse({'status': 'success', 'order_state': order_state})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
        
      
#     def checkCourierOrder(cls, request):
#         nearby_orders = cls.CourierOrderService.search_nearby_order()
#         if nearby_orders:
#             return JsonResponse({'status': 'success', 'nearby_orders': nearby_orders})
#         else:
#             return JsonResponse({'status': 'info', 'message': 'No nearby orders found.'})

#     @classmethod
#     def checkVendorOrder(cls, request):
#         restaurant_id = request.POST.get('restaurant_id')
        
#         orders = cls.VendorOrderService.get_restaurant_orders(restaurant_id)
#         if orders:
#             return JsonResponse({'status': 'success', 'orders': orders})
#         else:
#             return JsonResponse({'status': 'info', 'message': 'No orders found for this restaurant.'})

#     @classmethod
#     def acceptVendorOrder(cls, request):
#         order_id = request.POST.get('order_id')
#         success = cls.VendorOrderService.accept_restaurant_order(order_id)
#         if success:
#             return JsonResponse({'status': 'success', 'message': 'Order accepted successfully.'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Failed to accept the order.'})

#     @classmethod
#     # vendor finish order
#     def finishOrder(cls, request):
#         success = cls.VendorOrderService.finish_restaurant_order(request)
#         if success:
#             return JsonResponse({'status': 'success', 'message': 'Order finished successfully.'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Failed to finish the order.'})
        
#     @classmethod
#     def enterOrderManagePage(cls, request):
#         customer = request.user
        
#         orders = Order.objects.filter(customer=customer)
#         context = {"orders" : orders}
#         return render(request, "order/order_mange_page.html", context)

# @login_required
# def add_to_shopping_cart(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    
#     try:
#         data = json.loads(request.POST.get()
#         menu_item_id = data.get('menu_item_id')
#         quantity = data.get('quantity', 1)
#         customizations = data.get('customizations', [])
#         special_instructions = data.get('special_instructions', '')
        
#         menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
#         # Get or create user's cart
#         cart, created = Cart.objects.get_or_create(customer=request.user)
        
#         # Check if adding from a different restaurant
#         if cart.restaurant and cart.restaurant != menu_item.restaurant:
#             return JsonResponse({
#                 'error': 'You already have items from a different restaurant in your cart',
#                 'current_restaurant': cart.restaurant.name
#             }, status=400)
        
#         # Set the restaurant if cart is empty
#         if not cart.restaurant:
#             cart.restaurant = menu_item.restaurant
#             cart.save()
        
#         # Create cart item
#         cart_item = CartItem.objects.create(
#             cart=cart,
#             menu_item=menu_item,
#             quantity=quantity,
#             special_instructions=special_instructions
#         )
        
#         # Add customizations
#         for custom in customizations:
#             choice_id = custom.get('choice_id')
#             if choice_id:
#                 choice = get_object_or_404(CustomizationChoice, id=choice_id)
#                 CartItemCustomization.objects.create(
#                     cart_item=cart_item,
#                     choice=choice
#                 )
        
#         return JsonResponse({
#             'success': True,
#             'cart_item_id': cart_item.id,
#             'cart_total': cart.get_total_price()
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

# @login_required
# def get_cart(request):
#     try:
#         cart = Cart.objects.get(customer=request.user)
#         items = []
        
#         for item in cart.cartitem_set.all():
#             customizations = []
#             for custom in item.cartitemcustomization_set.all():
#                 customizations.append({
#                     'option_name': custom.choice.option.name,
#                     'choice_name': custom.choice.name,
#                     'additional_price': float(custom.choice.additional_price)
#                 })
            
#             items.append({
#                 'id': item.id,
#                 'menu_item_id': item.menu_item.id,
#                 'name': item.menu_item.name,
#                 'quantity': item.quantity,
#                 'unit_price': float(item.menu_item.price),
#                 'total_price': float(item.get_total_price()),
#                 'special_instructions': item.special_instructions,
#                 'customizations': customizations
#             })
        
#         return JsonResponse({
#             'success': True,
#             'restaurant': {
#                 'id': cart.restaurant.id,
#                 'name': cart.restaurant.name
#             } if cart.restaurant else None,
#             'items': items,
#             'total': float(cart.get_total_price())
#         })
        
#     except Cart.DoesNotExist:
#         return JsonResponse({
#             'success': True,
#             'restaurant': None,
#             'items': [],
#             'total': 0
#         })

# @login_required
# @require_POST
# def create_order(request):
#     try:
#         data = json.loads(request.body)
#         address_id = data.get('address_id')
#         payment_method = data.get('payment_method')
        
#         # Get user's cart
#         cart = get_object_or_404(Cart, customer=request.user)
        
#         if not cart.cartitem_set.exists():
#             return JsonResponse({'error': 'Your cart is empty'}, status=400)
        
#         # Get delivery address
#         address = get_object_or_404(Address, id=address_id, user=request.user)
        
#         with transaction.atomic():
#             # Create order
#             order = Order.objects.create(
#                 customer=request.user,
#                 restaurant=cart.restaurant,
#                 delivery_address=address,
#                 payment_method=payment_method,
#                 total_price=0,  # Will be calculated later
#                 delivery_fee=5.00,  # Example fixed fee
#                 tax=0,  # Will be calculated later
#                 grand_total=0  # Will be calculated later
#             )
            
#             # Create order items from cart items
#             for cart_item in cart.cartitem_set.all():
#                 order_item = OrderItem.objects.create(
#                     order=order,
#                     menu_item=cart_item.menu_item,
#                     quantity=cart_item.quantity,
#                     unit_price=cart_item.menu_item.price,
#                     special_instructions=cart_item.special_instructions
#                 )
                
#                 # Add customizations
#                 for cart_customization in cart_item.cartitemcustomization_set.all():
#                     OrderItemCustomization.objects.create(
#                         order_item=order_item,
#                         option_name=cart_customization.choice.option.name,
#                         choice_name=cart_customization.choice.name,
#                         additional_price=cart_customization.choice.additional_price
#                     )
            
#             # Calculate totals
#             order.calculate_totals()
            
#             # Clear the cart
#             cart.clear()
            
#             # Check for available couriers
#             check_courier_order(order)
            
#             return JsonResponse({
#                 'success': True,
#                 'order_id': order.id,
#                 'status': order.status
#             })
            
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

