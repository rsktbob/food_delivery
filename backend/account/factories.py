from .models import *
from Restaurant.models import Restaurant

class UserFactory:
    def create_user(self, user_type, username, email, password, phone_number, **extra_fields):
        if user_type == 'customer':
            address = extra_fields.get('address', '')
            return CustomerUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type="customer",
                phone_number=phone_number,
                address=address
            )
        elif user_type == 'courier':
            vehicle_type = extra_fields.get('vehicle_type', '')
            license_plate = extra_fields.get('license_plate', '')
            return CourierUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type="courier",
                phone_number=phone_number,
                vehicle_type=vehicle_type,
                license_plate=license_plate
            )
        elif user_type == 'vendor':
            restaurant_name = extra_fields.get('restaurant_name', '')
            restaurant_image = extra_fields.get('restaurant_image', None)
            restaurant_address = extra_fields.get('restaurant_address', None)
            restaurant_phone_number = extra_fields.get('restaurant_phone_number', None)
            restaurant_latitude = extra_fields.get('restaurant_latitude', None)
            restaurant_longitude = extra_fields.get('restaurant_longitude', None)

            user = VendorUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type="vendor",
                phone_number=phone_number
            )
            Restaurant.objects.create(
                owner=user,
                name=restaurant_name,
                address=restaurant_address,
                phone_number=restaurant_phone_number,
                image=restaurant_image,
                latitude=restaurant_latitude,
                longitude=restaurant_longitude
            )
            return user