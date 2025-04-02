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
from .constants import GENERAL_TIPS, notification_schema
import json
import random
from firebase_admin import messaging

class RegisterDeviceView(APIView):
    def post(self, request):
        fcm_token = request.data.get("fcm_token")
        
        if not fcm_token:
            return Response({"error": "FCM Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendNotificationView(APIView):
    def post(self, request):
        """
        Send a notification to a user.
        Accepts:
        - `user_id`: The ID of the user to send the notification to.
        - `title`: The notification title.
        - `body`: The notification body.
        - `notification_type`: (Optional) The type of notification (e.g., "general", "event", "scam_alert").
        """
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        body = request.data.get("body")
        notification_type = request.data.get("notification_type", "custom")

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        notify_user(user, title, body, notification_type)
        
        return Response({"message": f"Notification sent to user {user_id}"}, status=status.HTTP_200_OK)

        
@api_view(['GET'])
def get_notification_schema(request):
    """
    Returns the schema for notifications.
    """
    return Response(notification_schema, status=status.HTTP_200_OK)

def save_fcm_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            fcm_token = data.get("fcm_token")

            if (user_id and fcm_token):
                device, created = UserDevice.objects.update_or_create(
                    user_id=user_id, defaults={"fcm_token": fcm_token}
                )
                return JsonResponse({"message": "FCM Token Saved!"})
            return JsonResponse({"error": "Missing user_id or fcm_token"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid Request"}, status=400)


def notify_user(user, title=None, body=None, notification_type="general"):
    """
    Sends notifications of different types to the user.
    - If title and body are provided, sends a custom notification.
    - If notification_type is "general", sends a random general travel tip.
    """
    devices = UserDevice.objects.filter(user=user)

    if not devices:
        print(f"No registered devices for user {user.id}")
        return

    # Pick a general tip if no title/body is given
    if notification_type == "general" and not title and not body:
        tip = random.choice(GENERAL_TIPS)
        title = tip["title"]
        body = tip["body"]

    # Ensure title and body are not empty
    if not title or not body:
        print("Skipping notification: title or body missing.")
        return

    for device in devices:
        response = send_push_notifications(device.fcm_token, title, body)
        print(f"Notification sent to user {user.id} ({device.fcm_token}): {response}")  # Debugging

        
def send_push_notifications(fcm_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=fcm_token,
    )
    response = messaging.send(message)
    print("Notification Sent:", response)
    return response

def send_general_tips():
    """Send a random general tip as a notification to the user."""
    if not GENERAL_TIPS:
        return
    tip = random.choice(GENERAL_TIPS)
    users = User.objects.all()
    
    for user in users:
        devices = UserDevice.objects.filter(user=user)
        for device in devices:
            send_push_notifications(device.fcm_token, tip["title"], tip["body"])
            print(f"Notification sent to {device.user_id}")

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
        user_location = Point(float(longitude), float(latitude), srid=4326)
    except ValueError:
        return Response({"error": "Invalid location data"}, status=status.HTTP_400_BAD_REQUEST)

    nearby_events = Event.objects.filter(
        location__coordinates__distance_lte=(user_location, D(km=5)))

    if nearby_events:
        for event in nearby_events:
            user = get_object_or_404(User, id=user_id)
            notify_user(
                user=user,
                title=event.title,
                body=event.description,
                notification_type="event"
            )
        return Response({"message": "Notifications sent for nearby events"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No nearby events found"}, status=status.HTTP_200_OK)