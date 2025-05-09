# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from decimal import Decimal
# from unittest.mock import patch, MagicMock

# from order.models import Order, OrderItem, Cart, CartItem
# from account.models import CustomerProfile, CourierProfile, VendorProfile
# from Restaurant.models import Restaurant, MenuItem
# from order.services import OrderService, CustomerOrderService, VendorOrderService, CourierOrderService

# User = get_user_model()

# class OrderServiceTestCase(TestCase):
#     def setUp(self):
#         # Create base user for customer
#         self.customer_user = User.objects.create_user(
#             username='testcustomer',
#             email='customer@test.com',
#             password='password123',
#             user_type='customer'
#         )
        
#         # Create base user for vendor
#         self.vendor_user = User.objects.create_user(
#             username='testvendor',
#             email='vendor@test.com',
#             password='password123',
#             user_type='vendor'
#         )
        
#         # Create base user for courier
#         self.courier_user = User.objects.create_user(
#             username='testcourier',
#             email='courier@test.com',
#             password='password123',
#             user_type='courier'
#         )
        
#         # Create profiles
#         self.customer = CustomerProfile.objects.create(
#             user=self.customer_user,
#             save_address='123 Test St'
#         )
        
#         self.vendor = VendorProfile.objects.create(
#             user=self.vendor_user,
#             restaurant_name='Test Restaurant'
#         )
        
#         self.courier = CourierProfile.objects.create(
#             user=self.courier_user,
#             vehicle_type='Scooter',
#             license_plate='TEST123'
#         )
        
#         # Create restaurant
#         self.restaurant = Restaurant.objects.create(
#             name='Test Restaurant',
#             address='456 Test Ave',
#             owner=self.vendor
#         )
        
#         # Create menu items
#         self.menu_item1 = MenuItem.objects.create(
#             restaurant=self.restaurant,
#             name='Test Burger',
#             description='A delicious test burger',
#             price=Decimal('10.99'),
#             is_available=True
#         )
        
#         self.menu_item2 = MenuItem.objects.create(
#             restaurant=self.restaurant,
#             name='Test Fries',
#             description='Crispy test fries',
#             price=Decimal('4.99'),
#             is_available=True
#         )
        
#         # Create order for testing
#         self.order = Order.objects.create(
#             customer=self.customer,
#             restaurant=self.restaurant,
#             delivery_address='123 Test St',
#             status='Created',
#             payment_method='Credit Card',
#             total_price=Decimal('15.98'),
#             delivery_fee=Decimal('3.00')
#         )
        
#         # Create order items
#         self.order_item1 = OrderItem.objects.create(
#             order=self.order,
#             menu_item=self.menu_item1,
#             quantity=1,
#             unit_price=self.menu_item1.price
#         )
        
#         self.order_item2 = OrderItem.objects.create(
#             order=self.order,
#             menu_item=self.menu_item2,
#             quantity=1,
#             unit_price=self.menu_item2.price
#         )
        
#         # Create cart
#         self.cart = Cart.objects.create(
#             customer=self.customer,
#             restaurant=self.restaurant
#         )
        
#         # Create cart items
#         self.cart_item1 = CartItem.objects.create(
#             cart=self.cart,
#             menu_item=self.menu_item1,
#             quantity=1
#         )
        
#         self.cart_item2 = CartItem.objects.create(
#             cart=self.cart,
#             menu_item=self.menu_item2,
#             quantity=1
#         )
        
#         # Initialize services
#         self.order_service = OrderService()
#         self.customer_order_service = CustomerOrderService()
#         self.vendor_order_service = VendorOrderService()
#         self.courier_order_service = CourierOrderService()

#     def test_set_order_state(self):
#         # Test successful state change
#         result = self.order_service.set_order_state(self.order.id, 'Accepted')
#         self.assertTrue(result)
        
#         # Verify state was changed
#         updated_order = Order.objects.get(id=self.order.id)
#         self.assertEqual(updated_order.status, 'Accepted')
        
#         # Test with invalid order ID
#         result = self.order_service.set_order_state(999, 'Accepted')
#         self.assertFalse(result)

#     def test_get_order_state(self):
#         # Test getting state of valid order
#         status = self.order_service.get_order_state(self.order.id)
#         self.assertEqual(status, 'Created')
        
#         # Test with invalid order ID
#         status = self.order_service.get_order_state(999)
#         self.assertIsNone(status)

#     def test_create_order(self):
#         # Define order info
#         order_info = {
#             'user_id': self.customer_user.id,
#             'restaurant_id': self.restaurant.id,
#             'delivery_address': '789 New Address',
#             'payment_method': 'Cash',
#             'total_price': Decimal('25.98'),
#             'delivery_fee': Decimal('4.00'),
#         }
        
#         # Test successful order creation
#         result = self.customer_order_service.create_order(order_info)
#         self.assertTrue(result)
        
#         # Verify order was created
#         order = Order.objects.filter(
#             customer=self.customer,
#             delivery_address='789 New Address'
#         ).first()
        
#         self.assertIsNotNone(order)
#         self.assertEqual(order.status, 'Created')
#         self.assertEqual(order.payment_method, 'Cash')
#         self.assertEqual(order.total_price, Decimal('25.98'))
#         self.assertEqual(order.delivery_fee, Decimal('4.00'))
        
