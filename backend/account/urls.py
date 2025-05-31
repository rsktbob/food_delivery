from django.urls import path
from . import view
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('api/register/', view.register_user, name='register'),
    path('api/login/', view.login_user, name='login'),
    path('api/courier-update-pos/', view.CourierUpdatePos, name='courier-update-pos'),
]