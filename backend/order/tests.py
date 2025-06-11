from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from unittest.mock import patch, MagicMock
from decimal import Decimal
from rest_framework import status

from order.views import OrderController
from order.models import Cart, CartItem, Order, OrderItem
from account.models import CustomerUser, CourierUser, VendorUser
from Restaurant.models import Restaurant, FoodItem


class CartModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建客戶
        self.customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Customer Address'
        )
        
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678'
        )
        
        # 創建餐點
        self.food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Test Food',
            price=Decimal('100.00')
        )
        
        # 創建購物車
        self.cart = Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant
        )

    def test_cart_str(self):
        """測試 Cart.__str__ 方法"""
        expected = f"Cart {self.cart.id}"
        self.assertEqual(str(self.cart), expected)

    def test_cart_get_total_price_empty(self):
        """測試 Cart.get_total_price 方法 - 空購物車"""
        result = self.cart.get_total_price()
        self.assertEqual(result, 0)

    def test_cart_get_total_price_with_items(self):
        """測試 Cart.get_total_price 方法 - 有商品"""
        CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        result = self.cart.get_total_price()
        self.assertEqual(result, Decimal('200.00'))

    def test_cart_add_item_new(self):
        """測試 Cart.add_item 方法 - 新商品"""
        self.cart.add_item(self.food_item.id, 3)
        
        cart_item = self.cart.items.get(food_item=self.food_item)
        self.assertEqual(cart_item.quantity, 3)

    def test_cart_add_item_existing(self):
        """測試 Cart.add_item 方法 - 現有商品"""
        # 先建立一個商品
        CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        # 再次新增同一商品
        self.cart.add_item(self.food_item.id, 3)
        
        cart_item = self.cart.items.get(food_item=self.food_item)
        self.assertEqual(cart_item.quantity, 5)  # 2 + 3

    def test_cart_set_item_quantity(self):
        """測試 Cart.set_item_quantity 方法"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        self.cart.set_item_quantity(cart_item.id, 5)
        
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_cart_clear_items(self):
        """測試 Cart.clear_items 方法"""
        CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        self.cart.clear_items()
        
        self.assertEqual(self.cart.items.count(), 0)

    def test_cart_create_order(self):
        """測試 Cart.create_order 方法"""
        CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )
        
        delivery_info = {
            'address': 'Test Delivery Address',
            'lat': 25.0330,
            'lng': 121.5654,
            'payment': 'cash'
        }
        
        order = self.cart.create_order(delivery_info)
        
        # 驗證訂單資訊
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.restaurant, self.restaurant)
        self.assertEqual(order.delivery_address, 'Test Delivery Address')
        self.assertEqual(order.latitude, 25.0330)
        self.assertEqual(order.longitude, 121.5654)
        self.assertEqual(order.status, 'created')
        self.assertEqual(order.payment_method, 'cash')
        self.assertEqual(order.total_price, Decimal('200.00'))  # 計算後的總價
        self.assertEqual(order.delivery_fee, 80)
        
        # 驗證訂單商品
        self.assertEqual(order.items.count(), 1)
        order_item = order.items.first()
        self.assertEqual(order_item.food_item, self.food_item)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.unit_price, self.food_item.price)
        
        # 驗證購物車已清空
        self.assertEqual(self.cart.items.count(), 0)

    def test_cart_get_or_create_for_customer_new(self):
        """測試 Cart.get_or_create_for_customer 方法 - 創建新購物車"""
        # 先刪除現有購物車
        self.cart.delete()
        
        cart = Cart.get_or_create_for_customer(
            self.customer.id,
            self.restaurant.id
        )
        
        self.assertEqual(cart.customer, self.customer)
        self.assertEqual(cart.restaurant, self.restaurant)

    def test_cart_get_or_create_for_customer_existing(self):
        """測試 Cart.get_or_create_for_customer 方法 - 取得現有購物車"""
        cart = Cart.get_or_create_for_customer(
            self.customer.id,
            self.restaurant.id
        )
        
        self.assertEqual(cart.id, self.cart.id)

    def test_cart_get_or_create_for_customer_delete_other(self):
        """測試 Cart.get_or_create_for_customer 方法 - 刪除其他餐廳購物車"""
        # 創建另一個餐廳老闆
        other_vendor = VendorUser.objects.create_user(
            username='othervendor',
            email='othervendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        other_restaurant = Restaurant.objects.create(
            owner=other_vendor,
            name='Other Restaurant',
            address='Other Address',
            latitude=25.0340,
            longitude=121.5664,
            phone_number='0912345679'
        )
        
        original_cart_id = self.cart.id
        
        # 為其他餐廳創建購物車
        new_cart = Cart.get_or_create_for_customer(
            self.customer.id,
            other_restaurant.id
        )
        
        # 原本的購物車應該被刪除
        self.assertFalse(Cart.objects.filter(id=original_cart_id).exists())
        
        # 新購物車應該是其他餐廳的
        self.assertEqual(new_cart.restaurant, other_restaurant)


class CartItemModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建客戶
        self.customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Customer Address'
        )
        
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678'
        )
        
        # 創建餐點
        self.food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Test Food',
            price=Decimal('150.00')
        )
        
        # 創建購物車
        self.cart = Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant
        )
        
        # 創建購物車商品
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            food_item=self.food_item,
            quantity=2
        )

    def test_cart_item_str(self):
        """測試 CartItem.__str__ 方法"""
        expected = f"2 x {self.food_item.name}"
        self.assertEqual(str(self.cart_item), expected)

    def test_cart_item_get_total_price(self):
        """測試 CartItem.get_total_price 方法"""
        result = self.cart_item.get_total_price()
        self.assertEqual(result, Decimal('300.00'))  # 150 * 2

    def test_cart_item_set_quantity_valid(self):
        """測試 CartItem.set_quantity 方法 - 有效數量"""
        self.cart_item.set_quantity(5)
        
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)

    def test_cart_item_set_quantity_invalid_zero(self):
        """測試 CartItem.set_quantity 方法 - 無效數量 0"""
        original_quantity = self.cart_item.quantity
        
        self.cart_item.set_quantity(0)
        
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, original_quantity)

    def test_cart_item_set_quantity_invalid_negative(self):
        """測試 CartItem.set_quantity 方法 - 無效數量負數"""
        original_quantity = self.cart_item.quantity
        
        self.cart_item.set_quantity(-1)
        
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, original_quantity)


class OrderModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建客戶
        self.customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Customer Address'
        )
        
        # 創建外送員
        self.courier = CourierUser.objects.create_user(
            username='testcourier',
            email='courier@test.com',
            password='testpass123',
            user_type='courier',
            latitude=25.0330,
            longitude=121.5654
        )
        
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678'
        )
        
        # 創建餐點
        self.food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Test Food',
            price=Decimal('200.00')
        )
        
        # 創建訂單
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Test Address',
            latitude=25.0340,
            longitude=121.5664,
            status='created',
            payment_method='cash',
            delivery_fee=80
        )

    def test_order_str(self):
        """測試 Order.__str__ 方法"""
        expected = f"Order #{self.order.id}"
        self.assertEqual(str(self.order), expected)

    def test_order_calculate_totals(self):
        """測試 Order.calculate_totals 方法"""
        OrderItem.objects.create(
            order=self.order,
            food_item=self.food_item,
            quantity=2,
            unit_price=Decimal('200.00')
        )
        
        self.order.calculate_totals()
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, Decimal('400'))
        self.assertEqual(self.order.grand_total, Decimal('480'))  # 400 + 80

    def test_order_change_status_valid(self):
        """測試 Order.change_status 方法 - 有效轉換"""
        result = self.order.change_status('accepted')
        
        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'accepted')

    def test_order_change_status_invalid(self):
        """測試 Order.change_status 方法 - 無效轉換"""
        result = self.order.change_status('picked_up')  # created -> picked_up 無效
        
        self.assertFalse(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'created')

    def test_order_add_item(self):
        """測試 Order.add_item 方法"""
        self.order.add_item(self.food_item, 3, Decimal('200.00'))
        
        order_item = self.order.items.get(food_item=self.food_item)
        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(order_item.unit_price, Decimal('200.00'))

    @patch('account.models.CourierUser.is_available')
    def test_order_assign_courier_success(self, mock_is_available):
        """測試 Order.assign_courier 方法 - 成功指派"""
        mock_is_available.return_value = True
        self.order.status = 'accepted'
        self.order.save()
        
        with patch.object(self.restaurant, 'get_distance', return_value=2.0):
            result = self.order.assign_courier(self.courier.id)
        
        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.courier, self.courier)
        self.assertEqual(self.order.status, 'assigned')

    @patch('account.models.CourierUser.is_available')
    def test_order_assign_courier_not_available(self, mock_is_available):
        """測試 Order.assign_courier 方法 - 外送員不可用"""
        mock_is_available.return_value = False
        self.order.status = 'accepted'
        self.order.save()
        
        result = self.order.assign_courier(self.courier.id)
        
        self.assertFalse(result)

    def test_order_assign_courier_wrong_status(self):
        """測試 Order.assign_courier 方法 - 錯誤狀態"""
        self.order.status = 'created'
        self.order.save()
        
        result = self.order.assign_courier(self.courier.id)
        
        self.assertFalse(result)

    @patch('account.models.CourierUser.is_available')
    def test_order_assign_courier_out_of_range(self, mock_is_available):
        """測試 Order.assign_courier 方法 - 距離過遠"""
        mock_is_available.return_value = True
        self.order.status = 'accepted'
        self.order.save()
        
        with patch.object(self.restaurant, 'get_distance', return_value=3.0):
            result = self.order.assign_courier(self.courier.id)
        
        self.assertFalse(result)

    def test_order_can_be_assigned_true(self):
        """測試 Order.can_be_assigned 方法 - 可指派"""
        self.order.status = 'accepted'
        self.order.save()
        
        result = self.order.can_be_assigned()
        
        self.assertTrue(result)

    def test_order_can_be_assigned_false(self):
        """測試 Order.can_be_assigned 方法 - 不可指派"""
        self.order.status = 'created'
        self.order.save()
        
        result = self.order.can_be_assigned()
        
        self.assertFalse(result)

    def test_order_is_within_delivery_range_true(self):
        """測試 Order.is_within_delivery_range 方法 - 範圍內"""
        with patch.object(self.restaurant, 'get_distance', return_value=2.0):
            result = self.order.is_within_delivery_range(self.courier)
        
        self.assertTrue(result)

    def test_order_is_within_delivery_range_false(self):
        """測試 Order.is_within_delivery_range 方法 - 範圍外"""
        with patch.object(self.restaurant, 'get_distance', return_value=3.0):
            result = self.order.is_within_delivery_range(self.courier)
        
        self.assertFalse(result)

    @patch('account.models.CourierUser.objects.get')
    def test_order_get_available_orders_for_courier(self, mock_get_courier):
        """測試 Order.get_available_orders_for_courier 類方法"""
        mock_get_courier.return_value = self.courier
        
        # 創建一個 accepted 狀態的訂單
        accepted_order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Test Address',
            latitude=25.0340,
            longitude=121.5664,
            status='accepted',
            payment_method='cash',
            delivery_fee=80
        )
        
        # 創建一個非 accepted 狀態的訂單
        Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Test Address',
            latitude=25.0340,
            longitude=121.5664,
            status='created',
            payment_method='cash',
            delivery_fee=80
        )
        
        with patch.object(self.restaurant, 'get_distance', return_value=2.0):
            result = Order.get_available_orders_for_courier(self.courier.id)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], accepted_order.id)
        self.assertEqual(result[0]['customer_name'], self.customer.username)
        self.assertEqual(result[0]['restaurant'], self.restaurant.name)
        self.assertEqual(result[0]['fee'], 80)
        self.assertIn('restaurant_position', result[0])
        self.assertIn('customer_position', result[0])

    @patch('account.models.CustomerUser.objects.get')
    def test_order_get_latest_order_for_customer(self, mock_get_customer):
        """測試 Order.get_latest_order_for_customer 類方法"""
        mock_get_customer.return_value = self.customer
        
        # 創建多個訂單
        Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Old Address',
            status='created',
            payment_method='cash'
        )
        
        latest_order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Latest Address',
            status='accepted',
            payment_method='cash'
        )
        
        # 創建已完成訂單（應被排除）
        Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Done Address',
            status='done',
            payment_method='cash'
        )
        
        # 創建已拒絕訂單（應被排除）
        Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Rejected Address',
            status='rejected',
            payment_method='cash'
        )
        
        result = Order.get_latest_order_for_customer(self.customer.id)
        
        self.assertEqual(result.id, latest_order.id)

    @patch('account.models.CustomerUser.objects.get')
    def test_order_get_latest_order_for_customer_none(self, mock_get_customer):
        """測試 Order.get_latest_order_for_customer 類方法 - 無訂單"""
        mock_get_customer.return_value = self.customer
        
        # 刪除所有訂單
        Order.objects.all().delete()
        
        result = Order.get_latest_order_for_customer(self.customer.id)
        
        self.assertIsNone(result)


class OrderItemModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建客戶
        self.customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Customer Address'
        )
        
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678'
        )
        
        # 創建餐點
        self.food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Test Food',
            price=Decimal('250.00')
        )
        
        # 創建訂單
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Test Address',
            status='created',
            payment_method='cash'
        )
        
        # 創建訂單商品
        self.order_item = OrderItem.objects.create(
            order=self.order,
            food_item=self.food_item,
            quantity=3,
            unit_price=Decimal('250.00')
        )

    def test_order_item_str(self):
        """測試 OrderItem.__str__ 方法"""
        expected = f"3 x {self.food_item.name}"
        self.assertEqual(str(self.order_item), expected)

    def test_order_item_get_total_price(self):
        """測試 OrderItem.get_total_price 方法"""
        result = self.order_item.get_total_price()
        self.assertEqual(result, Decimal('750.00'))

    def test_order_item_get_total_price_decimal(self):
        """測試 OrderItem.get_total_price 方法 - 小數點計算"""
        self.order_item.unit_price = Decimal('10.50')
        self.order_item.quantity = 3
        
        result = self.order_item.get_total_price()
        
        self.assertEqual(result, Decimal('31.50'))


class OrderStatusTransitionDetailTest(TestCase):
    """測試每個具體的狀態轉換"""
    
    def setUp(self):
        # 創建客戶
        self.customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Customer Address'
        )
        
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678'
        )
        
        # 創建訂單
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='Test Address',
            status='created',
            payment_method='cash'
        )

    def test_created_to_accepted(self):
        """測試 created -> accepted 轉換"""
        self.order.status = 'created'
        self.order.save()
        
        result = self.order.change_status('accepted')
        
        self.assertTrue(result)
        self.assertEqual(self.order.status, 'accepted')

    def test_created_to_rejected(self):
        """測試 created -> rejected 轉換"""
        self.order.status = 'created'
        self.order.save()
        
        result = self.order.change_status('rejected')
        
        self.assertTrue(result)
        self.assertEqual(self.order.status, 'rejected')

    def test_accepted_to_assigned(self):
        """測試 accepted -> assigned 轉換"""
        self.order.status = 'accepted'
        self.order.save()
        
        result = self.order.change_status('assigned')
        
        self.assertTrue(result)
        self.assertEqual(self.order.status, 'assigned')

    def test_assigned_to_picked_up(self):
        """測試 assigned -> picked_up 轉換"""
        self.order.status = 'assigned'
        self.order.save()
        
        result = self.order.change_status('picked_up')
        
        self.assertTrue(result)
        self.assertEqual(self.order.status, 'picked_up')

    def test_picked_up_to_finish(self):
        """測試 picked_up -> finish 轉換"""
        self.order.status = 'picked_up'
        self.order.save()
        
        result = self.order.change_status('finish')
        
        self.assertTrue(result)
        self.assertEqual(self.order.status, 'finish')

    def test_finish_to_done(self):
        """測試 finish -> done 轉換"""
        self.order.status = 'finish'
        self.order.save()
        
        result = self.order.change_status('done')
        
        self.assertTrue(result)
        self.assertEqual(self.order.status, 'done')

    def test_done_no_transitions(self):
        """測試 done 狀態無法轉換"""
        self.order.status = 'done'
        self.order.save()
        
        for status in ['created', 'accepted', 'assigned', 'picked_up', 'finish', 'rejected']:
            result = self.order.change_status(status)
            self.assertFalse(result)
            self.assertEqual(self.order.status, 'done')

    def test_rejected_no_transitions(self):
        """測試 rejected 狀態無法轉換"""
        self.order.status = 'rejected'
        self.order.save()
        
        for status in ['created', 'accepted', 'assigned', 'picked_up', 'finish', 'done']:
            result = self.order.change_status(status)
            self.assertFalse(result)
            self.assertEqual(self.order.status, 'rejected')