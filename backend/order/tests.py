from django.test import TestCase
from account.models import CustomerUser, CourierUser, VendorUser
from Restaurant.models import Restaurant, FoodItem
from .models import Cart, CartItem, Order, OrderItem

class OrderSystemTest(TestCase):
    def setUp(self):
        self.customer = CustomerUser.objects.create_user(username='test_customer', password='pass', user_type='customer')
        self.vendor = VendorUser.objects.create_user(username='test_vendor', password='pass', user_type='vendor')
        self.courier = CourierUser.objects.create_user(username='test_courier', password='pass', user_type='courier')

        self.restaurant = Restaurant.objects.create(name="Test Restaurant", owner=self.vendor)
        self.food = FoodItem.objects.create(name="Test Food", price=100, restaurant=self.restaurant)
        self.cart = Cart.objects.create(customer=self.customer, restaurant=self.restaurant)

    def test_add_item_to_cart(self):
        # 在這裡寫測試加入商品到購物車的邏輯
        self.cart.items.create(food_item=self.food, quantity=2)
        self.assertEqual(self.cart.items.count(), 1)
        self.assertEqual(self.cart.items.first().quantity, 2)

    def test_create_order_from_cart(self):
        order = Order.objects.create(customer=self.customer, restaurant=self.restaurant)
        # 複製購物車裡的商品到訂單
        for item in self.cart.items.all():
            order.items.create(food_item=item.food_item, quantity=item.quantity)
        self.assertEqual(order.items.count(), self.cart.items.count())

    def test_order_status_transition(self):
        order = Order.objects.create(customer=self.customer, restaurant=self.restaurant, status='pending')
        order.change_status('accepted')
        self.assertEqual(order.status, 'accepted')
        order.change_status('assigned')
        self.assertEqual(order.status, 'assigned')
        order.change_status('picked_up')
        self.assertEqual(order.status, 'picked_up')