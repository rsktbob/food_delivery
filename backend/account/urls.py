from django.urls import path
from . import view

urlpatterns = [
    path('api/register/', view.register_user, name='register'),
    path('api/login/', view.login_user, name='login'),
]