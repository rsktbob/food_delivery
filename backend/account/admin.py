from django.contrib import admin
from account.models import *

admin.site.register(CustomerProfile)
admin.site.register(CourierProfile)
admin.site.register(VendorProfile)
admin.site.register(BaseUser)