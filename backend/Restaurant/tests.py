from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from unittest.mock import patch, MagicMock
from math import radians, sin, cos, sqrt, atan2

from Restaurant.models import FoodCategory, Restaurant, FoodItem, RestaurantService
from account.models import VendorUser
from order.models import Order


class FoodCategoryModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建測試圖片檔案
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )
        
        self.category = FoodCategory.objects.create(
            name='Test Category',
            image=self.test_image
        )

    def test_food_category_str(self):
        """測試 FoodCategory.__str__ 方法"""
        self.assertEqual(str(self.category), 'Test Category')

    def test_food_category_get_all_categories(self):
        """測試 FoodCategory.get_all_categories 類方法"""
        # 創建另一個分類
        other_image = SimpleUploadedFile(
            name='other_image.jpg',
            content=b'other_fake_image_content',
            content_type='image/jpeg'
        )
        FoodCategory.objects.create(name='Other Category', image=other_image)
        
        categories = FoodCategory.get_all_categories()
        
        self.assertEqual(categories.count(), 2)
        self.assertIn(self.category, categories)

    def test_food_category_get_restaurants_empty(self):
        """測試 FoodCategory.get_restaurants 方法 - 無餐廳"""
        restaurants = self.category.get_restaurants()
        self.assertEqual(restaurants.count(), 0)

    def test_food_category_get_restaurants_with_restaurants(self):
        """測試 FoodCategory.get_restaurants 方法 - 有餐廳"""
        # 創建餐廳老闆
        vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        restaurant = Restaurant.objects.create(
            owner=vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678',
            category=self.category
        )
        
        restaurants = self.category.get_restaurants()
        
        self.assertEqual(restaurants.count(), 1)
        self.assertIn(restaurant, restaurants)


class RestaurantModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建分類
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )
        self.category = FoodCategory.objects.create(
            name='Test Category',
            image=test_image
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            city='Test City',
            phone_number='0912345678',
            rating=4.5,
            total_ratings=10,
            category=self.category
        )

    def test_restaurant_str(self):
        """測試 Restaurant.__str__ 方法"""
        self.assertEqual(str(self.restaurant), 'Test Restaurant')

    def test_restaurant_get_distance(self):
        """測試 Restaurant.get_distance 方法"""
        # 使用實際的地理座標測試距離計算
        target_lat = 25.0340
        target_lng = 121.5664
        
        distance = self.restaurant.get_distance(target_lat, target_lng)
        
        # 檢查距離是否為正數且在合理範圍內
        self.assertGreater(distance, 0)
        self.assertLess(distance, 2)  # 應該很近

    def test_restaurant_get_distance_same_location(self):
        """測試 Restaurant.get_distance 方法 - 相同位置"""
        distance = self.restaurant.get_distance(
            self.restaurant.latitude, 
            self.restaurant.longitude
        )
        
        # 相同位置距離應該接近 0
        self.assertAlmostEqual(distance, 0, places=5)

    def test_restaurant_add_food_item(self):
        """測試 Restaurant.add_food_item 方法"""
        food_image = SimpleUploadedFile(
            name='food_image.jpg',
            content=b'fake_food_image_content',
            content_type='image/jpeg'
        )
        
        food_item = self.restaurant.add_food_item(
            name='Test Food',
            price=Decimal('150.00'),
            image=food_image
        )
        
        self.assertEqual(food_item.name, 'Test Food')
        self.assertEqual(food_item.price, Decimal('150.00'))
        self.assertEqual(food_item.restaurant, self.restaurant)

    def test_restaurant_update_food_item_all_fields(self):
        """測試 Restaurant.update_food_item 方法 - 更新所有欄位"""
        # 先創建一個餐點
        original_image = SimpleUploadedFile(
            name='original_image.jpg',
            content=b'original_image_content',
            content_type='image/jpeg'
        )
        food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Original Food',
            price=Decimal('100.00'),
            image=original_image
        )
        
        # 更新餐點
        new_image = SimpleUploadedFile(
            name='new_image.jpg',
            content=b'new_image_content',
            content_type='image/jpeg'
        )
        
        updated_food = self.restaurant.update_food_item(
            food_id=food_item.id,
            name='Updated Food',
            price=Decimal('200.00'),
            image=new_image
        )
        
        self.assertEqual(updated_food.name, 'Updated Food')
        self.assertEqual(updated_food.price, Decimal('200.00'))
        self.assertEqual(updated_food.id, food_item.id)

    def test_restaurant_update_food_item_partial(self):
        """測試 Restaurant.update_food_item 方法 - 部分更新"""
        # 先創建一個餐點
        food_image = SimpleUploadedFile(
            name='food_image.jpg',
            content=b'fake_food_image_content',
            content_type='image/jpeg'
        )
        food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Original Food',
            price=Decimal('100.00'),
            image=food_image
        )
        
        # 只更新名稱
        updated_food = self.restaurant.update_food_item(
            food_id=food_item.id,
            name='Updated Food Name'
        )
        
        self.assertEqual(updated_food.name, 'Updated Food Name')
        self.assertEqual(updated_food.price, Decimal('100.00'))  # 價格保持不變

    def test_restaurant_delete_food_item(self):
        """測試 Restaurant.delete_food_item 方法"""
        # 先創建一個餐點
        food_image = SimpleUploadedFile(
            name='food_image.jpg',
            content=b'fake_food_image_content',
            content_type='image/jpeg'
        )
        food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Food to Delete',
            price=Decimal('100.00'),
            image=food_image
        )
        
        food_id = food_item.id
        
        # 刪除餐點
        self.restaurant.delete_food_item(food_id)
        
        # 檢查餐點是否已被刪除
        self.assertFalse(FoodItem.objects.filter(id=food_id).exists())

    def test_restaurant_get_orders_no_filter(self):
        """測試 Restaurant.get_orders 方法 - 無篩選"""
        from account.models import CustomerUser
        
        # 創建客戶
        customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Address'
        )
        
        # 創建訂單
        order1 = Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 1',
            status='created',
            payment_method='cash'
        )
        
        order2 = Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 2',
            status='accepted',
            payment_method='cash'
        )
        
        orders = self.restaurant.get_orders()
        
        # 檢查訂單數量和順序（應該按 id 降序）
        self.assertEqual(orders.count(), 2)
        self.assertEqual(list(orders), [order2, order1])

    def test_restaurant_get_orders_with_filter(self):
        """測試 Restaurant.get_orders 方法 - 有篩選"""
        from account.models import CustomerUser
        
        # 創建客戶
        customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Address'
        )
        
        # 創建不同狀態的訂單
        Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 1',
            status='created',
            payment_method='cash'
        )
        
        accepted_order = Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 2',
            status='accepted',
            payment_method='cash'
        )
        
        Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 3',
            status='done',
            payment_method='cash'
        )
        
        # 篩選特定狀態
        orders = self.restaurant.get_orders(['accepted', 'assigned'])
        
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first(), accepted_order)

    def test_restaurant_get_pending_orders(self):
        """測試 Restaurant.get_pending_orders 方法"""
        from account.models import CustomerUser
        
        # 創建客戶
        customer = CustomerUser.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='testpass123',
            user_type='customer',
            address='Test Address'
        )
        
        # 創建不同狀態的訂單
        created_order = Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 1',
            status='created',
            payment_method='cash'
        )
        
        accepted_order = Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 2',
            status='accepted',
            payment_method='cash'
        )
        
        Order.objects.create(
            customer=customer,
            restaurant=self.restaurant,
            delivery_address='Address 3',
            status='done',
            payment_method='cash'
        )
        
        pending_orders = self.restaurant.get_pending_orders()
        
        self.assertEqual(pending_orders.count(), 2)
        self.assertIn(created_order, pending_orders)
        self.assertIn(accepted_order, pending_orders)

    def test_restaurant_is_owned_by_true(self):
        """測試 Restaurant.is_owned_by 方法 - 是擁有者"""
        result = self.restaurant.is_owned_by(self.vendor.id)
        self.assertTrue(result)

    def test_restaurant_is_owned_by_false(self):
        """測試 Restaurant.is_owned_by 方法 - 不是擁有者"""
        # 創建另一個使用者
        other_vendor = VendorUser.objects.create_user(
            username='othervendor',
            email='other@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        result = self.restaurant.is_owned_by(other_vendor.id)
        self.assertFalse(result)

    def test_restaurant_search_by_name(self):
        """測試 Restaurant.search_by_name 類方法"""
        # 創建另一個餐廳
        other_vendor = VendorUser.objects.create_user(
            username='othervendor',
            email='other@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        Restaurant.objects.create(
            owner=other_vendor,
            name='Pizza Palace',
            address='Other Address',
            latitude=25.0340,
            longitude=121.5664,
            phone_number='0912345679'
        )
        
        # 搜尋包含 "Test" 的餐廳
        results = Restaurant.search_by_name('Test')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.restaurant, results)
        
        # 搜尋包含 "Pizza" 的餐廳
        results = Restaurant.search_by_name('Pizza')
        self.assertEqual(results.count(), 1)

    def test_restaurant_get_by_category(self):
        """測試 Restaurant.get_by_category 類方法"""
        # 創建另一個分類和餐廳
        other_image = SimpleUploadedFile(
            name='other_image.jpg',
            content=b'other_fake_image_content',
            content_type='image/jpeg'
        )
        other_category = FoodCategory.objects.create(
            name='Other Category',
            image=other_image
        )
        
        other_vendor = VendorUser.objects.create_user(
            username='othervendor',
            email='other@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        Restaurant.objects.create(
            owner=other_vendor,
            name='Other Restaurant',
            address='Other Address',
            latitude=25.0340,
            longitude=121.5664,
            phone_number='0912345679',
            category=other_category
        )
        
        # 按分類搜尋
        results = Restaurant.get_by_category('Test Category')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.restaurant, results)

    def test_restaurant_get_all_restaurants(self):
        """測試 Restaurant.get_all_restaurants 類方法"""
        # 創建另一個餐廳
        other_vendor = VendorUser.objects.create_user(
            username='othervendor',
            email='other@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        Restaurant.objects.create(
            owner=other_vendor,
            name='Other Restaurant',
            address='Other Address',
            latitude=25.0340,
            longitude=121.5664,
            phone_number='0912345679'
        )
        
        restaurants = Restaurant.get_all_restaurants()
        self.assertEqual(restaurants.count(), 2)

    def test_restaurant_get_restaurants_near_location(self):
        """測試 Restaurant.get_restaurants_near_location 類方法"""
        # 創建一個遠距離的餐廳
        far_vendor = VendorUser.objects.create_user(
            username='farvendor',
            email='far@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        far_restaurant = Restaurant.objects.create(
            owner=far_vendor,
            name='Far Restaurant',
            address='Far Address',
            latitude=24.0000,  # 較遠的位置
            longitude=120.0000,
            phone_number='0912345679'
        )
        
        # 創建一個近距離的餐廳
        near_vendor = VendorUser.objects.create_user(
            username='nearvendor',
            email='near@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        near_restaurant = Restaurant.objects.create(
            owner=near_vendor,
            name='Near Restaurant',
            address='Near Address',
            latitude=25.0340,  # 較近的位置
            longitude=121.5664,
            phone_number='0912345680'
        )
        
        # 搜尋附近餐廳
        nearby = Restaurant.get_restaurants_near_location(
            lat=25.0330,
            lng=121.5654,
            max_distance=5
        )
        
        # 應該包含原本的餐廳和近距離餐廳，但不包含遠距離餐廳
        self.assertIn(self.restaurant, nearby)
        self.assertIn(near_restaurant, nearby)
        # 檢查是否按距離排序（近的在前面）
        self.assertEqual(nearby[0], self.restaurant)  # 最近的應該是原本的餐廳

    def test_restaurant_get_restaurants_near_location_no_coordinates(self):
        """測試 Restaurant.get_restaurants_near_location 類方法 - 無座標餐廳"""
        # 創建一個沒有座標的餐廳
        no_coord_vendor = VendorUser.objects.create_user(
            username='nocoordvendor',
            email='nocoord@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        Restaurant.objects.create(
            owner=no_coord_vendor,
            name='No Coord Restaurant',
            address='No Coord Address',
            latitude=None,
            longitude=None,
            phone_number='0912345679'
        )
        
        nearby = Restaurant.get_restaurants_near_location(
            lat=25.0330,
            lng=121.5654,
            max_distance=10
        )
        
        # 只應該包含有座標的餐廳
        self.assertEqual(len(nearby), 1)
        self.assertIn(self.restaurant, nearby)


class FoodItemModelTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678'
        )
        
        # 創建餐點
        food_image = SimpleUploadedFile(
            name='food_image.jpg',
            content=b'fake_food_image_content',
            content_type='image/jpeg'
        )
        
        self.food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Test Food',
            price=Decimal('150.00'),
            image=food_image
        )

    def test_food_item_str(self):
        """測試 FoodItem.__str__ 方法"""
        expected = f"Test Food - {self.restaurant.name}"
        self.assertEqual(str(self.food_item), expected)

    def test_food_item_get_by_restaurant(self):
        """測試 FoodItem.get_by_restaurant 類方法"""
        # 創建另一個餐廳和餐點
        other_vendor = VendorUser.objects.create_user(
            username='othervendor',
            email='other@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        other_restaurant = Restaurant.objects.create(
            owner=other_vendor,
            name='Other Restaurant',
            address='Other Address',
            latitude=25.0340,
            longitude=121.5664,
            phone_number='0912345679'
        )
        
        other_image = SimpleUploadedFile(
            name='other_food_image.jpg',
            content=b'other_fake_food_image_content',
            content_type='image/jpeg'
        )
        
        FoodItem.objects.create(
            restaurant=other_restaurant,
            name='Other Food',
            price=Decimal('200.00'),
            image=other_image
        )
        
        # 取得特定餐廳的餐點
        items = FoodItem.get_by_restaurant(self.restaurant.id)
        
        self.assertEqual(items.count(), 1)
        self.assertIn(self.food_item, items)

    def test_food_item_search_by_name_no_restaurant(self):
        """測試 FoodItem.search_by_name 類方法 - 不指定餐廳"""
        # 創建另一個餐點
        another_image = SimpleUploadedFile(
            name='another_food_image.jpg',
            content=b'another_fake_food_image_content',
            content_type='image/jpeg'
        )
        
        FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Pizza Food',
            price=Decimal('180.00'),
            image=another_image
        )
        
        # 搜尋包含 "Test" 的餐點
        results = FoodItem.search_by_name('Test')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.food_item, results)
        
        # 搜尋包含 "Food" 的餐點
        results = FoodItem.search_by_name('Food')
        self.assertEqual(results.count(), 2)

    def test_food_item_search_by_name_with_restaurant(self):
        """測試 FoodItem.search_by_name 類方法 - 指定餐廳"""
        # 創建另一個餐廳和餐點
        other_vendor = VendorUser.objects.create_user(
            username='othervendor',
            email='other@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        other_restaurant = Restaurant.objects.create(
            owner=other_vendor,
            name='Other Restaurant',
            address='Other Address',
            latitude=25.0340,
            longitude=121.5664,
            phone_number='0912345679'
        )
        
        other_image = SimpleUploadedFile(
            name='other_food_image.jpg',
            content=b'other_fake_food_image_content',
            content_type='image/jpeg'
        )
        
        FoodItem.objects.create(
            restaurant=other_restaurant,
            name='Test Food in Other Restaurant',
            price=Decimal('200.00'),
            image=other_image
        )
        
        # 在特定餐廳搜尋
        results = FoodItem.search_by_name('Test', restaurant_id=self.restaurant.id)
        
        self.assertEqual(results.count(), 1)
        self.assertIn(self.food_item, results)


