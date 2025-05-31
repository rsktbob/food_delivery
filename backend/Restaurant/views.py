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
from .serializer import FoodItemSerializer,RestaurantSerializer

# def calculate_distance(lat1, lon1, lat2, lon2):
#     # Haversine formula to calculate distance between two points
#     R = 6371  # Radius of Earth in km
#     dLat = math.radians(lat2 - lat1)
#     dLon = math.radians(lon2 - lon1)
#     a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#     distance = R * c
#     return distance

# def search_restaurant(request):
#     query = request.GET.get('q', '')
#     category = request.GET.get('category', '')
#     lat = request.GET.get('lat')
#     lon = request.GET.get('lon')
    
#     restaurants = Restaurant.objects.filter(is_active=True)
    
#     # Apply search filter
#     if query:
#         restaurants = restaurants.filter(
#             Q(name__icontains=query) | 
#             Q(cuisine_type__icontains=query) |
#             Q(menu_items__name__icontains=query)
#         ).distinct()
    
#     # Apply category filter
#     if category:
#         restaurants = restaurants.filter(cuisine_type=category)
    
#     # Calculate distance if coordinates provided
#     restaurant_list = []
#     if lat and lon:
#         try:
#             user_lat = float(lat)
#             user_lon = float(lon)
            
#             for rest in restaurants:
#                 distance = calculate_distance(user_lat, user_lon, rest.latitude, rest.longitude)
#                 if distance <= settings.MAX_DELIVERY_DISTANCE:
#                     restaurant_list.append({
#                         'id': rest.id,
#                         'name': rest.name,
#                         'cuisine_type': rest.cuisine_type,
#                         'rating': rest.rating,
#                         'distance': round(distance, 2)
#                     })
            
#             # Sort by distance
#             restaurant_list.sort(key=lambda x: x['distance'])
#         except (ValueError, TypeError):
#             pass
    
#     return JsonResponse({'restaurants': restaurant_list})

# def view_restaurant(request, restaurant_id):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
#     menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
    
#     # Group menu items by category
#     categories = {}
#     for item in menu_items:
#         category_name = item.category.name if item.category else "Other"
#         if category_name not in categories:
#             categories[category_name] = []
        
#         # Get customization options
#         customization_options = []
#         for option in CustomizationOption.objects.filter(menu_item=item):
#             choices = option.choices.all().values('id', 'name', 'additional_price')
#             customization_options.append({
#                 'id': option.id,
#                 'name': option.name,
#                 'type': option.option_type,
#                 'required': option.is_required,
#                 'choices': list(choices)
#             })
        
#         categories[category_name].append({
#             'id': item.id,
#             'name': item.name,
#             'description': item.description,
#             'price': float(item.price),
#             'image': item.image.url if item.image else None,
#             'customization_options': customization_options
#         })
    
#     response_data = {
#         'id': restaurant.id,
#         'name': restaurant.name,
#         'description': restaurant.description,
#         'cuisine_type': restaurant.cuisine_type,
#         'address': restaurant.address,
#         'rating': restaurant.rating,
#         'total_ratings': restaurant.total_ratings,
#         'categories': categories
#     }
    
#     return JsonResponse(response_data)

# @login_required
# def manage_menu(request, restaurant_id):
#     # Implementation for restaurant owners to manage their menu
#     pass


class RestaurantManegHandler:
    @classmethod
    def EnterRestaurant(cls, request):
        restaurant_id = request.GET.get('restaurant_id')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        menu_items = restaurant.menu_items.all()
        context = {'restaurant' : restaurant, "menu_items" : menu_items}
        return render(request, "Restaurant/restaurant.html", context)      
    
    @classmethod
    def AddMenuItem(cls, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        form = MenuItemForm(request.POST, request.FILES)

        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()

        menu_items = restaurant.menu_items.all()
        print(menu_items)
        context = {"menu_items" : menu_items}
        return render(request, "Restaurant/menu_items.html", context)
    
    @classmethod
    def AddCartItem(cls, request, menu_item_id):
        menu_item = FoodItem.objects.get(id=menu_item_id)
        restaurant = menu_item.restaurant
        customer = request.user.customer_profile

        cart = Cart.objects.filter(customer=customer, restaurant=restaurant).first()
        if cart == None:
            cart = Cart(customer=customer, restaurant=restaurant)
            cart.save()
        
        cart_item = CartItem(cart=cart, menu_item_id=menu_item_id)
        cart_item.save()
        return HttpResponse("成功點餐")
    
    @classmethod
    def EnterShoppingCart(cls, request):
        customer = request.user.customer_profile

        carts = Cart.objects.filter(customer=customer)
        context = {"carts" : carts}
        return render(request, "Restaurant/shopping_cart.html", context)
    

@api_view(['GET'])
def get_restaurant_by_vendor(request):
    user = request.user
    
    try:
        restaurant = Restaurant.objects.get(owner=user)
        serializer = RestaurantSerializer(restaurant,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Restaurant.DoesNotExist:
        return Response(
            {'error': '找不到該用戶的餐廳'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'服務器錯誤: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERRORP
        )

@api_view(['GET'])
def get_restaurant(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer = RestaurantSerializer(restaurant,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Restaurant.DoesNotExist:
        return Response(
            {'error': '找不到該用戶的餐廳'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'服務器錯誤: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERRORP
        )

    
@api_view(['GET'])
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def get_food_items(request, restaurant_id):
    items = FoodItem.objects.filter(restaurant_id=restaurant_id)
    serializer = FoodItemSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_food_category(request):
    items = FoodCategory.objects.values('id', 'name')  # QuerySet of dicts
    items_list = list(items)  # 轉成純 Python list
    return Response(items_list)

@api_view(['POST'])
def add_food_item(request):
    name = request.data.get('name')
    price = request.data.get('price')
    category_id = request.data.get('category')
    restaurant_id = request.data.get('restaurant')
    image = request.FILES.get('image')


    if not all([name, price, category_id, restaurant_id, image]):
        return Response({"error": "所有欄位皆為必填"}, status=status.HTTP_400_BAD_REQUEST)

    # 加入保存資料邏輯，例如：
    FoodItem.objects.create(
         name=name, price=price, category_id=category_id,
         restaurant_id=restaurant_id, image=image
     )

    return Response({"message": "餐點新增成功"}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_food_item(request, food_id):
    food = FoodItem.objects.get(id=food_id)
    food.delete()
    return Response({"message": "餐點刪除成功"}, status=status.HTTP_201_CREATED)
