from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from urllib.parse import unquote

from .models import Restaurant, FoodItem, FoodCategory, RestaurantService
from .serializer import RestaurantSerializer, FoodItemSerializer, RestaurantCategorySerializer
from order.serializer import OrderSerializer

class RestaurantController:
    """
    Controller: 只處理 HTTP 請求和回應，委託給適當的模型或服務
    Low Coupling: 只依賴 Restaurant app 的模型和服務
    """

    @staticmethod
    @api_view(['GET'])
    def get_vendor_restaurant(request):
        """
        Controller: 委託給 RestaurantService 處理完整資訊查詢
        """
        user = request.user
        
        # 使用 FK 關係找到該 vendor 的餐廳
        try:
            restaurant = user.restaurant
            serializer = RestaurantSerializer(restaurant, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'error': '找不到餐廳'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(['GET'])
    def get_restaurant(request, restaurant_id):
        """
        Controller: 簡單的查詢，委託給 Restaurant
        """
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer = RestaurantSerializer(restaurant, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod      
    @api_view(['GET'])
    def search_restaurants(request):
        """
        Controller: 委託給 Restaurant 處理搜尋邏輯
        """
        name_query = request.GET.get('name', '')
        restaurants = Restaurant.search_by_name(name_query)
        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['GET'])
    def list_restaurants_by_category(request, food_category):
        """
        Controller: 委託給 Restaurant 處理分類查詢
        """
        decoded_category = unquote(food_category)
        restaurants = Restaurant.get_by_category(decoded_category)
        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @staticmethod
    @api_view(['GET'])
    def list_restaurants(request):
        """
        Controller: 委託給 Restaurant 處理列表查詢
        """
        restaurants = Restaurant.get_all_restaurants()
        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    @api_view(['GET'])
    def list_food_items(request, restaurant_id):
        """
        Controller: 委託給 FoodItem 處理查詢
        """
        items = FoodItem.get_by_restaurant(restaurant_id)
        serializer = FoodItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)
        
    @staticmethod
    @api_view(['GET'])
    def list_food_categories(request):
        """
        Controller: 委託給 FoodCategory 處理查詢
        """
        categories = FoodCategory.get_all_categories()
        serializer = RestaurantCategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)
    
    @staticmethod
    @api_view(['GET'])
    def list_restaurant_orders(request, restaurant_id):
        """
        Controller: 委託給 Restaurant 處理訂單查詢
        """
        restaurant = Restaurant.objects.get(id=restaurant_id)
        orders = restaurant.get_pending_orders()
        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def add_food_item(request):
        """
        Controller: 委託給 RestaurantService 處理餐點創建
        """
        restaurant_id = request.data.get('restaurant')
        food_data = {
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'image': request.FILES.get('image')
        }

        food_item = RestaurantService.create_food_item_for_restaurant(restaurant_id, food_data)
        return Response({"message": "餐點新增成功"}, status=status.HTTP_201_CREATED)

    @staticmethod
    @api_view(['PATCH'])
    def update_food_item(request, food_id):
        """
        Controller: 委託給 RestaurantService 處理餐點更新
        """
        # 獲取餐點所屬的餐廳
        food_item = FoodItem.objects.get(id=food_id)
        restaurant_id = food_item.restaurant.id
        
        food_data = {
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'image': request.FILES.get('image')
        }

        RestaurantService.update_food_item_for_restaurant(restaurant_id, food_id, food_data)
        return Response({"message": "餐點修改成功"}, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['DELETE'])
    def delete_food_item(request, food_id):
        """
        Controller: 委託給 RestaurantService 處理餐點刪除
        """
        # 驗證是否為該餐廳的擁有者
        user_id = request.user.id
        food_item = FoodItem.objects.get(id=food_id)
        restaurant = food_item.restaurant
        
        if restaurant.is_owned_by(user_id):
            RestaurantService.delete_food_item_for_restaurant(restaurant.id, food_id)
            return Response({"message": "餐點刪除成功"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "無權限刪除此餐點"}, status=status.HTTP_403_FORBIDDEN)
    
