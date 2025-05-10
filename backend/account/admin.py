from django.contrib import admin
from account.models import *

admin.site.register(CustomerUser)
admin.site.register(CourierUser)
admin.site.register(VendorUser)
admin.site.register(BaseUser)