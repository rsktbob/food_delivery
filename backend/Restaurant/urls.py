from django.urls import path
from . import views

urlpatterns = [
    path('api/restaurants/vendor', views.RestaurantController.get_vendor_restaurant),
    path('api/restaurants/<int:restaurant_id>/food_items/', views.RestaurantController.list_food_items),
    path('api/food_category/', views.RestaurantController.lisr_food_categories),
    path('api/food_items/add', views.RestaurantController.add_food_item),
    path('api/food_items/<int:food_id>/delete', views.RestaurantController.delete_food_item),
    path('api/food_items/<int:food_id>/update', views.RestaurantController.update_food_item),
    path('api/restaurants', views.RestaurantController.list_restaurants),
    path('api/restaurants/<int:restaurant_id>/orders/', views.RestaurantController.list_restaurant_orders),
    path('api/categories/<str:food_category>/restaurants', views.RestaurantController.list_restaurants_by_category),
    path('api/restaurants/<int:restaurant_id>', views.RestaurantController.get_restaurant),
    path('api/restaurants/search/', views.RestaurantController.search_restaurants),
]