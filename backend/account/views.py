from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login

from .models import AuthenticationService, CourierUser
from .factories import UserFactory


class AccountController:
    """
    Controller: 只處理 HTTP 請求和回應，委託給適當的服務或模型
    Low Coupling: 只依賴 account app 的模型和服務
    """

    @staticmethod
    @api_view(['POST'])
    def register_user(request):
        """
        Controller: 委託給 UserFactory 處理使用者創建
        """
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
        
        # 提取額外欄位
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
        
        # 委託給 Factory 創建使用者
        factory = UserFactory()
        user = factory.create_user(
            user_type=user_type,
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            **extra_fields
        )
        
        return Response(
            {'success': '用戶註冊成功'},
            status=status.HTTP_201_CREATED
        )
        
    @staticmethod
    @api_view(['POST'])
    def login_user(request):
        """
        Controller: 委託給 AuthenticationService 處理登入邏輯
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': '請提供用戶名和密碼'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 委託給認證服務驗證使用者
        user = AuthenticationService.authenticate_user(username, password)
        
        if not user:
            return Response(
                {'error': '用戶名或密碼錯誤'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)
        
        # 委託給認證服務組裝使用者資料
        user_data = AuthenticationService.get_user_profile_data(user)
        
        return Response(user_data)

    @staticmethod
    @api_view(['POST'])
    def courier_update_pos(request):
        """
        Controller: 委託給 CourierUser 處理位置更新
        """
        user_id = request.data.get('user_id')
        pos = request.data.get('pos')
        lat = pos.get('lat')
        lng = pos.get('lng')

        courier = CourierUser.objects.get(id=user_id)
        courier.set_position(lat, lng)
        
        return Response(status=status.HTTP_200_OK)