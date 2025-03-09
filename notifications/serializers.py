from rest_framework import serializers
from .models import userDevice

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = userDevice
        fields = ['user','fcm_token']