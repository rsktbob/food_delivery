from django.urls import path
from . import views

urlpatterns = [
    path('api/courier-take-orders/', views.courierTakeOrder),
    path('api/courier-check-orders/', views.courierCheckOrder),
    path('api/restaurants/<int:restaurant_id>/cart/add', views.add_to_cart),
    path('api/cart_items', views.get_cart_items),
    path('api/cart_items/<int:cart_item_id>/delete', views.delete_cart_items),
    path('api/courier-take-orders/', views.courierTakeOrder, name='courier-take-orders'),
    path('api/courier-check-orders/', views.courierCheckOrder, name='courier-check-orders'),
    path('api/courier-pick-up-meals/', views.courierPickUpMeal, name='courier-pick-up-meals'),
    path('api/courier-finish-orders/', views.courierFinishOrder, name='courier-finish-orders'),
]