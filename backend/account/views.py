from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View 
from account.forms import CustomerRegisterForm, VendorRegisterForm, CourierRegisterForm

class RegisterView(View):
    user_type = None  # 透過 URL 傳入的參數

    def get(self, request, user_type):
        if user_type == 'customer':
            form = CustomerRegisterForm()
        elif user_type == 'vendor':
            form = VendorRegisterForm()
        elif user_type == 'courier':
            form = CourierRegisterForm()
        
        context = {'form' : form}
        return render(request, 'account/register.html', context)

    def post(self, request, user_type):
        if user_type == 'customer':
            form = CustomerRegisterForm(request.POST)
        elif user_type == 'vendor':
            form = VendorRegisterForm(request.POST)
        elif user_type == 'courier':
            form = CourierRegisterForm(request.POST)
        else:
            return redirect('register')

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            context = {'form' : form}
            return render(request, 'account/register.html', context)

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    
    def form_valid(self, form):
        # First execute parent login logic
        super().form_valid(form)
        return redirect('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Login failed. Please check your username and password.')
        return super().form_invalid(form)