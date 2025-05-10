from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import *

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
            # 根據用戶類型創建對應的個人資料
            if user_type == 'customer':
                address = request.data.get('address', '')
                
                CustomerUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    user_type="customer",
                    phone_number=phone_number,
                    address=address
                )
            
            elif user_type == 'courier':
                vehicle_type = request.data.get('vehicle_type', '')
                license_plate = request.data.get('license_plate', '')
                
                CourierUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    user_type="customer",
                    phone_number=phone_number,
                    vehicle_type=vehicle_type,
                    license_plate=license_plate
                )

            elif user_type == 'vendor':
                VendorUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    user_type="vendor",
                    phone_number=phone_number
                )
            
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
        
        print(isinstance(user, CustomerUser))
        # 根據用戶類型添加額外資訊
        if isinstance(user, CustomerUser):
            user_data['address'] = user.address
        elif isinstance(user, CourierUser):
            user_data['rating'] = user.rating
            user_data['vehicle_type'] = user.vehicle_type
            user_data['license_plate'] = user.license_plate
        elif isinstance(user, VendorUser):
            pass
        
        return Response(user_data)
    else:
        return Response(
            {'error': '用戶名或密碼錯誤'},
            status=status.HTTP_401_UNAUTHORIZED
        )