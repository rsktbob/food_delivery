from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import math
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant
from .forms import *
from order.models import CartItem, Cart
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from urllib.parse import unquote
from order.serializer import OrderSerializer
from .serializer import *
from order.models import Order

    
class RestaurantController:

    @staticmethod
    @api_view(['GET'])
    def get_vendor_restaurant(request):
        user = request.user
        restaurant = user.restaurant
        serializer = RestaurantSerializer(restaurant,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['GET'])
    def get_restaurant(request, restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer = RestaurantSerializer(restaurant,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod      
    @api_view(['GET'])
    def search_restaurants(request):
        name_query = request.GET.get('name', '')
        restaurants = Restaurant.objects.filter(name__icontains=name_query)
        serializer = RestaurantSerializer(restaurants, many=True,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['GET'])
    def list_restaurants_by_category(request, food_category):
        decoded_category = unquote(food_category)
        restaurants = Restaurant.objects.filter(category__name=decoded_category)
        serializer = RestaurantSerializer(restaurants,  many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @staticmethod
    @api_view(['GET'])
    def list_restaurants(request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    @api_view(['GET'])
    def list_food_items(request, restaurant_id):
        items = FoodItem.objects.filter(restaurant_id=restaurant_id)
        serializer = FoodItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)
        
    @staticmethod
    @api_view(['GET'])
    def lisr_food_categories(request):
        items = FoodCategory.objects.all()
        serializer = RestaurantCategorySerializer(items, many=True, context={'request': request})
        return Response(serializer.data)
    
    @staticmethod
    @api_view(['GET'])
    def list_restaurant_orders(request, restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        orders = restaurant.get_orders()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def add_food_item(request):
        name = request.data.get('name')
        price = request.data.get('price')
        restaurant_id = request.data.get('restaurant')
        image = request.FILES.get('image')

        restaurant = Restaurant.objects.get(id=restaurant_id)
        restaurant.add_food_item(name=name, price=price, image=image)

        return Response({"message": "餐點新增成功"}, status=status.HTTP_201_CREATED)


    @staticmethod
    @api_view(['PATCH'])
    def update_food_item(request, food_id):
        name = request.data.get('name')
        price = request.data.get('price')
        image = request.FILES.get('image')

        food = FoodItem.objects.get(id=food_id)
        food.name = name
        food.price = price
        if image:
            food.image = image  # 僅在有提供時更新圖檔
        food.save()

        return Response({"message": "餐點修改成功"}, status=status.HTTP_201_CREATED)



    @staticmethod
    @api_view(['DELETE'])
    def delete_food_item(request, food_id):
        user = request.user
        vendor = VendorUser.objects.get(id=user.id)
        restaurnt = vendor.restaurant
        restaurnt.delete_food_item(food_id)
        return Response({"message": "餐點刪除成功"}, status=status.HTTP_201_CREATED)
