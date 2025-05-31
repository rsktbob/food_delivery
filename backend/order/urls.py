from django.urls import path
from . import views

urlpatterns = [
    # path('check-vendor-orders/', views.OrderManageHandler.checkVendorOrder, name='check_vendor_orders'),
    # path('accept-vendor-order/', views.OrderManageHandler.acceptVendorOrder, name='accept_vendor_order'),
    # path('create_order/<int:restaurant_id>/', views.OrderManageHandler.createOrder, name="create_order"),
    # path('order_mange/', views.OrderManageHandler.enterOrderManagePage, name="enter_order_mange_page"),
    path('api/courier-take-orders/', views.courierTakeOrder, name='courier-take-orders'),
    path('api/courier-check-orders/', views.courierCheckOrder, name='courier-check-orders'),
    path('api/courier-pick-up-meals/', views.courierPickUpMeal, name='courier-pick-up-meals'),
    path('api/courier-finish-orders/', views.courierFinishOrder, name='courier-finish-orders'),
]