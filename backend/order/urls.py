from django.urls import path
from . import views

urlpatterns = [
    path('api/courier-take-orders/', views.OrderController.courier_take_order),
    path('api/restaurants/<int:restaurant_id>/cart/add', views.OrderController.add_to_cart),
    path('api/cart', views.OrderController.list_cart_items),
    path('api/cart/<int:cart_item_id>/delete', views.OrderController.delete_cart_items),
    path('api/cart/<int:cart_item_id>/update', views.OrderController.update_cart_item_quantity),
    path('api/orders/<int:order_id>/status/', views.OrderController.update_order_status),
    path('api/courier-take-orders/', views.OrderController.courier_take_order),
    path('api/courier-check-orders/', views.OrderController.list_available_orders_for_courier),
    path('api/courier-pick-up-meals/', views.OrderController. courier_pick_up_meal),
    path('api/courier-finish-orders/', views.OrderController.courier_finish_Order),
    path('api/create-orders/', views.OrderController.create_order),
    path('api/customer-get-order/', views.OrderController.customer_get_order),
    path('api/customer-done-order/', views.OrderController.mark_order_done),
]