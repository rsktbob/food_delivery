from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from unittest.mock import patch, Mock, MagicMock
from decimal import Decimal

from .views import RestaurantController
from .models import Restaurant, FoodItem, FoodCategory
from .serializers import RestaurantSerializer, FoodItemSerializer, RestaurantCategorySerializer
from order.serializers import OrderSerializer
from user.factories import UserFactory


class RestaurantControllerTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 使用 APIRequestFactory
        self.factory = APIRequestFactory()
        self.user_factory = UserFactory()
        
        # 使用 UserFactory 創建用戶
        self.vendor_user = self.user_factory.create_user(
            user_type='vendor',
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            phone_number='0912345680',
            restaurant_name='Test Restaurant',
            restaurant_address='Test Address',
            restaurant_phone_number='0912345681',
            restaurant_latitude=25.0330,
            restaurant_longitude=121.5654
        )
        
        self.customer_user = self.user_factory.create_user(
            user_type='customer',
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            phone_number='0912345678',
            address='Test Customer Address'
        )
        
        # 取得餐廳
        self.restaurant = Restaurant.objects.get(owner=self.vendor_user)
        
        # 創建測試食物分類
        self.food_category = FoodCategory.objects.create(
            name='中式料理',
            description='傳統中式料理'
        )
        
        # 創建測試餐點
        self.food_item = FoodItem.objects.create(
            name='牛肉麵',
            price=Decimal('150.00'),
            restaurant=self.restaurant
        )

    def test_get_vendor_restaurant_success(self):
        """測試 get_vendor_restaurant - 成功獲取餐廳資訊"""
        request = self.factory.get('/api/vendor/restaurant/')
        force_authenticate(request, user=self.vendor_user)
        
        expected_data = {
            'id': self.restaurant.id,
            'name': 'Test Restaurant',
            'address': 'Test Address'
        }
        
        with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
            mock_serializer_instance = MagicMock()
            mock_serializer_instance.data = expected_data
            mock_serializer.return_value = mock_serializer_instance
            
            response = RestaurantController.get_vendor_restaurant(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_vendor_restaurant_not_found(self):
        """測試 get_vendor_restaurant - 找不到餐廳"""
        request = self.factory.get('/api/vendor/restaurant/')
        force_authenticate(request, user=self.customer_user)
        
        # Mock AttributeError when accessing restaurant
        with patch.object(self.customer_user, 'restaurant', side_effect=AttributeError):
            response = RestaurantController.get_vendor_restaurant(request)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], '找不到餐廳')

    def test_get_restaurant_success(self):
        """測試 get_restaurant - 成功獲取特定餐廳"""
        request = self.factory.get(f'/api/restaurants/{self.restaurant.id}/')
        
        expected_data = {
            'id': self.restaurant.id,
            'name': 'Test Restaurant',
            'address': 'Test Address'
        }
        
        with patch('Restaurant.views.Restaurant.objects.get', return_value=self.restaurant):
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.get_restaurant(request, self.restaurant.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_search_restaurants_success(self):
        """測試 search_restaurants - 成功搜尋餐廳"""
        request = self.factory.get('/api/restaurants/search/?name=測試')
        
        expected_data = [{
            'id': self.restaurant.id,
            'name': 'Test Restaurant',
            'address': 'Test Address'
        }]
        
        with patch('Restaurant.views.Restaurant.search_by_name', return_value=[self.restaurant]):
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.search_restaurants(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_search_restaurants_empty_query(self):
        """測試 search_restaurants - 空搜尋關鍵字"""
        request = self.factory.get('/api/restaurants/search/')
        
        with patch('Restaurant.views.Restaurant.search_by_name', return_value=[self.restaurant]) as mock_search:
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = []
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.search_restaurants(request)
        
        mock_search.assert_called_once_with('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_restaurants_no_results(self):
        """測試 search_restaurants - 無搜尋結果"""
        request = self.factory.get('/api/restaurants/search/?name=不存在的餐廳')
        
        with patch('Restaurant.views.Restaurant.search_by_name', return_value=[]):
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = []
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.search_restaurants(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_restaurants_by_category_success(self):
        """測試 list_restaurants_by_category - 成功按分類列出餐廳"""
        request = self.factory.get('/api/restaurants/category/中式料理/')
        
        expected_data = [{
            'id': self.restaurant.id,
            'name': 'Test Restaurant',
            'category': '中式料理'
        }]
        
        with patch('Restaurant.views.Restaurant.get_by_category', return_value=[self.restaurant]) as mock_get_by_category:
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.list_restaurants_by_category(request, '中式料理')
        
        mock_get_by_category.assert_called_once_with('中式料理')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_restaurants_by_category_url_encoded(self):
        """測試 list_restaurants_by_category - URL 編碼的分類名稱"""
        request = self.factory.get('/api/restaurants/category/%E4%B8%AD%E5%BC%8F%E6%96%99%E7%90%86/')
        
        with patch('Restaurant.views.Restaurant.get_by_category', return_value=[self.restaurant]) as mock_get_by_category:
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = []
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.list_restaurants_by_category(request, '%E4%B8%AD%E5%BC%8F%E6%96%99%E7%90%86')
        
        mock_get_by_category.assert_called_once_with('中式料理')  # URL decode 後的結果
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_restaurants_by_category_no_results(self):
        """測試 list_restaurants_by_category - 無結果"""
        request = self.factory.get('/api/restaurants/category/不存在分類/')
        
        with patch('Restaurant.views.Restaurant.get_by_category', return_value=[]):
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = []
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.list_restaurants_by_category(request, '不存在分類')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_restaurants_success(self):
        """測試 list_restaurants - 成功列出所有餐廳"""
        request = self.factory.get('/api/restaurants/')
        
        expected_data = [{
            'id': self.restaurant.id,
            'name': 'Test Restaurant',
            'address': 'Test Address'
        }]
        
        with patch('Restaurant.views.Restaurant.get_all_restaurants', return_value=[self.restaurant]) as mock_get_all:
            with patch('Restaurant.views.RestaurantSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.list_restaurants(request)
        
        mock_get_all.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_food_items_success(self):
        """測試 list_food_items - 成功列出餐廳餐點"""
        request = self.factory.get(f'/api/restaurants/{self.restaurant.id}/foods/')
        
        expected_data = [{
            'id': self.food_item.id,
            'name': '牛肉麵',
            'price': '150.00',
            'restaurant': self.restaurant.id
        }]
        
        with patch('Restaurant.views.FoodItem.get_by_restaurant', return_value=[self.food_item]) as mock_get_by_restaurant:
            with patch('Restaurant.views.FoodItemSerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.list_food_items(request, self.restaurant.id)
        
        mock_get_by_restaurant.assert_called_once_with(self.restaurant.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_food_categories_success(self):
        """測試 list_food_categories - 成功列出所有食物分類"""
        request = self.factory.get('/api/food-categories/')
        
        expected_data = [{
            'id': self.food_category.id,
            'name': '中式料理',
            'description': '傳統中式料理'
        }]
        
        with patch('Restaurant.views.FoodCategory.get_all_categories', return_value=[self.food_category]) as mock_get_all_categories:
            with patch('Restaurant.views.RestaurantCategorySerializer') as mock_serializer:
                mock_serializer_instance = MagicMock()
                mock_serializer_instance.data = expected_data
                mock_serializer.return_value = mock_serializer_instance
                
                response = RestaurantController.list_food_categories(request)
        
        mock_get_all_categories.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_restaurant_orders_success(self):
        """測試 list_restaurant_orders - 成功列出餐廳訂單"""
        request = self.factory.get(f'/api/restaurants/{self.restaurant.id}/orders/')
        
        mock_orders = [MagicMock(), MagicMock()]
        expected_data = [{'id': 1, 'status': 'pending'}, {'id': 2, 'status': 'pending'}]
        
        with patch('Restaurant.views.Restaurant.objects.get', return_value=self.restaurant):
            with patch.object(self.restaurant, 'get_pending_orders', return_value=mock_orders):
                with patch('Restaurant.views.OrderSerializer') as mock_serializer:
                    mock_serializer_instance = MagicMock()
                    mock_serializer_instance.data = expected_data
                    mock_serializer.return_value = mock_serializer_instance
                    
                    response = RestaurantController.list_restaurant_orders(request, self.restaurant.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_add_food_item_success(self):
        """測試 add_food_item - 成功新增餐點"""
        # 創建模擬圖片檔案
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        request_data = {
            'restaurant': self.restaurant.id,
            'name': '新餐點',
            'price': 200.00
        }
        
        request = self.factory.post('/api/food-items/', request_data)
        request._files = {'image': image_file}
        
        with patch('Restaurant.views.RestaurantService.create_food_item_for_restaurant', return_value=self.food_item) as mock_create:
            response = RestaurantController.add_food_item(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], '餐點新增成功')
        
        # 驗證 service 被正確調用
        expected_food_data = {
            'name': '新餐點',
            'price': 200.00,
            'image': image_file
        }
        mock_create.assert_called_once_with(self.restaurant.id, expected_food_data)

    def test_add_food_item_without_image(self):
        """測試 add_food_item - 沒有圖片"""
        request_data = {
            'restaurant': self.restaurant.id,
            'name': '無圖餐點',
            'price': 100.00
        }
        
        request = self.factory.post('/api/food-items/', request_data)
        
        with patch('Restaurant.views.RestaurantService.create_food_item_for_restaurant', return_value=self.food_item) as mock_create:
            response = RestaurantController.add_food_item(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 驗證傳遞的資料包含 None 圖片
        expected_food_data = {
            'name': '無圖餐點',
            'price': 100.00,
            'image': None
        }
        mock_create.assert_called_once_with(self.restaurant.id, expected_food_data)

    def test_update_food_item_success(self):
        """測試 update_food_item - 成功更新餐點"""
        image_file = SimpleUploadedFile(
            "updated_image.jpg",
            b"updated fake image content",
            content_type="image/jpeg"
        )
        
        request_data = {
            'name': '更新餐點',
            'price': 250.00
        }
        
        request = self.factory.patch(f'/api/food-items/{self.food_item.id}/', request_data)
        request._files = {'image': image_file}
        
        with patch('Restaurant.views.FoodItem.objects.get', return_value=self.food_item):
            with patch('Restaurant.views.RestaurantService.update_food_item_for_restaurant') as mock_update:
                response = RestaurantController.update_food_item(request, self.food_item.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '餐點修改成功')
        
        # 驗證 service 被正確調用
        expected_food_data = {
            'name': '更新餐點',
            'price': 250.00,
            'image': image_file
        }
        mock_update.assert_called_once_with(self.restaurant.id, self.food_item.id, expected_food_data)

    def test_delete_food_item_success(self):
        """測試 delete_food_item - 成功刪除餐點"""
        request = self.factory.delete(f'/api/food-items/{self.food_item.id}/')
        force_authenticate(request, user=self.vendor_user)
        
        with patch('Restaurant.views.FoodItem.objects.get', return_value=self.food_item):
            with patch.object(self.restaurant, 'is_owned_by', return_value=True) as mock_is_owned:
                with patch('Restaurant.views.RestaurantService.delete_food_item_for_restaurant') as mock_delete:
                    response = RestaurantController.delete_food_item(request, self.food_item.id)
        
        mock_is_owned.assert_called_once_with(self.vendor_user.id)
        mock_delete.assert_called_once_with(self.restaurant.id, self.food_item.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '餐點刪除成功')

    def test_delete_food_item_permission_denied(self):
        """測試 delete_food_item - 權限不足"""
        request = self.factory.delete(f'/api/food-items/{self.food_item.id}/')
        force_authenticate(request, user=self.customer_user)
        
        with patch('Restaurant.views.FoodItem.objects.get', return_value=self.food_item):
            with patch.object(self.restaurant, 'is_owned_by', return_value=False) as mock_is_owned:
                response = RestaurantController.delete_food_item(request, self.food_item.id)
        
        mock_is_owned.assert_called_once_with(self.customer_user.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], '無權限刪除此餐點')