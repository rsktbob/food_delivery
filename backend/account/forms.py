from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from account.models import BaseUser, CustomerProfile, VendorProfile, CourierProfile
from Restaurant.models import Restaurant
from order.models import Cart

# Base form with common fields and methods
class BaseRegisterForm(UserCreationForm):
    class Meta:
        model = BaseUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("The form is not valid!")
        
        user = super().save(commit=False)
        
        if commit:
            user.save()
        
        return user

class CustomerRegisterForm(BaseRegisterForm):
    address = forms.CharField(max_length=255, required=True)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'
        
        if commit:
            customer_profile = CustomerProfile(
                user=user,
                address=self.cleaned_data['address'],
            )
            user.save()
            customer_profile.save()
        
        return user

class VendorRegisterForm(BaseRegisterForm):
    restaurant_name = forms.CharField(max_length=100, required=True)
    restaurant_address = forms.CharField(max_length=255, required=True)
    restaurant_city = forms.CharField(max_length=255, required=True)
    restaurant_phone_number = forms.CharField(max_length=255, required=True)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor'
        
        if commit:
            vendor_profile = VendorProfile(user=user)
            user.save()
            vendor_profile.save()
            Restaurant.objects.create(
                owner=vendor_profile,
                name=self.cleaned_data['restaurant_name'],
                address=self.cleaned_data['restaurant_address'],
                city=self.cleaned_data['restaurant_city'],
                phone_number=self.cleaned_data['restaurant_phone_number'],
            )
        
        return user

class CourierRegisterForm(BaseRegisterForm):
    vehicle_type = forms.CharField(max_length=20, required=True)
    license_plate = forms.CharField(max_length=20, required=True)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'courier'
        
        if commit:
            courier_profile = CourierProfile(
                user=user,
                vehicle_type=self.cleaned_data['vehicle_type'],
                license_plate=self.cleaned_data['license_plate']
            )
            user.save()
            courier_profile.save()
        
        return user