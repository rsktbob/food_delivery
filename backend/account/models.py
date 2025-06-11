from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class BaseUser(AbstractUser):
    user_type = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, blank=True)

class CustomerUser(BaseUser):
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Customer: {self.username}"
    
    def get_latest_order(self):
        """
        Information Expert: CustomerUser 最了解自己的訂單
        """
        from order.models import Order
        return Order.get_latest_order_for_customer(self.id)
    
    def create_cart(self, restaurant_id):
        """
        Creator: CustomerUser 負責為自己創建購物車
        Controller: 協調跨 app 操作
        """
        from order.models import Cart
        
        # 刪除現有購物車（確保一次只能從一家餐廳點餐）
        Cart.objects.filter(customer_id=self.id).delete()
        
        return Cart.objects.create(customer_id=self.id, restaurant_id=restaurant_id)

    def has_cart(self):
        """
        Information Expert: CustomerUser 最了解自己是否有購物車
        """
        from order.models import Cart
        return Cart.objects.filter(customer_id=self.id).exists()
    
    def get_cart(self):
        """
        Information Expert: CustomerUser 最了解如何取得自己的購物車
        """
        from order.models import Cart
        try:
            return Cart.objects.get(customer_id=self.id)
        except Cart.DoesNotExist:
            return None
    
    def get_order_history(self):
        """
        Information Expert: CustomerUser 最了解自己的訂單歷史
        """
        from order.models import Order
        return Order.objects.filter(customer_id=self.id).order_by('-id')
    
    def create_order_from_cart(self, delivery_info):
        """
        Controller: CustomerUser 協調購物車到訂單的轉換
        """
        cart = self.get_cart()
        if cart:
            return cart.create_order(delivery_info)
        return None

class CourierUser(BaseUser):
    rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    vehicle_type = models.CharField(max_length=20, blank=True)
    license_plate = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Courier: {self.username}"
    
    def set_position(self, lat, lng):
        """
        Information Expert: CourierUser 最了解如何設定自己的位置
        """
        self.latitude = lat
        self.longitude = lng
        self.save()

    def is_available(self):
        """
        Information Expert: CourierUser 最了解自己是否可以接單
        """
        from order.models import Order
        active_orders = Order.objects.filter(
            courier_id=self.id,
            status__in=['assigned', 'picked_up']
        )
        return active_orders.count() == 0

class VendorUser(BaseUser):
    def __str__(self):
        return f"Vendor: {self.username}"
    
    def has_restaurant(self):
        """
        Information Expert: VendorUser 最了解自己是否有餐廳
        """
        return hasattr(self, 'restaurant')

# User Authentication Service
class AuthenticationService:
    """
    Controller: 處理認證相關的業務邏輯
    """
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Information Expert: AuthenticationService 最了解認證邏輯
        """
        from django.contrib.auth import authenticate
        return authenticate(username=username, password=password)
    
    @staticmethod
    def get_user_profile_data(user):
        """
        Information Expert: AuthenticationService 最了解如何組裝使用者資料
        """
        base_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
            'phone_number': user.phone_number
        }
        
        # 根據使用者類型添加額外資訊
        if user.user_type == 'customer':
            customer = CustomerUser.objects.get(id=user.id)
            base_data['address'] = customer.address
            
        elif user.user_type == 'courier':
            courier = CourierUser.objects.get(id=user.id)
            base_data.update({
                'rating': courier.rating,
                'vehicle_type': courier.vehicle_type,
                'license_plate': courier.license_plate
            })
            
        elif user.user_type == 'vendor':
            vendor = VendorUser.objects.get(id=user.id)
            if vendor.has_restaurant():
                base_data['restaurant_id'] = vendor.restaurant.id
        
        return base_data