# from django.db import models
# from account.models import User, CourierProfile
# from Restaurant.models import Restaurant
# from order.models import Order

# class RestaurantRating(models.Model):
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ratings')
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='restaurant_rating')
#     rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#     review = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('customer', 'order')
    
#     def __str__(self):
#         return f"{self.restaurant.name} - {self.rating}/5"
    
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         # Update restaurant's average rating
#         restaurant = self.restaurant
#         ratings = RestaurantRating.objects.filter(restaurant=restaurant)
#         total_ratings = ratings.count()
#         avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        
#         restaurant.rating = avg_rating
#         restaurant.total_ratings = total_ratings
#         restaurant.save()

# class CourierRating(models.Model):
#     courier = models.ForeignKey(CourierProfile, on_delete=models.CASCADE, related_name='ratings')
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='courier_rating')
#     rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#     review = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('customer', 'order')
    
#     def __str__(self):
#         return f"{self.courier.user.username} - {self.rating}/5"
    
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         # Update courier's average rating
#         courier = self.courier
#         ratings = CourierRating.objects.filter(courier=courier)
#         total_ratings = ratings.count()
#         avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        
#         courier.rating = avg_rating
#         courier.total_ratings = total_ratings
#         courier.save()