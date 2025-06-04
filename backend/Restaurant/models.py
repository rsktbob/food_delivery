from django.db import models
from account.models import VendorUser

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Food Categories"


class Restaurant(models.Model):
    owner = models.ForeignKey(VendorUser, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15)
    rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    image = models.ImageField(upload_to='restaurant_images/', default='restaurant_images/default_restaurant.jpg')
    category = models.ForeignKey(FoodCategory, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')
    
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    



# class CustomizationOption(models.Model):
#     OPTION_TYPE_CHOICES = (
#         ('single', 'Single Choice'),
#         ('multiple', 'Multiple Choice'),
#     )
    
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='customization_options')
#     name = models.CharField(max_length=100)
#     option_type = models.CharField(max_length=10, choices=OPTION_TYPE_CHOICES)
#     is_required = models.BooleanField(default=False)
    
#     def __str__(self):
#         return f"{self.name} - {self.menu_item.name}"

# class CustomizationChoice(models.Model):
#     option = models.ForeignKey(CustomizationOption, on_delete=models.CASCADE, related_name='choices')
#     name = models.CharField(max_length=100)
#     additional_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
#     def __str__(self):
#         return f"{self.name} (+${self.additional_price})"