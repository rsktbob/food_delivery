from django.db import models
import math

class Cart(models.Model):
    customer = models.OneToOneField('account.CustomerUser', on_delete=models.CASCADE, related_name='cart')
    restaurant = models.ForeignKey('Restaurant.Restaurant', on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def add_item(self, food_item_id, quantity):
        """
        Information Expert: Cart 最了解如何管理自己的商品
        Creator: Cart 負責創建 CartItem
        """
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            food_item_id=food_item_id
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
    
    def set_item_quantity(self, cart_item_id, quantity):
        """
        Information Expert: Cart 負責管理自己的商品數量
        """
        cart_item = self.items.get(id=cart_item_id)
        cart_item.set_quantity(quantity)
    
    def clear_items(self):
        """清空購物車商品"""
        self.items.all().delete()
    
    def create_order(self, delivery_info):
        """
        Creator: Cart 負責創建訂單並轉移商品
        Information Expert: Cart 最了解自己的內容
        """
        order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address=delivery_info['address'],
            latitude=delivery_info['lat'],
            longitude=delivery_info['lng'],
            status='created',
            payment_method=delivery_info['payment'],
            total_price=0,
            delivery_fee=80,
        )
        
        # 轉移商品到訂單
        for item in self.items.all():
            order.add_item(
                food_item=item.food_item,
                quantity=item.quantity,
                unit_price=item.food_item.price
            )
        
        order.calculate_totals()
        self.clear_items()
        return order

    @classmethod
    def get_or_create_for_customer(cls, customer_id, restaurant_id):
        """
        Creator: 負責購物車的創建邏輯
        """
        from account.models import CustomerUser
        from Restaurant.models import Restaurant
        
        customer = CustomerUser.objects.get(id=customer_id)
        restaurant = Restaurant.objects.get(id=restaurant_id)
        
        # 刪除其他餐廳的購物車（一次只能從一家餐廳點餐）
        cls.objects.filter(customer=customer).exclude(restaurant=restaurant).delete()
        
        cart, created = cls.objects.get_or_create(
            customer=customer,
            restaurant=restaurant
        )
        return cart

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    food_item = models.ForeignKey('Restaurant.FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"
    
    def get_total_price(self):
        """
        Information Expert: CartItem 最了解自己的總價計算
        """
        return self.food_item.price * self.quantity
    
    def set_quantity(self, quantity):
        """
        Information Expert: CartItem 最了解如何設定自己的數量
        """
        if quantity >= 1:
            self.quantity = quantity
            self.save()
    
    class Meta:
        unique_together = ('cart', 'food_item')

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('created', 'Created'),
        ('accepted', 'Accepted'),
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('finish', 'Finish'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
    )

    allowed_transitions = {
        'created': ['accepted', 'rejected'],
        'accepted': ['assigned'],
        'assigned': ['picked_up'],
        'picked_up': ['finish'],
        'finish': ['done'],
        'done': [],
        'rejected': [],
    }

    customer = models.ForeignKey('account.CustomerUser', on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey('Restaurant.Restaurant', on_delete=models.CASCADE, related_name='orders')
    courier = models.ForeignKey('account.CourierUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    delivery_address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    payment_method = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"

    def calculate_totals(self):
        """
        Information Expert: Order 最了解如何計算自己的總價
        """
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        self.grand_total = self.total_price + self.delivery_fee
        self.save()
    
    def change_status(self, new_status):
        """
        Information Expert: Order 最了解自己的狀態轉換規則
        """
        if new_status in self.allowed_transitions.get(self.status, []):
            self.status = new_status
            self.save()
            return True
        return False
    
    def add_item(self, food_item, quantity, unit_price):
        """
        Creator: Order 負責創建 OrderItem
        """
        self.items.create(
            food_item=food_item,
            quantity=quantity,
            unit_price=unit_price
        )

    def assign_courier(self, courier_id):
        """
        Information Expert: Order 最了解指派邏輯
        Controller: 協調跨 app 的操作
        """
        if not self.can_be_assigned():
            return False
        
        from account.models import CourierUser
        courier = CourierUser.objects.get(id=courier_id)
        
        if not courier.is_available():
            return False
            
        if not self.is_within_delivery_range(courier):
            return False
            
        self.courier = courier
        return self.change_status('assigned')
    
    def can_be_assigned(self):
        """Information Expert: Order 最了解自己能否被指派"""
        return self.status == 'accepted'
    
    def is_within_delivery_range(self, courier):
        """檢查配送距離 - 使用 FK 關係"""
        total_distance = (
            self.restaurant.get_distance(courier.latitude, courier.longitude) +
            self.restaurant.get_distance(self.latitude, self.longitude)
        )
        return total_distance <= 5

    @classmethod
    def get_available_orders_for_courier(cls, courier_id):
        """
        Information Expert: Order 最了解可接單的邏輯
        """
        from account.models import CourierUser
        courier = CourierUser.objects.get(id=courier_id)
        
        orders = cls.objects.filter(status='accepted')
        available_orders = []
        
        for order in orders:
            if order.is_within_delivery_range(courier):
                total_distance = (
                    order.restaurant.get_distance(courier.latitude, courier.longitude) +
                    order.restaurant.get_distance(order.latitude, order.longitude)
                )
                
                order_data = {
                    'id': order.id,
                    'customer_name': order.customer.username,
                    'restaurant': order.restaurant.name,
                    'distance': round(total_distance, 2),
                    'fee': order.delivery_fee,
                    'restaurant_position': {
                        'lat': float(order.restaurant.latitude),
                        'lng': float(order.restaurant.longitude)
                    },
                    'customer_position': {
                        'lat': float(order.latitude),
                        'lng': float(order.longitude)
                    }
                }
                available_orders.append(order_data)
        
        return available_orders
    

    @classmethod
    def get_latest_order_for_customer(cls, customer_id):
        """
        Information Expert: Order 最了解查詢邏輯
        """
        from account.models import CustomerUser
        customer = CustomerUser.objects.get(id=customer_id)
        return cls.objects.filter(
            customer=customer
        ).exclude(
            status__in=['done', 'rejected']
        ).last()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey('Restaurant.FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"
    
    def get_total_price(self):
        """
        Information Expert: OrderItem 最了解自己的總價計算
        """
        return self.unit_price * self.quantity