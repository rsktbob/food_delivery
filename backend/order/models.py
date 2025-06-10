from django.db import models
from account.models import CourierUser, CustomerUser
from Restaurant.models import Restaurant, FoodItem
import math

class Cart(models.Model):
    customer = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name='cart')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer.username}'s Cart"
    
    def clear(self):
        self.cartitem_set.all().delete()
        self.restaurant = None
        self.save()
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def transfer_items_to_order(self, order):
        for item in self.items.all():
            order.add_item(
                food_item=item.food_item,
                quantity=item.quantity,
                unit_price=item.food_item.price
            )
            item.delete()

    def create_order(self, lat, lng, address, payment):
        order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address=address,
            latitude=lat,
            longitude=lng,
            status='created',
            payment_method=payment,
            total_price=0,   # 先給 0，等 add_item 後計算
            delivery_fee=80,  # 這裡可以改成計算或固定值
        )
        self.transfer_items_to_order(order)
        order.calculate_totals()

    def set_item_quantity(self, cart_item_id, quantity):
        cart_item = self.items.get(id=cart_item_id)
        cart_item.update_quantity(quantity)
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"
    
    def get_total_price(self):
        item_price = self.food_item.price
        # customizations_price = sum(c.choice.additional_price for c in self.cartitemcustomization_set.all())
        return item_price * self.quantity
    
    class Meta:
        unique_together = ('cart', 'food_item')  # 每位使用者對每項食物只能有一筆記錄

    def set_quantity(self, quantity):
        if quantity >= 1:
            self.quantity = quantity
            self.save()

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('created', 'Created'), # 這是顧客創建訂單時，order為created
        ('accepted', 'Accepted'),#餐廳接受
        ('assigned', 'Assigned'),#有外送員接單
        ('picked_up', 'Picked Up'),#外送員拿到餐點
        ('finish', 'Finish'),#外送員送到餐點
        ('Done', 'Done'),
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


    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    courier = models.ForeignKey(CourierUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    delivery_address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Created')
    payment_method = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

    def calculate_totals(self):
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        self.grand_total = self.total_price + self.delivery_fee
        self.save()
    
    def is_in_delivery_distance(self, lat, lng, distance):
        print(self.restaurant.get_distance(lat, lng))
        return self.restaurant.get_distance(lat, lng) < distance
    
    def change_status(self, new_status):
        if new_status in self.allowed_transitions.get(self.status, []):
            self.status = new_status
            self.save()
            return True
        else:
            return False
        
    def add_item(self, food_item, quantity, unit_price):
        self.items.create(food_item=food_item, quantity=quantity, unit_price=unit_price)

    def get_total_distance(self, lat, lng):
        return self.restaurant.get_distance(lat, lng) + self.restaurant.get_distance(self.latitude, self.longitude)
    
    def take_order(self, order_id):
        try:
            order = self.orders.get(id=order_id)
            order.change_status('assigned')
            order.save()
        except Exception as e:
            print(e)

# class CartItemCustomization(models.Model):
#     cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
#     choice = models.ForeignKey(CustomizationChoice, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.cart_item.menu_item.name} - {self.choice.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"
    
    def get_total_price(self):
        # customizations_price = sum(c.additional_price for c in self.orderitemcustomization_set.all())
        return self.unit_price * self.quantity

# class OrderItemCustomization(models.Model):
#     order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='customizations')
#     option_name = models.CharField(max_length=100)
#     choice_name = models.CharField(max_length=100)
#     additional_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
#     def __str__(self):
#         return f"{self.order_item.menu_item.name} - {self.choice_name}"