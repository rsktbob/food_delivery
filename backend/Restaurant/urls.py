from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/', views.RestaurantManegHandler.EnterRestaurant, name="restaurant"),
    path('restaurant/add_menu_item/<int:restaurant_id>/', views.RestaurantManegHandler.AddMenuItem, name="add_menu_item"),
    path('restaurant/add_cart_item/<int:menu_item_id>/', views.RestaurantManegHandler.AddCartItem, name="add_cart_item"),
    path('shopping_cart/', views.RestaurantManegHandler.EnterShoppingCart, name="enter_shopping_cart"),
    path('api/restaurants/vendor', views.get_restaurant_by_vendor),
    path('api/restaurants/<int:restaurant_id>/food_items/', views.get_food_items),
    path('api/food_category/', views.get_food_category),
    path('api/food_items/add', views.add_food_item),
    path('api/food_items/<int:food_id>/delete', views.delete_food_item),
    path('api/restaurants', views.get_restaurants),
    path('api/restaurants/<int:restaurant_id>/orders/', views.get_restaurant_orders),
    path('api/categories/<str:food_category>/restaurants', views.get_restaurants_by_category),
    path('api/restaurants/<int:restaurant_id>', views.get_restaurant),
    path('api/restaurants/search/', views.serach_restaurants),
]