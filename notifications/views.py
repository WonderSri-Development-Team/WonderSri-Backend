from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, userDevice
from .serializers import DeviceSerializer
from .notifications import send_push_notifications
from .constants import GENERAL_TIPS, notification_schema
import json
import random
from firebase_admin import messaging

from decouple import config
from pyfcm import FCMNotification

push_service = FCMNotification(api_key=config('FIREBASE_API_KEY'))

class RegisterDeviceView(APIView):
    def post(self, request):
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
        
class GetNotificationSchemaView(APIView):
    def get(self, request):
        return Response(notification_schema)

def save_fcm_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            fcm_token = data.get("fcm_token")

            if (user_id and fcm_token):
                device, created = userDevice.objects.update_or_create(
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
    devices = userDevice.objects.filter(user=user)

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


def welcome_notification(user):
    """
    Sends a welcome notification to the user.
    """
    if not user.fcm_token:
        print(f"No FCM token found for user {user.id}")
        return
    
    # Send a welcome notification to the user
    return notify_user(
        user=user,
        title="Welcome to WonderSri!",
        body="Thanks for trying out our app! Get ready to explore the wonders of Sri Lanka with WonderSri!"
        )
        
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
        devices = userDevice.objects.filter(user=user)
        for device in devices:
            send_push_notifications(device.fcm_token, tip["title"], tip["body"])
            print(f"Notification sent to {device.user_id}")