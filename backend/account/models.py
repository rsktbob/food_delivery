from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class BaseUser(AbstractUser):
    user_type = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, blank=True)

class CustomerUser(BaseUser):
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Cusotmer: {self.username}"
    
    def get_latest_order(self):
        order = self.orders.exclude(status__in=['Done', 'Rejected']).first()
        return order
    
    def create_cart(self, restaurant):
        from order.models import Cart
        
        if hasattr(self, 'cart'):
            self.cart.delete()
        Cart.objects.create(customer=self, restaurant=restaurant)

    def has_cart(self):
        try:
            return self.cart is not None
        except AttributeError:
            return False
                    

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
        self.latitude = lat
        self.longitude = lng
        self.save()

    def take_order(self, order_id):
        order = self.orders.get(id=order_id)
        order.change_status('Assigned')
        order.save()   


class VendorUser(BaseUser):
    def __str__(self):
        return f"Vendor: {self.username}"

# class CustomerProfile(models.Model):
#     user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='customer_profile')
#     address = models.CharField(max_length=255)
    
#     def __str__(self):
#         return f"Customer: {self.user.username}"
    
# class CourierProfile(models.Model):
#     user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='courier_profile')
#     rating = models.FloatField(default=0)
#     total_ratings = models.IntegerField(default=0)
#     vehicle_type = models.CharField(max_length=20, blank=True)
#     license_plate = models.CharField(max_length=20, blank=True)
    
#     def __str__(self):
#         return f"Courier: {self.user.username}"

# class VendorProfile(models.Model):
#     user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='vendor_profile')
    
#     def __str__(self):
#         return f"Vendor: {self.user.username}"