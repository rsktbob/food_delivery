from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from Restaurant.models import Restaurant
from Restaurant.forms import MenuItemForm
from order.models import Cart
from django.http import JsonResponse
from order.models import Order

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_customer():
            restaurants = Restaurant.objects.all()
            customer = request.user.customer_profile

            carts = Cart.objects.filter(customer=customer)
            context = {'restaurants' : restaurants, 'carts' : carts}           
            return render(request, 'core/customer_home.html', context)
        elif user.is_vendor():
            restaurant = user.vendor_profile.restaurants.first()
            form = MenuItemForm()
            context = {"restaurant" : restaurant, "form" : form}
            return render(request, 'core/vendor_home.html', context)
        elif user.is_courier():
            return render(request, 'core/courier_home.html')
        else:
            return render(request, 'account/login.html')
        
def hello(request):
    return JsonResponse({"message": "Hello, Food delivery!"})

def order(request, id):
    order = Order.objects.get(id=id)
    return JsonResponse({
            'order_id': order.id,
            'status': order.status,  # 假設你有這欄位
            'total': order.total_price # 假設你有這欄位
        })