class RestaurantServiceTest(TestCase):
    def setUp(self):
        """測試資料設定"""
        # 創建餐廳老闆
        self.vendor = VendorUser.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # 創建餐廳
        self.restaurant = Restaurant.objects.create(
            owner=self.vendor,
            name='Test Restaurant',
            address='Test Address',
            latitude=25.0330,
            longitude=121.5654,
            phone_number='0912345678'
        )

    def test_restaurant_service_create_food_item_for_restaurant(self):
        """測試 RestaurantService.create_food_item_for_restaurant 靜態方法"""
        food_image = SimpleUploadedFile(
            name='food_image.jpg',
            content=b'fake_food_image_content',
            content_type='image/jpeg'
        )
        
        food_data = {
            'name': 'Service Created Food',
            'price': Decimal('250.00'),
            'image': food_image
        }
        
        food_item = RestaurantService.create_food_item_for_restaurant(
            self.restaurant.id,
            food_data
        )
        
        self.assertEqual(food_item.name, 'Service Created Food')
        self.assertEqual(food_item.price, Decimal('250.00'))
        self.assertEqual(food_item.restaurant, self.restaurant)

    def test_restaurant_service_update_food_item_for_restaurant(self):
        """測試 RestaurantService.update_food_item_for_restaurant 靜態方法"""
        # 先創建一個餐點
        original_image = SimpleUploadedFile(
            name='original_image.jpg',
            content=b'original_image_content',
            content_type='image/jpeg'
        )
        
        food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Original Food',
            price=Decimal('100.00'),
            image=original_image
        )
        
        # 更新餐點
        new_image = SimpleUploadedFile(
            name='new_image.jpg',
            content=b'new_image_content',
            content_type='image/jpeg'
        )
        
        food_data = {
            'name': 'Updated Food',
            'price': Decimal('300.00'),
            'image': new_image
        }
        
        updated_food = RestaurantService.update_food_item_for_restaurant(
            self.restaurant.id,
            food_item.id,
            food_data
        )
        
        self.assertEqual(updated_food.name, 'Updated Food')
        self.assertEqual(updated_food.price, Decimal('300.00'))
        self.assertEqual(updated_food.id, food_item.id)

    def test_restaurant_service_delete_food_item_for_restaurant(self):
        """測試 RestaurantService.delete_food_item_for_restaurant 靜態方法"""
        # 先創建一個餐點
        food_image = SimpleUploadedFile(
            name='food_image.jpg',
            content=b'fake_food_image_content',
            content_type='image/jpeg'
        )
        
        food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            name='Food to Delete',
            price=Decimal('100.00'),
            image=food_image
        )
        
        food_id = food_item.id
        
        # 刪除餐點
        RestaurantService.delete_food_item_for_restaurant(
            self.restaurant.id,
            food_id
        )
        
        # 檢查餐點是否已被刪除
        self.assertFalse(FoodItem.objects.filter(id=food_id).exists())