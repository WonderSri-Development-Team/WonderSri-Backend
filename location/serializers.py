from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404

from .models import Event, Venue, Location
from rest_framework import serializers
from .models import Venue, Location  # Adjust the import according to your models

class LocationSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(write_only=True)  # Explicitly expecting these fields
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Location
        fields = ('name', 'radius', 'longitude', 'latitude')

    def create(self, validated_data):
        print("Location Validated Data:", validated_data)  # Debugging
        coordinates = Point(validated_data.pop('longitude'), validated_data.pop('latitude'))
        validated_data['coordinates'] = coordinates  # Add Point field
        return super().create(validated_data)

class VenueSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Venue
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location', None)
        if not location_data:
            raise serializers.ValidationError({"location": "Location data is missing."})

        location_instance = Location.objects.create(
            name=location_data['name'],
            radius=location_data['radius'],
            coordinates=Point(location_data['longitude'], location_data['latitude'])  # Ensure coordinates are stored
        )

        venue = Venue.objects.create(location=location_instance, **validated_data)
        return venue



from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Event, Venue

class EventSerializer(serializers.ModelSerializer):
    venue_id = serializers.IntegerField(write_only=True, required=False)  # Add venue_id for input

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        venue_id = validated_data.pop('venue_id', None)  # Extract venue_id if provided

        # Create or fetch venue
        if venue_id:
            venue = get_object_or_404(Venue, id=venue_id)  # Fetch the existing venue
            validated_data['venue'] = venue  # Assign the venue to the event

        # Create the event
        event = Event.objects.create(**validated_data)
        return event

