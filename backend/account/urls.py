from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('api/register/', views.AccountController.register_user, name='register'),
    path('api/login/', views.AccountController.login_user, name='login'),
    path('api/courier-update-pos/', views.AccountController.courier_update_pos, name='courier-update-pos'),
]