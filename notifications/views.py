from datetime import datetime, timezone
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.gis.geos import Point 
from django.contrib.gis.measure import D # For distance calculations
from .models import User, UserDevice
from location.models import Event, Location, Activity, Food
from .serializers import DeviceSerializer
from .constants import GENERAL_TIPS, NOTIFICATION_SCHEMA
import json
import random
from firebase_admin import messaging

class RegisterDeviceView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        fcm_token = request.data.get("fcm_token")
        
        if not user_id or not fcm_token:
            return Response({"error": "User ID and FCM Token are required"}, status=status.HTTP_400_BAD_REQUEST)

        device, created = UserDevice.objects.update_or_create(
            user_id=user_id,
            defaults={"fcm_token": fcm_token}
        )
        
        serializer = DeviceSerializer(device)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendNotificationView(APIView):
    """
    Send a notification to a specific user.
    Request Body:
    - user_id (int): Required. The ID of the user to send the notification to.
    - title (str): Optional if using 'general' type. The title of the notification.
    - body (str): Optional if using 'general' type. The body of the notification.
    - notification_type (str): Optional. Default is 'custom'. Options: 'custom', 'general', 'event', etc.
    """
    def post(self, request):
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        body = request.data.get("body")
        notification_type = request.data.get("notification_type", "custom")

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        if notification_type == "custom" and (not title or not body):
            return Response({"error": "Custom notifications require a title and body."},
                            status=status.HTTP_400_BAD_REQUEST)

        send_notification_to_user(user, title, body, notification_type)

        return Response({"message": f"Notification sent to user {user_id}"}, status=status.HTTP_200_OK)

        
@api_view(['GET'])
def get_notification_schema():
    """
    Returns the schema for notifications.
    """
    return Response(NOTIFICATION_SCHEMA)

        
def send_notification_to_device(fcm_token, title, body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=fcm_token,
        data=data or {},
    )
    response = messaging.send(message)
    print(f"Notification Sent to {fcm_token}: {response}")
    return response


def send_notification_to_user(user, title=None, body=None, data=None):
    """
    Centralized function to send notifications to all devices of a user.
    """
    devices = UserDevice.objects.filter(user=user)

    if not devices.exists():
        print(f"No registered devices for user {user.id}")
        return

    for device in devices:
        send_notification_to_device(device.fcm_token, title, body, data)

def send_general_tip_to_user(user):
    """Send a random general tip as a notification to the user."""
    users = User.objects.all()
    for user in users:
        if not GENERAL_TIPS:
            return
        tip = random.choice(GENERAL_TIPS)
        send_notification_to_user(user, tip["title"], tip["body"])


def notify_new_event(event):
    """Notify all users about a new event."""
    users = User.objects.filter(profile__notifications_enabled=True)
    
    for user in users:
        send_notification_to_user(user, event.title, event.description)
        print(f"Notification sent to {user.username} about new event: {event.title}")


@api_view(['POST'])
def check_nearby_events(request):
    """
    Check if there are any events nearby the user's location.
    Accepts:
    - `user_id`: The ID of the user to check for events.
    - `latitude`: The latitude of the user's location.
    - `longitude`: The longitude of the user's location.
    """
    user_id = request.data.get("user_id")
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if not user_id or not latitude or not longitude:
        return Response({"error": "User ID, latitude, and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = get_object_or_404(User, id=user_id)
        user_location = Point(float(longitude), float(latitude), srid=4326)
    except ValueError:
        return Response({"error": "Invalid location data"}, status=status.HTTP_400_BAD_REQUEST)

    nearby_events = Event.objects.filter(
        location__coordinates__distance_lte=(user_location, D(km=5)))

    if nearby_events.exists():
        # Send notifications for each nearby event
        for event in nearby_events:
            send_notification_to_user(
                user=user,
                title=event.title,
                body=event.description,
                data={'timestamp': datetime.now(timezone.utc).isoformat()}
            )
        return Response({"message": "Notifications sent for nearby events"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No nearby events found"}, status=status.HTTP_200_OK)