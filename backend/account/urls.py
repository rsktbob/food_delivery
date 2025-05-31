from django.urls import path
from . import view

urlpatterns = [
    path('api/register/', view.register_user, name='register'),
    path('api/login/', view.login_user, name='login'),
    path('api/courier-update-pos/', view.CourierUpdatePos, name='courier-update-pos'),
]