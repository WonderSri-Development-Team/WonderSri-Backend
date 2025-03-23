from rest_framework import serializers
from .models import userDevice
from users.serializers import UserSerializer

class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = userDevice
        fields = ['user','fcm_token']