from rest_framework import serializers
from .models import Event, Venue, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'coordinates', 'radius']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'venue_type', 'location', 'description', 'opening_hours', 'contact_info', 'website', 'is_active']

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