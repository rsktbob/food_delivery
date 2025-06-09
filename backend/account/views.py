from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import *
from Restaurant.models import Restaurant
from .factories import UserFactory

class AccountController:

    @staticmethod
    @api_view(['POST'])
    def register_user(request):
        user_type = request.data.get('user_type')
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number', '')

        # 基本驗證
        if not username or not password or not email or not user_type:
            return Response(
                {'error': '請提供所有必要資訊'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        extra_fields = {
            'address': request.data.get('address'),
            'vehicle_type': request.data.get('vehicle_type'),
            'license_plate': request.data.get('license_plate'),
            'restaurant_name': request.data.get('restaurant_name'),
            'restaurant_image': request.data.get('restaurant_image'),
            'restaurant_address': request.data.get('restaurant_address'),
            'restaurant_phone_number': request.data.get('restaurant_phone_number'),
            'restaurant_latitude': request.data.get('restaurant_latitude'),
            'restaurant_longitude': request.data.get('restaurant_longitude'),
        }
        
        try:
            factory = UserFactory()
            factory.create_user(user_type=user_type, username=username, email=email, password=password, phone_number=phone_number, **extra_fields)          
                
            return Response(
                {'success': '用戶註冊成功'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': f'註冊失敗: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @staticmethod
    @api_view(['POST'])
    def login_user(request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': '請提供用戶名和密碼'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({'error': '用戶名或密碼錯誤'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        
        # 獲取用戶角色相關信息
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
            'phone_number': user.phone_number
        }
        
        # 根據用戶類型添加額外資訊
        if user.user_type == 'customer':
            customer = CustomerUser.objects.get(id=user.id)
            user_data['address'] = customer.address
        elif user.user_type == 'courier':
            courier = CourierUser.objects.get(id=user.id)
            user_data['rating'] = courier.rating
            user_data['vehicle_type'] = courier.vehicle_type
            user_data['license_plate'] = courier.license_plate
        elif user.user_type == 'vendor':
            vendor = VendorUser.objects.get(id=user.id)
            user_data['restaurant_id'] = vendor.restaurant.id

        return Response(user_data)

    @staticmethod
    @api_view(['POST'])
    def courier_update_pos(request):
        user_id = request.data.get('user_id')
        
        pos = request.data.get('pos')
        lat = pos.get('lat')
        lng = pos.get('lng')

        print(user_id, request.user.id)
        courier = CourierUser.objects.get(id=user_id)
        courier.set_position(lat, lng)
        return Response(status=status.HTTP_200_OK)