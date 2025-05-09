from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('hello/', views.hello, name="hello"),
    path('order/<int:id>/', views.order, name="order"),
]