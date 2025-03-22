from cProfile import Profile

from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import UserProfile
from .models import Event, Food, Location, Activity  # Adjusted imports


class LocationSerializer(serializers.ModelSerializer):
    """Handles location serialization with explicit latitude & longitude fields."""

    longitude = serializers.FloatField(write_only=True)  # Explicitly expecting these fields
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Location
        fields = (
        'id', 'name', 'category', 'radius', 'longitude', 'latitude', 'description', 'opening_hours', 'contact_info',
        'website')

    def create(self, validated_data):
        """Create a Location instance with proper GIS coordinates."""
        coordinates = Point(validated_data.pop('longitude'), validated_data.pop('latitude'))
        validated_data['coordinates'] = coordinates  # Assign GIS field
        return super().create(validated_data)


class EventSerializer(serializers.ModelSerializer):
    """Handles event serialization with automatic location creation if needed."""

    location_id = serializers.IntegerField(write_only=True, required=False)  # Optional ID
    location_details = LocationSerializer(write_only=True, required=False)  # Location details

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        """Create an event linked to an existing or new location."""
        location_id = validated_data.pop('location_id', None)
        location_details = validated_data.pop('location_details', None)

        if location_id:
            location = get_object_or_404(Location, id=location_id)
        elif location_details:
            # Create a new location if details are provided
            coordinates = Point(location_details.pop('longitude'), location_details.pop('latitude'))
            location_details['coordinates'] = coordinates
            location = Location.objects.create(**location_details)
        else:
            raise serializers.ValidationError({"location": "Either location_id or location_details must be provided."})

        validated_data['location'] = location
        return Event.objects.create(**validated_data)


class ActivitiesSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Activity
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location', None)

        if isinstance(location_data, dict):  # If location details are given, create a new location
            location = Location.objects.create(
                name=location_data['name'],
                radius=location_data.get('radius', 100),  # Default radius if not provided
                coordinates=Point(location_data['longitude'], location_data['latitude'])
            )
        else:
            raise serializers.ValidationError({"location": "Invalid location data."})

        validated_data['location'] = location  # Assign the new location to the activity
        return Activity.objects.create(**validated_data)


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'



