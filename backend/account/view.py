from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import BaseUser, CustomerProfile, CourierProfile, VendorProfile

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
    
    # 檢查用戶名是否已存在
    if BaseUser.objects.filter(username=username).exists():
        return Response(
            {'error': '用戶名已被使用'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        with transaction.atomic():
            # 創建基本用戶
            user = BaseUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                phone_number=phone_number
            )
            
            # 根據用戶類型創建對應的個人資料
            if user_type == 'customer':
                address = request.data.get('address', '')
                CustomerProfile.objects.create(user=user, address=address)
            elif user_type == 'courier':
                vehicle_type = request.data.get('vehicle_type', '')
                license_plate = request.data.get('license_plate', '')
                CourierProfile.objects.create(
                    user=user,
                    vehicle_type=vehicle_type,
                    license_plate=license_plate
                )
            elif user_type == 'vendor':
                VendorProfile.objects.create(user=user)
            
        return Response(
            {'success': '用戶註冊成功'},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'error': f'註冊失敗: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

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
    
    if user is not None:
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
        if user.is_customer():
            user_data['profile'] = {
                'address': user.customer_profile.address
            }
        elif user.is_courier():
            user_data['profile'] = {
                'rating': user.courier_profile.rating,
                'vehicle_type': user.courier_profile.vehicle_type,
                'license_plate': user.courier_profile.license_plate
            }
        elif user.is_vendor():
            user_data['profile'] = {}  # 廠商可能沒有額外欄位
        
        return Response(user_data)
    else:
        return Response(
            {'error': '用戶名或密碼錯誤'},
            status=status.HTTP_401_UNAUTHORIZED
        )