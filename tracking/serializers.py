from rest_framework import serializers
from .models import MainGeofence, SubGeofence

class SubGeofenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGeofence
        fields = '__all__'

class AllGeofenceSerializer(serializers.ModelSerializer):
    sub_geofences = SubGeofenceSerializer(many=True, read_only=True)
    class Meta:
        model = MainGeofence
        fields = ['id', 'name', 'location', 'description', 'image_url', 'main_point', 'sub_geofences']

class GeofenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainGeofence
        fields = '__all__'
