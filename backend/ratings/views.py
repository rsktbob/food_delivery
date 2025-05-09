# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
# import json
# from .models import RestaurantRating, CourierRating
# from order.models import Order

# @login_required
# @require_POST
# def rate_restaurant(request, order_id):
#     try:
#         data = json.loads(request.body)
#         rating = data.get('rating')
#         review = data.get('review', '')
        
#         if not rating or not 1 <= int(rating) <= 5:
#             return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
        
#         # Get the order and verify ownership
#         order = get_object_or_404(Order, id=order_id)
#         if order.customer != request.user:
#             return JsonResponse({'error': 'Not authorized to rate this order'}, status=403)
        
#         if order.status != 'delivered':
#             return JsonResponse({'error': 'Cannot rate an order that is not delivered'}, status=400)
        
#         # Check if already rated
#         if hasattr(order, 'restaurant_rating'):
#             return JsonResponse({'error': 'Restaurant already rated for this order'}, status=400)
        
#         # Create the rating
#         rating_obj = RestaurantRating.objects.create(
#             restaurant=order.restaurant,
#             customer=request.user,
#             order=order,
#             rating=rating,
#             review=review
#         )
        
#         return JsonResponse({
#             'success': True,
#             'rating': rating_obj.rating,
#             'restaurant_avg_rating': order.restaurant.rating
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

# @login_required
# @require_POST
# def rate_courier(request, order_id):
#     try:
#         data = json.loads(request.body)
#         rating = data.get('rating')
#         review = data.get('review', '')
        
#         if not rating or not 1 <= int(rating) <= 5:
#             return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
        
#         # Get the order and verify ownership
#         order = get_object_or_404(Order, id=order_id)
#         if order.customer != request.user:
#             return JsonResponse({'error': 'Not authorized to rate this order'}, status=403)
        
#         if order.status != 'delivered':
#             return JsonResponse({'error': 'Cannot rate an order that is not delivered'}, status=400)
        
#         if not order.courier:
#             return JsonResponse({'error': 'This order has no courier to rate'}, status=400)
        
#         # Check if already rated
#         if hasattr(order, 'courier_rating'):
#             return JsonResponse({'error': 'Courier already rated for this order'}, status=400)
        
#         # Create the rating
#         rating_obj = CourierRating.objects.create(
#             courier=order.courier,
#             customer=request.user,
#             order=order,
#             rating=rating,
#             review=review
#         )
        
#         return JsonResponse({
#             'success': True,
#             'rating': rating_obj.rating,
#             'courier_avg_rating': order.courier.rating
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)