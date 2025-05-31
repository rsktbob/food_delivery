from typing import List
from order.models import *
from django.shortcuts import get_object_or_404
from account.models import *
from Restaurant.models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


class OrderService:
    def set_order_state(self, order_id, status):
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            return True
        except:
            return False

    def get_order_state(self, order_id) -> str:
        try:
            order = Order.objects.get(id=order_id)
            status = order.status
            return status
        except:
            return None


class CustomerOrderService(OrderService):
    def create_order(self, order_info):
        try:
            # 獲取 customer 資料
            customer = CustomerUser.objects.get(user_id=order_info['user_id'])
        
            restaurant_id = order_info['restaurant_id']
            restaurant = Restaurant.objects.get(id=restaurant_id)

            # 創建 Order
            order = Order.objects.create(
                customer=customer,
                restaurant=restaurant,  # 傳遞 Restaurant 實例
                delivery_address=order_info['delivery_address'],
                status='Created',
                payment_method=order_info['payment_method'],
                total_price=order_info['total_price'],
                delivery_fee=order_info['delivery_fee'],
            )

            return True
        except:
            return False


class VendorOrderService(OrderService):
    def get_restaurant_orders(self, restaurant_id) -> List[Order]:
        return Order.objects.filter(restaurant_id=restaurant_id)

    def accept_restaurant_order(self, order_id) -> bool:
        return self.set_order_state(order_id, 'Accepted')


class CourierOrderService(OrderService):
    def search_nearby_order(self) -> List[Order]:  # 導航先不寫
        return Order.objects.filter(status='Accepted')

    def accept_for_delivery(self, order_id):
        order = Order.objects.get(id=order_id)
        if order.status == "Accepted":
            self.set_order_state(order_id, 'Assigned')
            return True
        else:
            return False

    def pick_up_meal(self, order_id):
        order = Order.objects.get(id=order_id)
        if order.status == "Assigned":
            self.set_order_state(order_id, 'Picked_Up')
            return True
        else:
            return False

    def finish_restaurant_order(self, order_id):
        order = Order.objects.get(id=order_id)
        if order.status == "Picked_Up":
            self.set_order_state(order_id, 'Finish')
            return True
        else:
            return False

    def nevigation(self, position):
        return
