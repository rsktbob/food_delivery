
# from django.test import TestCase, Client
# from django.urls import reverse
# from account.models import BaseUser
# from unittest.mock import patch
# from order.models import Restaurant, Order

# class OrderManageHandlerTests(TestCase):
    
#     def setUp(self):
#         self.user = BaseUser.objects.create_user(username='testuser', password='testpassword')
#         self.client = Client()
        
#         self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Test St")
    
#     def test_create_order_success(self):
#         data = {
#             'restaurant_id': self.restaurant.id,
#             'delivery_address': "456 New Address",
#             'total_price': 100.00,
#             'payment_method': "Credit Card",
#             'delivery_fee': 10.00
#         }

#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.post(reverse('create_order'), data)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['status'], 'success')
#         self.assertEqual(response.json()['message'], 'Order created successfully!')

#     def test_set_order_state_success(self):
#         order = Order.objects.create(
#             restaurant=self.restaurant,
#             delivery_address="456 New Address",
#             status='Created',
#             payment_method="Credit Card",
#             total_price=100.00,
#             delivery_fee=10.00
#         )
        
#         data = {'order_id': order.id, 'state': 'Accepted'}
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.post(reverse('set_order_state'), data)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['status'], 'success')
#         self.assertEqual(response.json()['message'], 'Order state updated successfully!')

#     @patch('orders.services.CourierOrderService.search_nearby_order')
#     def test_check_courier_order_success(self, mock_search_nearby_order):
#         mock_search_nearby_order.return_value = ['order1', 'order2']
#         response = self.client.get(reverse('check_courier_order'))

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['status'], 'success')
#         self.assertEqual(len(response.json()['nearby_orders']), 2)

#     @patch('orders.services.VendorOrderService.get_restaurant_orders')
#     def test_check_vendor_order_success(self, mock_get_restaurant_orders):
#         mock_get_restaurant_orders.return_value = [Order(id=1)]
#         data = {'restaurant_id': self.restaurant.id}
#         response = self.client.post(reverse('check_vendor_order'), data)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['status'], 'success')
#         self.assertEqual(len(response.json()['orders']), 1)