#         # Test with invalid data
#         invalid_order_info = {
#             'user_id': 999,  # Non-existent user
#             'restaurant_id': self.restaurant.id,
#             'delivery_address': '789 New Address',
#             'payment_method': 'Cash',
#             'total_price': Decimal('25.98'),
#             'delivery_fee': Decimal('4.00'),
#         }
        
#         result = self.customer_order_service.create_order(invalid_order_info)
#         self.assertFalse(result)

#     def test_get_restaurant_orders(self):
#         # Test getting orders for a restaurant
#         orders = self.vendor_order_service.get_restaurant_orders(self.restaurant.id)
#         self.assertEqual(orders.count(), 1)
#         self.assertEqual(orders.first(), self.order)
        
#         # Test with invalid restaurant ID
#         orders = self.vendor_order_service.get_restaurant_orders(999)
#         self.assertEqual(orders.count(), 0)

#     def test_accept_restaurant_order(self):
#         # Test accepting order
#         result = self.vendor_order_service.accept_restaurant_order(self.order.id)
#         self.assertTrue(result)
        
#         # Verify order status was updated
#         updated_order = Order.objects.get(id=self.order.id)
#         self.assertEqual(updated_order.status, 'Accepted')
        
#         # Test with invalid order ID
#         result = self.vendor_order_service.accept_restaurant_order(999)
#         self.assertFalse(result)

#     def test_search_nearby_order(self):
#         # Change order status to Accepted
#         self.order.status = 'Accepted'
#         self.order.save()
        
#         # Test searching nearby orders
#         orders = self.courier_order_service.search_nearby_order()
#         self.assertEqual(orders.count(), 1)
#         self.assertEqual(orders.first(), self.order)
        
#         # Change order status to something else
#         self.order.status = 'Created'
#         self.order.save()
        
#         # Test searching nearby orders with no matching orders
#         orders = self.courier_order_service.search_nearby_order()
#         self.assertEqual(orders.count(), 0)

#     def test_accept_for_delivery(self):
#         # Set order status to Accepted
#         self.order.status = 'Accepted'
#         self.order.save()
        
#         # Test accepting for delivery
#         result = self.courier_order_service.accept_for_delivery(self.order.id)
#         self.assertTrue(result)
        
#         # Verify order status was updated
#         updated_order = Order.objects.get(id=self.order.id)
#         self.assertEqual(updated_order.status, 'Assigned')
        
#         # Test with order in wrong status
#         self.order.status = 'Created'
#         self.order.save()
        
#         result = self.courier_order_service.accept_for_delivery(self.order.id)
#         self.assertFalse(result)

#     def test_pick_up_meal(self):
#         # Set order status to Assigned
#         self.order.status = 'Assigned'
#         self.order.save()
        
#         # Test picking up meal
#         result = self.courier_order_service.pick_up_meal(self.order.id)
#         self.assertTrue(result)
        
#         # Verify order status was updated
#         updated_order = Order.objects.get(id=self.order.id)
#         self.assertEqual(updated_order.status, 'Picked_Up')
        
#         # Test with order in wrong status
#         self.order.status = 'Created'
#         self.order.save()
        
#         result = self.courier_order_service.pick_up_meal(self.order.id)
#         self.assertFalse(result)

#     def test_finish_restaurant_order(self):
#         # Set order status to Picked_Up
#         self.order.status = 'Picked_Up'
#         self.order.save()
        
#         # Test finishing order
#         result = self.courier_order_service.finish_restaurant_order(self.order.id)
#         self.assertTrue(result)
        
#         # Verify order status was updated
#         updated_order = Order.objects.get(id=self.order.id)
#         self.assertEqual(updated_order.status, 'Finish')
        
#         # Test with order in wrong status
#         self.order.status = 'Created'
#         self.order.save()
        
#         result = self.courier_order_service.finish_restaurant_order(self.order.id)
#         self.assertFalse(result)

#     def test_cart_operations(self):
#         # Test get_total_price
#         total_price = self.cart.get_total_price()
#         expected_total = self.menu_item1.price + self.menu_item2.price
#         self.assertEqual(total_price, expected_total)
        
#         # Test cart clear
#         self.cart.clear()
#         self.assertEqual(self.cart.cartitem_set.count(), 0)
#         self.assertIsNone(self.cart.restaurant)

#     def test_cart_item_operations(self):
#         # Test get_total_price for cart item
#         cart_item_price = self.cart_item1.get_total_price()
#         self.assertEqual(cart_item_price, self.menu_item1.price)
        
#         # Test with quantity > 1
#         self.cart_item1.quantity = 3
#         self.cart_item1.save()
        
#         cart_item_price = self.cart_item1.get_total_price()
#         self.assertEqual(cart_item_price, self.menu_item1.price * 3)

#     def test_order_item_operations(self):
#         # Test get_total_price for order item
#         order_item_price = self.order_item1.get_total_price()
#         self.assertEqual(order_item_price, self.menu_item1.price)
        
#         # Test with quantity > 1
#         self.order_item1.quantity = 2
#         self.order_item1.save()
        
#         order_item_price = self.order_item1.get_total_price()
#         self.assertEqual(order_item_price, self.menu_item1.price * 2)