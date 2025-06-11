from django.test import TestCase
from django.contrib.auth import authenticate
from unittest.mock import patch, MagicMock
from decimal import Decimal

from account.models import BaseUser, CustomerUser, CourierUser, VendorUser, AuthenticationService
from Restaurant.models import Restaurant
from order.models import Cart, Order


class BaseUserModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        self.base_user = BaseUser.objects.create_user(
            username='testbaseuser',
            email='baseuser@test.com',
            password='testpass123',
            user_type='test_type',
            phone_number='0912345678'
        )

    def test_base_user_creation(self):
        """測試 BaseUser 創建"""
        self.assertEqual(self.base_user.username, 'testbaseuser')
        self.assertEqual(self.base_user.email, 'baseuser@test.com')
        self.assertEqual(self.base_user.user_type, 'test_type')
        self.assertEqual(self.base_user.phone_number, '0912345678')

    def test_base_user_str_inherited(self):
        """測試 BaseUser 繼承 AbstractUser 的 __str__ 方法"""
        # BaseUser 沒有覆寫 __str__，所以應該使用 username
        self.assertEqual(str(self.base_user), 'testbaseuser')


class CustomerUserModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        self.customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            phone_number='0912345678',
            address='Test Customer Address'
        )
        
        # 創建餐廳老闆和餐廳
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345679'
        )

    def test_customer_user_str(self):
        """測試 CustomerUser.__str__ 方法"""
        expected = f"Customer: {self.customer.username}"
        self.assertEqual(str(self.customer), expected)

    @patch('order.models.Order.get_latest_order_for_customer')
    def test_customer_user_get_latest_order(self, mock_get_latest):
        """測試 CustomerUser.get_latest_order 方法"""
        mock_order = MagicMock()
        mock_get_latest.return_value = mock_order
        
        result = self.customer.get_latest_order()
        
        mock_get_latest.assert_called_once_with(self.customer.id)
        self.assertEqual(result, mock_order)

    def test_customer_user_create_cart(self):
        """測試 CustomerUser.create_cart 方法"""
        # 先創建一個現有的購物車
        existing_cart = Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant
        )
        
        # 創建新購物車（應該刪除舊的）
        new_cart = self.customer.create_cart(self.restaurant.id)
        
        # 檢查舊購物車被刪除
        self.assertFalse(Cart.objects.filter(id=existing_cart.id).exists())
        
        # 檢查新購物車
        self.assertEqual(new_cart.customer, self.customer)
        self.assertEqual(new_cart.restaurant, self.restaurant)

    def test_customer_user_has_cart_true(self):
        """測試 CustomerUser.has_cart 方法 - 有購物車"""
        Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant
        )
        
        result = self.customer.has_cart()
        self.assertTrue(result)

    def test_customer_user_has_cart_false(self):
        """測試 CustomerUser.has_cart 方法 - 無購物車"""
        result = self.customer.has_cart()
        self.assertFalse(result)

    def test_customer_user_get_cart_exists(self):
        """測試 CustomerUser.get_cart 方法 - 購物車存在"""
        cart = Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant
        )
        
        result = self.customer.get_cart()
        self.assertEqual(result, cart)

    def test_customer_user_get_cart_not_exists(self):
        """測試 CustomerUser.get_cart 方法 - 購物車不存在"""
        result = self.customer.get_cart()
        self.assertIsNone(result)

    def test_customer_user_get_order_history(self):
        """測試 CustomerUser.get_order_history 方法"""
        # 創建多個訂單
        order1 = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Address 1',
            status='created',
            payment_method='cash'
        )
        
        order2 = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Address 2',
            status='accepted',
            payment_method='cash'
        )
        
        # 創建其他客戶的訂單（不應該包含在內）
        other_customer = CustomerUser.objects.create_user(
            username='othercustomer',
            email='other@test.com',
            password='testpass123',
            user_type='customer',
            address='Other Address'
        )
        
        Order.objects.create(
            customer=other_customer,
            restaurant=self.restaurant,
            delivery_address='Other Address',
            status='created',
            payment_method='cash'
        )
        
        # 取得訂單歷史
        history = self.customer.get_order_history()
        
        # 檢查只包含自己的訂單，且按 id 降序排列
        self.assertEqual(history.count(), 2)
        self.assertEqual(list(history), [order2, order1])

    def test_customer_user_create_order_from_cart_with_cart(self):
        """測試 CustomerUser.create_order_from_cart 方法 - 有購物車"""
        cart = Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant
        )
        
        delivery_info = {
            'address': 'Test Delivery Address',
            'lat': 25.0330,
            'lng': 121.5654,
            'payment': 'cash'
        }
        
        # Mock get_cart 方法來返回我們的 cart 物件
        with patch.object(self.customer, 'get_cart', return_value=cart):
            with patch.object(cart, 'create_order') as mock_create_order:
                mock_order = MagicMock()
                mock_create_order.return_value = mock_order
                
                result = self.customer.create_order_from_cart(delivery_info)
                
                mock_create_order.assert_called_once_with(delivery_info)
                self.assertEqual(result, mock_order)

    def test_customer_user_create_order_from_cart_no_cart(self):
        """測試 CustomerUser.create_order_from_cart 方法 - 無購物車"""
        delivery_info = {
            'address': 'Test Delivery Address',
            'lat': 25.0330,
            'lng': 121.5654,
            'payment': 'cash'
        }
        
        result = self.customer.create_order_from_cart(delivery_info)
        self.assertIsNone(result)


class CourierUserModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        self.courier = CourierUser.objects.create_user(
            username='testcourier',
            email='courier@test.com',
            password='testpass123',
            user_type='courier',
            phone_number='0912345678',
            rating=4.5,
            total_ratings=10,
            vehicle_type='scooter',
            license_plate='ABC-123',
            latitude=25.0330,
            longitude=121.5654
        )

    def test_courier_user_str(self):
        """測試 CourierUser.__str__ 方法"""
        expected = f"Courier: {self.courier.username}"
        self.assertEqual(str(self.courier), expected)

    def test_courier_user_set_position(self):
        """測試 CourierUser.set_position 方法"""
        new_lat = 25.0340
        new_lng = 121.5664
        
        self.courier.set_position(new_lat, new_lng)
        
        self.courier.refresh_from_db()
        self.assertEqual(self.courier.latitude, new_lat)
        self.assertEqual(self.courier.longitude, new_lng)

    def test_courier_user_is_available_true(self):
        """測試 CourierUser.is_available 方法 - 可接單"""
        result = self.courier.is_available()
        self.assertTrue(result)

    def test_courier_user_is_available_false_assigned(self):
        """測試 CourierUser.is_available 方法 - 有 assigned 訂單"""
        # 創建客戶和餐廳
        customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Address'
        )
        
        vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        restaurant = Restaurant.objects.create(
            owner=vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345679'
        )
        
        # 創建 assigned 狀態的訂單
        Order.objects.create(
            customer=customer,
            restaurant=restaurant,
            courier=self.courier,
            delivery_address='Test Address',
            status='assigned',
            payment_method='cash'
        )
        
        result = self.courier.is_available()
        self.assertFalse(result)

    def test_courier_user_is_available_false_picked_up(self):
        """測試 CourierUser.is_available 方法 - 有 picked_up 訂單"""
        # 創建客戶和餐廳
        customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Address'
        )
        
        vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        restaurant = Restaurant.objects.create(
            owner=vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345679'
        )
        
        # 創建 picked_up 狀態的訂單
        Order.objects.create(
            customer=customer,
            restaurant=restaurant,
            courier=self.courier,
            delivery_address='Test Address',
            status='picked_up',
            payment_method='cash'
        )
        
        result = self.courier.is_available()
        self.assertFalse(result)

    def test_courier_user_is_available_true_with_done_order(self):
        """測試 CourierUser.is_available 方法 - 有已完成訂單但仍可接單"""
        # 創建客戶和餐廳
        customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Address'
        )
        
        vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        restaurant = Restaurant.objects.create(
            owner=vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345679'
        )
        
        # 創建 done 狀態的訂單（不影響可用性）
        Order.objects.create(
            customer=customer,
            restaurant=restaurant,
            courier=self.courier,
            delivery_address='Test Address',
            status='done',
            payment_method='cash'
        )
        
        result = self.courier.is_available()
        self.assertTrue(result)


class VendorUserModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor',
            phone_number='0912345678'
        )

    def test_vendor_user_str(self):
        """測試 VendorUser.__str__ 方法"""
        expected = f"Vendor: {self.vendor.username}"
        self.assertEqual(str(self.vendor), expected)

    def test_vendor_user_has_restaurant_false(self):
        """測試 VendorUser.has_restaurant 方法 - 無餐廳"""
        result = self.vendor.has_restaurant()
        self.assertFalse(result)

    def test_vendor_user_has_restaurant_true(self):
        """測試 VendorUser.has_restaurant 方法 - 有餐廳"""
        # 創建餐廳
        Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345679'
        )
        
        result = self.vendor.has_restaurant()
        self.assertTrue(result)


class AuthenticationServiceTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建不同類型的用戶
        self.customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            phone_number='0912345678',
            address='Test Customer Address'
        )
        
        self.courier = CourierUser.objects.create_user(
            username='testcourier',
            email='courier@test.com',
            password='testpass123',
            user_type='courier',
            phone_number='0912345679',
            rating=4.5,
            vehicle_type='scooter',
            license_plate='ABC-123'
        )
        
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor',
            phone_number='0912345680'
        )
        
        # 為 vendor 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345681'
        )

    @patch('django.contrib.auth.authenticate')
    def test_authentication_service_authenticate_user_success(self, mock_authenticate):
        """測試 AuthenticationService.authenticate_user 方法 - 成功"""
        mock_authenticate.return_value = self.customer
        
        result = AuthenticationService.authenticate_user('testcustomer', 'testpass123')
        
        mock_authenticate.assert_called_once_with(
            username='testcustomer',
            password='testpass123'
        )
        self.assertEqual(result, self.customer)

    @patch('django.contrib.auth.authenticate')
    def test_authentication_service_authenticate_user_failure(self, mock_authenticate):
        """測試 AuthenticationService.authenticate_user 方法 - 失敗"""
        mock_authenticate.return_value = None
        
        result = AuthenticationService.authenticate_user('wronguser', 'wrongpass')
        
        mock_authenticate.assert_called_once_with(
            username='wronguser',
            password='wrongpass'
        )
        self.assertIsNone(result)

    def test_authentication_service_get_user_profile_data_customer(self):
        """測試 AuthenticationService.get_user_profile_data 方法 - 客戶"""
        result = AuthenticationService.get_user_profile_data(self.customer)
        
        expected = {
            'id': self.customer.id,
            'username': 'testcustomer',
            'email': 'customer@test.com',
            'user_type': 'customer',
            'phone_number': '0912345678',
            'address': 'Test Customer Address'
        }
        
        self.assertEqual(result, expected)

    def test_authentication_service_get_user_profile_data_courier(self):
        """測試 AuthenticationService.get_user_profile_data 方法 - 外送員"""
        result = AuthenticationService.get_user_profile_data(self.courier)
        
        expected = {
            'id': self.courier.id,
            'username': 'testcourier',
            'email': 'courier@test.com',
            'user_type': 'courier',
            'phone_number': '0912345679',
            'rating': 4.5,
            'vehicle_type': 'scooter',
            'license_plate': 'ABC-123'
        }
        
        self.assertEqual(result, expected)

    def test_authentication_service_get_user_profile_data_vendor_with_restaurant(self):
        """測試 AuthenticationService.get_user_profile_data 方法 - 有餐廳的商家"""
        result = AuthenticationService.get_user_profile_data(self.vendor)
        
        expected = {
            'id': self.vendor.id,
            'username': 'testvendor',
            'email': 'vendor@test.com',
            'user_type': 'vendor',
            'phone_number': '0912345680',
            'restaurant_id': self.restaurant.id
        }
        
        self.assertEqual(result, expected)

    def test_authentication_service_get_user_profile_data_vendor_no_restaurant(self):
        """測試 AuthenticationService.get_user_profile_data 方法 - 無餐廳的商家"""
        # 創建一個沒有餐廳的商家
        vendor_no_restaurant = VendorUser.objects.create_user(
            username='vendorno',
            email='vendorno@test.com',
            password='testpass123',
            user_type='vendor',
            phone_number='0912345682'
        )
        
        result = AuthenticationService.get_user_profile_data(vendor_no_restaurant)
        
        expected = {
            'id': vendor_no_restaurant.id,
            'username': 'vendorno',
            'email': 'vendorno@test.com',
            'user_type': 'vendor',
            'phone_number': '0912345682'
        }
        
        self.assertEqual(result, expected)

    def test_authentication_service_get_user_profile_data_unknown_type(self):
        """測試 AuthenticationService.get_user_profile_data 方法 - 未知用戶類型"""
        # 創建一個基本用戶（不是 customer、courier 或 vendor）
        base_user = BaseUser.objects.create_user(
            username='baseuser',
            email='base@test.com',
            password='testpass123',
            user_type='unknown',
            phone_number='0912345683'
        )
        
        result = AuthenticationService.get_user_profile_data(base_user)
        
        expected = {
            'id': base_user.id,
            'username': 'baseuser',
            'email': 'base@test.com',
            'user_type': 'unknown',
            'phone_number': '0912345683'
        }
        
        self.assertEqual(result, expected)