from django.contrib.gis.geos import Point
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



class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)  # Optional nested location
    venue = VenueSerializer(required=False)  # Optional nested venue

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'venue', 'location', 'start_date', 'end_date', 'price', 'image']

    def create(self, validated_data):
        # Extract nested location and venue data
        location_data = validated_data.pop('location', None)
        venue_data = validated_data.pop('venue', None)

        # Create or fetch location
        if location_data:
            location = Location.objects.create(**location_data)
            validated_data['location'] = location

        # Create or fetch venue
        if venue_data:
            # If venue has a nested location, create it first
            if 'location' in venue_data:
                venue_location_data = venue_data.pop('location')
                venue_location = Location.objects.create(**venue_location_data)
                venue_data['location'] = venue_location
            venue = Venue.objects.create(**venue_data)
            validated_data['venue'] = venue

        # Create the event
        event = Event.objects.create(**validated_data)
        return event