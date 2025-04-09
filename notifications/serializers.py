from rest_framework import serializers
from .models import UserDevice
from users.serializers import UserSerializer

class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserDevice
        fields = ['user','fcm_token']