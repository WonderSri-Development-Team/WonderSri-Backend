from django.utils.timezone import now
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy.distance import geodesic
from notifications.views import send_push_notifications
from .supabase import fetch_events

# Create your views here.

@api_view(['POST'])
def check_nearby_events(request):
    """
    Check if the user has entered an event geofence.
    If yes, send a notification.
    """
    latitude = request.data.get('lat')
    longitude = request.data.get('lon')
    fcm_token = request.data.get('fcm_token')

    if not latitude or not longitude or not fcm_token:
        return Response({"error": "Latitude, Longitude, and FCM Token are required"}, status=400)

    user_location = (float(latitude), float(longitude))
    events = fetch_events() # Get events from Supabase

    nearby_events = []
    for event in events:
        event_location = (event["latitude"], event["longitude"])
        distance = geodesic(user_location, event_location).meters # Calculate distance in meters
        if distance <= 100: # Chekc if user is inside 100 meters of the event
            nearby_events.append(event)

    if nearby_events:
        for event in nearby_events:
            send_push_notifications(
                fcm_token,
                f"Nearby Event: {event['title']}",
                f"Happening Soon: {event['description']}"
            )
        return Response({"message": "Notifications sent", "events": nearby_events})

    return Response({"message": "No nearby events found"})