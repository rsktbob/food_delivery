from django.db import models
from math import radians, sin, cos, sqrt, atan2

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Food Categories"
    
    @classmethod
    def get_all_categories(cls):
        """
        Information Expert: FoodCategory 最了解如何查詢所有分類
        """
        return cls.objects.all()
    
    def get_restaurants(self):
        """
        Information Expert: FoodCategory 最了解屬於自己的餐廳
        """
        return self.restaurants.all()


class Restaurant(models.Model):
    # 保持原有的 FK 關係，配合 factories.py
    owner = models.OneToOneField('account.VendorUser', on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15)
    rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    image = models.ImageField(upload_to='restaurant_images/', default='restaurant_images/default_restaurant.jpg')
    category = models.ForeignKey(FoodCategory, blank=True, null=True, on_delete=models.SET_NULL, related_name='restaurants')

    def __str__(self):
        return self.name
    
    def get_distance(self, lat, lng):
        """
        Information Expert: Restaurant 最了解如何計算到自己的距離
        """
        R = 6371  # 地球半徑，單位：公里
        dlat = radians(self.latitude - lat)
        dlon = radians(self.longitude - lng)
        
        a = sin(dlat / 2)**2 + cos(radians(lat)) * cos(radians(self.latitude)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c  # 單位：公里
    
    def add_food_item(self, name, price, image):
        """
        Creator: Restaurant 負責創建自己的餐點
        """
        return FoodItem.objects.create(
            name=name,
            price=price,
            restaurant=self,
            image=image
        )

    def update_food_item(self, food_id, name=None, price=None, image=None):
        """
        Information Expert: Restaurant 最了解如何更新自己的餐點
        """
        food_item = self.food_items.get(id=food_id)
        
        if name is not None:
            food_item.name = name
        if price is not None:
            food_item.price = price
        if image is not None:
            food_item.image = image
            
        food_item.save()
        return food_item

    def delete_food_item(self, food_id):
        """
        Information Expert: Restaurant 最了解如何刪除自己的餐點
        """
        food_item = self.food_items.get(id=food_id)
        food_item.delete()

    def get_orders(self, status_filter=None):
        """
        Information Expert: Restaurant 最了解自己的訂單
        """
        orders = self.orders.all()
        
        if status_filter:
            orders = orders.filter(status__in=status_filter)
            
        return orders.order_by('-id')
    
    def get_pending_orders(self):
        """
        Information Expert: Restaurant 最了解需要處理的訂單
        """
        return self.get_orders(['created', 'accepted'])
    
    def is_owned_by(self, user_id):
        """
        Information Expert: Restaurant 最了解自己的擁有者
        """
        return self.owner.id == user_id

    @classmethod
    def search_by_name(cls, name_query):
        """
        Information Expert: Restaurant 最了解如何搜尋餐廳
        """
        return cls.objects.filter(name__icontains=name_query)
    
    @classmethod
    def get_by_category(cls, category_name):
        """
        Information Expert: Restaurant 最了解如何按分類查詢
        """
        return cls.objects.filter(category__name=category_name)
    
    @classmethod
    def get_all_restaurants(cls):
        """
        Information Expert: Restaurant 最了解如何查詢所有餐廳
        """
        return cls.objects.all()
    
    @classmethod
    def get_restaurants_near_location(cls, lat, lng, max_distance=10):
        """
        Information Expert: Restaurant 最了解如何找附近的餐廳
        """
        nearby_restaurants = []
        for restaurant in cls.objects.all():
            if restaurant.latitude and restaurant.longitude:
                distance = restaurant.get_distance(lat, lng)
                if distance <= max_distance:
                    nearby_restaurants.append({
                        'restaurant': restaurant,
                        'distance': distance
                    })
        
        # 按距離排序
        nearby_restaurants.sort(key=lambda x: x['distance'])
        return [item['restaurant'] for item in nearby_restaurants]


class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='food_items/')
    
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    
    @classmethod
    def get_by_restaurant(cls, restaurant_id):
        """
        Information Expert: FoodItem 最了解如何按餐廳查詢
        """
        return cls.objects.filter(restaurant_id=restaurant_id)
    
    @classmethod
    def search_by_name(cls, name_query, restaurant_id=None):
        """
        Information Expert: FoodItem 最了解如何搜尋餐點
        """
        items = cls.objects.filter(name__icontains=name_query)
        if restaurant_id:
            items = items.filter(restaurant_id=restaurant_id)
        return items

# Restaurant Service - 處理複雜的業務邏輯
class RestaurantService:
    """
    Controller: 處理跨模型的複雜業務邏輯
    """
    
    @staticmethod
    def create_food_item_for_restaurant(restaurant_id, food_data):
        """
        Creator: 協調餐點創建流程
        """
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return restaurant.add_food_item(
            name=food_data['name'],
            price=food_data['price'],
            image=food_data.get('image')
        )
    
    @staticmethod
    def update_food_item_for_restaurant(restaurant_id, food_id, food_data):
        """
        Controller: 協調餐點更新流程
        """
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return restaurant.update_food_item(
            food_id=food_id,
            name=food_data.get('name'),
            price=food_data.get('price'),
            image=food_data.get('image')
        )
    
    @staticmethod
    def delete_food_item_for_restaurant(restaurant_id, food_id):
        """
        Controller: 協調餐點刪除流程
        """
        restaurant = Restaurant.objects.get(id=restaurant_id)
        restaurant.delete_food_item(food_id)