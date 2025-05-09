from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path('login/', views.CustomLoginView.as_view(template_name="account/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('register/<str:user_type>/', views.RegisterView.as_view(), name="register"),
]