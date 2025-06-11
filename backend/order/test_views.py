import json
from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock, Mock
from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from order.views import OrderController
from order.models import Cart, CartItem, Order, OrderItem
from account.models import CustomerUser, CourierUser, VendorUser
from Restaurant.models import Restaurant, FoodItem
from account.factories import UserFactory

class OrderControllerTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 使用 APIRequestFactory
        self.factory = APIRequestFactory()
        self.user_factory = UserFactory()
        
        # 使用 UserFactory 創建用戶
        self.customer = self.user_factory.create_user(
            user_type='customer',
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            phone_number='0912345678',
            address='Test Customer Address'
        )
        
        self.courier = self.user_factory.create_user(
            user_type='courier',
            username='testcourier',
            email='courier@test.com',
            password='testpass123',
            phone_number='0912345679',
            vehicle_type='scooter',
            license_plate='ABC-123'
        )
        
        self.vendor = self.user_factory.create_user(
            user_type='vendor',
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            phone_number='0912345680',
            restaurant_name='Test Restaurant',
            restaurant_address='Test Address',
            restaurant_phone_number='0912345681',
            restaurant_latitude=25.0330,
            restaurant_longitude=121.5654
        )
        
        # 取得餐廳
        self.restaurant = Restaurant.objects.get(owner=self.vendor)
        
        # 創建餐點
        self.food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Test Food',
            price=Decimal('100.00')
        )
        
        # 創建購物車和訂單
        self.cart = Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant
        )
        
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Test Address',
            latitude=25.0340,
            longitude=121.5664,
            status='created',
            payment_method='cash'
        )

    def test_courier_take_order_success(self):
        """測試 courier_take_order - 成功接單"""
        request_data = {
            'order_id': self.order.id,
            'user_id': self.courier.id
        }
        
        request = self.factory.post('/api/courier-take-order/', request_data, format='json')
        force_authenticate(request, user=self.courier)
        
        # Mock Order.objects.get 和 assign_courier
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'assign_courier', return_value=True) as mock_assign:
                # 直接調用靜態方法
                response = OrderController.courier_take_order(request)
        
        mock_assign.assert_called_once_with(self.courier.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_courier_take_order_failure(self):
        """測試 courier_take_order - 接單失敗"""
        request_data = {
            'order_id': self.order.id,
            'user_id': self.courier.id
        }
        
        request = self.factory.post('/api/courier-take-order/', request_data, format='json')
        force_authenticate(request, user=self.courier)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'assign_courier', return_value=False) as mock_assign:
                response = OrderController.courier_take_order(request)
        
        mock_assign.assert_called_once_with(self.courier.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['success'])

    def test_list_available_orders_for_courier(self):
        """測試 list_available_orders_for_courier"""
        request = self.factory.get('/api/courier-check-orders/')
        force_authenticate(request, user=self.courier)
        
        mock_orders_data = [
            {
                'id': self.order.id,
                'customer_name': 'test customer',
                'restaurant': 'test restaurant',
                'distance': 2.5,
                'fee': 80
            }
        ]
        
        with patch('order.views.Order.get_available_orders_for_courier', return_value=mock_orders_data) as mock_get_orders:
            response = OrderController.list_available_orders_for_courier(request)
        
        mock_get_orders.assert_called_once_with(self.courier.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_orders_data)

    def test_add_to_cart(self):
        """測試 add_to_cart"""
        request_data = {
            'food_id': self.food_item.id,
            'quantity': 2
        }
        
        request = self.factory.post(f'/api/restaurants/{self.restaurant.id}/add-to-cart/', 
                                    request_data, format='json')
        force_authenticate(request, user=self.customer)
        
        with patch('order.views.Cart.get_or_create_for_customer', return_value=self.cart) as mock_get_cart:
            with patch.object(self.cart, 'add_item') as mock_add_item:
                response = OrderController.add_to_cart(request, self.restaurant.id)
        
        mock_get_cart.assert_called_once_with(self.customer.id, self.restaurant.id)
        mock_add_item.assert_called_once_with(self.food_item.id, 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "加入到購物車成功")

    def test_add_to_cart_default_quantity(self):
        """測試 add_to_cart - 使用預設數量"""
        request_data = {
            'food_id': self.food_item.id
            # 沒有提供 quantity
        }
        
        request = self.factory.post(f'/api/restaurants/{self.restaurant.id}/add-to-cart/', 
                                    request_data, format='json')
        force_authenticate(request, user=self.customer)
        
        with patch('order.views.Cart.get_or_create_for_customer', return_value=self.cart):
            with patch.object(self.cart, 'add_item') as mock_add_item:
                response = OrderController.add_to_cart(request, self.restaurant.id)
        
        mock_add_item.assert_called_once_with(self.food_item.id, 1)  # 預設數量為 1

    def test_list_cart_items_with_cart(self):
        """測試 list_cart_items - 有購物車"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        request = self.factory.get('/api/cart/items/')
        force_authenticate(request, user=self.customer)
        
        # Mock CustomerUser.objects.get
        mock_customer = MagicMock()
        mock_customer.cart = self.cart
        
        # Mock CartItemSerializer
        expected_data = [
            {
                'id': cart_item.id,
                'food_item': {
                    'id': self.food_item.id,
                    'name': 'Test Food',
                    'price': '100.00'
                },
                'quantity': 2
            }
        ]
        
        with patch('order.views.CustomerUser.objects.get', return_value=mock_customer):
            with patch('order.views.CartItemSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = OrderController.list_cart_items(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_cart_items_no_cart(self):
        """測試 list_cart_items - 無購物車"""
        request = self.factory.get('/api/cart/items/')
        force_authenticate(request, user=self.customer)
        
        # Mock exception
        with patch('order.views.CustomerUser.objects.get', side_effect=Exception("No cart")):
            with patch('order.views.CartItemSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = []
                mock_serializer.return_value = mock_serializer_instance
                
                response = OrderController.list_cart_items(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_cart_exists(self):
        """測試 get_cart - 購物車存在"""
        request = self.factory.get('/api/cart/')
        force_authenticate(request, user=self.customer)
        
        expected_data = {
            'id': self.cart.id,
            'restaurant': self.restaurant.id,
            'items_count': 0
        }
        
        with patch('order.views.Cart.objects.get', return_value=self.cart):
            with patch('order.views.CartSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = OrderController.get_cart(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_cart_not_exists(self):
        """測試 get_cart - 購物車不存在"""
        request = self.factory.get('/api/cart/')
        force_authenticate(request, user=self.customer)
        
        with patch('order.views.Cart.objects.get', side_effect=Cart.DoesNotExist):
            with patch('order.views.CartSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = None
                mock_serializer.return_value = mock_serializer_instance
                
                response = OrderController.get_cart(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_restaurant_accept_order_success(self):
        """測試 restaurant_accept_order - 成功接受"""
        request = self.factory.post(f'/api/orders/{self.order.id}/accept/')
        force_authenticate(request, user=self.vendor)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'change_status', return_value=True) as mock_change_status:
                response = OrderController.restaurant_accept_order(request, self.order.id)
        
        mock_change_status.assert_called_once_with('accepted')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "已成功設定訂單狀態")

    def test_restaurant_accept_order_failure(self):
        """測試 restaurant_accept_order - 接受失敗"""
        request = self.factory.post(f'/api/orders/{self.order.id}/accept/')
        force_authenticate(request, user=self.vendor)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'change_status', return_value=False) as mock_change_status:
                response = OrderController.restaurant_accept_order(request, self.order.id)
        
        mock_change_status.assert_called_once_with('accepted')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "狀態變更失敗")

    def test_restaurant_reject_order_success(self):
        """測試 restaurant_reject_order - 成功拒絕"""
        request = self.factory.post(f'/api/orders/{self.order.id}/reject/')
        force_authenticate(request, user=self.vendor)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'change_status', return_value=True) as mock_change_status:
                response = OrderController.restaurant_reject_order(request, self.order.id)
        
        mock_change_status.assert_called_once_with('rejected')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "已成功設定訂單狀態")

    def test_restaurant_reject_order_failure(self):
        """測試 restaurant_reject_order - 拒絕失敗"""
        request = self.factory.post(f'/api/orders/{self.order.id}/reject/')
        force_authenticate(request, user=self.vendor)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'change_status', return_value=False) as mock_change_status:
                response = OrderController.restaurant_reject_order(request, self.order.id)
        
        mock_change_status.assert_called_once_with('rejected')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "狀態變更失敗")

    def test_delete_cart_items(self):
        """測試 delete_cart_items"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        request = self.factory.delete(f'/api/cart/items/{cart_item.id}/')
        force_authenticate(request, user=self.customer)
        
        with patch('order.views.CartItem.objects.get', return_value=cart_item):
            with patch.object(cart_item, 'delete') as mock_delete:
                response = OrderController.delete_cart_items(request, cart_item.id)
        
        mock_delete.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "餐點成功刪除")

    def test_update_cart_item_quantity(self):
        """測試 update_cart_item_quantity"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        request_data = {'quantity': 5}
        request = self.factory.post(f'/api/cart/items/{cart_item.id}/quantity/', 
                                    request_data, format='json')
        force_authenticate(request, user=self.customer)
        
        with patch('order.views.Cart.objects.get', return_value=self.cart):
            with patch.object(self.cart, 'set_item_quantity') as mock_set_quantity:
                response = OrderController.update_cart_item_quantity(request, cart_item.id)
        
        mock_set_quantity.assert_called_once_with(cart_item.id, 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "cart item的數量成功改變")

    def test_update_cart_item_quantity_default_zero(self):
        """測試 update_cart_item_quantity - 預設數量為0"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        request_data = {}  # 沒有提供 quantity
        request = self.factory.post(f'/api/cart/items/{cart_item.id}/quantity/', 
                                    request_data, format='json')
        force_authenticate(request, user=self.customer)
        
        with patch('order.views.Cart.objects.get', return_value=self.cart):
            with patch.object(self.cart, 'set_item_quantity') as mock_set_quantity:
                response = OrderController.update_cart_item_quantity(request, cart_item.id)
        
        mock_set_quantity.assert_called_once_with(cart_item.id, 0)

    def test_courier_pick_up_meal(self):
        """測試 courier_pick_up_meal"""
        request_data = {'order_id': self.order.id}
        request = self.factory.post('/api/courier-pick-up/', request_data, format='json')
        force_authenticate(request, user=self.courier)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'change_status') as mock_change_status:
                response = OrderController.courier_pick_up_meal(request)
        
        mock_change_status.assert_called_once_with('picked_up')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_courier_finish_order(self):
        """測試 courier_finish_Order"""
        request_data = {'order_id': self.order.id}
        request = self.factory.post('/api/courier-finish/', request_data, format='json')
        force_authenticate(request, user=self.courier)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'change_status') as mock_change_status:
                response = OrderController.courier_finish_Order(request)
        
        mock_change_status.assert_called_once_with('finish')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        """測試 create_order"""
        request_data = {
            'pos': {'lat': 25.0330, 'lng': 121.5654},
            'address': 'Test Delivery Address',
            'payment': 'cash'
        }
        
        request = self.factory.post('/api/create-order/', request_data, format='json')
        force_authenticate(request, user=self.customer)
        
        mock_order = MagicMock()
        mock_order.id = 123
        expected_delivery_info = {
            'lat': 25.0330,
            'lng': 121.5654,
            'address': 'Test Delivery Address',
            'payment': 'cash'
        }
        
        with patch('order.views.Cart.objects.get', return_value=self.cart):
            with patch.object(self.cart, 'create_order', return_value=mock_order) as mock_create_order:
                response = OrderController.create_order(request)
        
        mock_create_order.assert_called_once_with(expected_delivery_info)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_get_order(self):
        """測試 customer_get_order"""
        request = self.factory.get('/api/customer/order/')
        force_authenticate(request, user=self.customer)
        
        expected_data = {
            'id': self.order.id,
            'status': 'created',
            'restaurant': self.restaurant.name
        }
        
        with patch('order.views.Order.get_latest_order_for_customer', return_value=self.order):
            with patch('order.views.OrderSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = OrderController.customer_get_order(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_customer_done_order(self):
        """測試 customer_done_order"""
        request_data = {'order_id': self.order.id}
        request = self.factory.post('/api/customer-done/', request_data, format='json')
        force_authenticate(request, user=self.customer)
        
        with patch('order.views.Order.objects.get', return_value=self.order):
            with patch.object(self.order, 'change_status') as mock_change_status:
                response = OrderController.customer_done_order(request)
        
        mock_change_status.assert_called_once_with('done')
        self.assertEqual(response.status_code, status.HTTP_200_OK)