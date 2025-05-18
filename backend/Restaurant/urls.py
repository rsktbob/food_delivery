from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/', views.RestaurantManegHandler.EnterRestaurant, name="restaurant"),
    path('restaurant/add_menu_item/<int:restaurant_id>/', views.RestaurantManegHandler.AddMenuItem, name="add_menu_item"),
    path('restaurant/add_cart_item/<int:menu_item_id>/', views.RestaurantManegHandler.AddCartItem, name="add_cart_item"),
    path('shopping_cart/', views.RestaurantManegHandler.EnterShoppingCart, name="enter_shopping_cart"),
    path('api/restaurant/', views.get_restaurant_info, name="restaurant"),
    path('api/menu_items/', views.get_menu_items, name="menu_items"),
]