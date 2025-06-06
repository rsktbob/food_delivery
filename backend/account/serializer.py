from rest_framework import serializers
from .models import *

class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourierUser
        fields = ['id', 'username', 'latitude', 'longitude']