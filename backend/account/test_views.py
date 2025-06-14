from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from unittest.mock import patch, Mock
from django.contrib.auth.models import User

from account.views import AccountController
from account.models import CourierUser, AuthenticationService
from account.factories import UserFactory


from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from unittest.mock import patch, Mock

from account.views import AccountController
from account.models import CourierUser, CustomerUser, VendorUser, AuthenticationService
from account.factories import UserFactory


class AccountControllerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        
        # 創建測試顧客
        self.customer = CustomerUser.objects.create_user(
            username='customer_user',
            email='customer@example.com',
            password='testpass123',
            user_type='customer',
            phone_number='1234567890',
            address='Customer Address'
        )
        
        # 創建測試快遞員
        self.courier = CourierUser.objects.create_user(
            username='courier_user',
            email='courier@example.com',
            password='testpass123',
            user_type='courier',
            phone_number='0987654321',
            vehicle_type='bicycle',
            license_plate='ABC123'
        )
        
        # 創建測試商家
        self.vendor = VendorUser.objects.create_user(
            username='vendor_user',
            email='vendor@example.com',
            password='testpass123',
            user_type='vendor',
            phone_number='5555555555'
        )

    def test_register_user_success(self):
        """測試 register_user - 成功註冊用戶"""
        request_data = {
            'user_type': 'customer',
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'newuser@example.com',
            'phone_number': '1234567890',
            'address': 'New Address'
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/register/', request_data, format='json')
        
        # Mock UserFactory
        mock_user = Mock()
        with patch('account.views.UserFactory') as mock_factory_class:
            mock_factory = Mock()
            mock_factory_class.return_value = mock_factory
            mock_factory.create_user.return_value = mock_user
            
            # 調用控制器方法
            response = AccountController.register_user(request)
            
            # 驗證 factory 調用
            mock_factory.create_user.assert_called_once_with(
                user_type='customer',
                username='newuser',
                email='newuser@example.com',
                password='newpass123',
                phone_number='1234567890',
                address='New Address',
                vehicle_type=None,
                license_plate=None,
                restaurant_name=None,
                restaurant_image=None,
                restaurant_address=None,
                restaurant_phone_number=None,
                restaurant_latitude=None,
                restaurant_longitude=None
            )
        
        # 驗證回應
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], '用戶註冊成功')

    def test_register_user_missing_required_fields(self):
        """測試 register_user - 缺少必要欄位"""
        request_data = {
            'username': 'newuser',
            'password': 'newpass123'
            # 缺少 email 和 user_type
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/register/', request_data, format='json')
        
        # 調用控制器方法
        response = AccountController.register_user(request)
        
        # 驗證回應
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], '請提供所有必要資訊')

    def test_register_user_with_courier_extra_fields(self):
        """測試 register_user - 快遞員註冊（包含額外欄位）"""
        request_data = {
            'user_type': 'courier',
            'username': 'courier_user',
            'password': 'courierpass123',
            'email': 'courier@example.com',
            'phone_number': '9876543210',
            'address': 'Courier Address',
            'vehicle_type': 'motorcycle',
            'license_plate': 'MOT456'
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/register/', request_data, format='json')
        
        # Mock UserFactory
        mock_user = Mock()
        with patch('account.views.UserFactory') as mock_factory_class:
            mock_factory = Mock()
            mock_factory_class.return_value = mock_factory
            mock_factory.create_user.return_value = mock_user
            
            # 調用控制器方法
            response = AccountController.register_user(request)
            
            # 驗證 factory 調用包含快遞員特定欄位
            mock_factory.create_user.assert_called_once_with(
                user_type='courier',
                username='courier_user',
                email='courier@example.com',
                password='courierpass123',
                phone_number='9876543210',
                address='Courier Address',
                vehicle_type='motorcycle',
                license_plate='MOT456',
                restaurant_name=None,
                restaurant_image=None,
                restaurant_address=None,
                restaurant_phone_number=None,
                restaurant_latitude=None,
                restaurant_longitude=None
            )
        
        # 驗證回應
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], '用戶註冊成功')

    def test_login_user_success(self):
        """測試 login_user - 成功登入"""
        request_data = {
            'username': 'customer_user',
            'password': 'testpass123'
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/login/', request_data, format='json')
        
        # Mock AuthenticationService 的靜態方法
        mock_user_data = {
            'id': self.customer.id,
            'username': 'customer_user',
            'email': 'customer@example.com',
            'user_type': 'customer',
            'address': 'Customer Address'
        }
        
        with patch('account.views.AuthenticationService.authenticate_user', return_value=self.customer) as mock_auth:
            with patch('account.views.AuthenticationService.get_user_profile_data', return_value=mock_user_data) as mock_profile:
                with patch('account.views.login') as mock_login:
                    
                    # 調用控制器方法
                    response = AccountController.login_user(request)
                    
                    # 驗證 AuthenticationService 調用
                    mock_auth.assert_called_once_with('customer_user', 'testpass123')
                    mock_profile.assert_called_once_with(self.customer)
                    
                    # 修正：使用 ANY 來匹配 request 物件類型
                    from unittest.mock import ANY
                    mock_login.assert_called_once_with(ANY, self.customer)
        
        # 驗證回應
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_user_data)

    def test_login_user_missing_credentials(self):
        """測試 login_user - 缺少登入資訊"""
        request_data = {
            'username': 'testuser'
            # 缺少 password
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/login/', request_data, format='json')
        
        # 調用控制器方法
        response = AccountController.login_user(request)
        
        # 驗證回應
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], '請提供用戶名和密碼')

    def test_login_user_invalid_credentials(self):
        """測試 login_user - 無效的登入資訊"""
        request_data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/login/', request_data, format='json')
        
        # Mock AuthenticationService 返回 None（認證失敗）
        with patch('account.views.AuthenticationService') as mock_auth_service:
            mock_auth_service.authenticate_user.return_value = None
            
            # 調用控制器方法
            response = AccountController.login_user(request)
            
            # 驗證 AuthenticationService 調用
            mock_auth_service.authenticate_user.assert_called_once_with('wronguser', 'wrongpass')
        
        # 驗證回應
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], '用戶名或密碼錯誤')

    def test_courier_update_pos_success(self):
        """測試 courier_update_pos - 成功更新位置"""
        request_data = {
            'user_id': self.courier.id,
            'pos': {
                'lat': 25.0330,
                'lng': 121.5654
            }
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/courier-update-pos/', request_data, format='json')
        force_authenticate(request, user=self.courier)
        
        # Mock CourierUser.objects.get 和 set_position
        with patch('account.views.CourierUser.objects.get', return_value=self.courier) as mock_get:
            with patch.object(self.courier, 'set_position') as mock_set_position:
                
                # 調用控制器方法
                response = AccountController.courier_update_pos(request)
                
                # 驗證 mock 調用
                mock_get.assert_called_once_with(id=self.courier.id)
                mock_set_position.assert_called_once_with(25.0330, 121.5654)
        
        # 驗證回應
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_courier_update_pos_courier_not_found(self):
        """測試 courier_update_pos - 快遞員不存在"""
        non_existent_id = 99999
        request_data = {
            'user_id': non_existent_id,
            'pos': {
                'lat': 25.0330,
                'lng': 121.5654
            }
        }
        
        # 創建 POST 請求（使用正確的 URL）
        request = self.factory.post('/api/courier-update-pos/', request_data, format='json')
        force_authenticate(request, user=self.courier)
        
        # Mock CourierUser.objects.get 拋出 DoesNotExist 異常
        with patch('account.views.CourierUser.objects.get', 
                   side_effect=CourierUser.DoesNotExist):
            
            # 驗證會拋出異常（因為原始程式碼沒有處理這個情況）
            with self.assertRaises(CourierUser.DoesNotExist):
                AccountController.courier_update_pos(request)