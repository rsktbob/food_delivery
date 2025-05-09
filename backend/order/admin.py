from django.contrib import admin
from order.models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Cart)
