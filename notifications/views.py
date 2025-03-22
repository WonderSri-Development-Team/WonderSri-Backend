from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import userDevice
from .serializers import DeviceSerializer
from .notifications import send_push_notifications
import json
import random

# General travel tips
GENERAL_TIPS = [
    {"title": "Respect Local Customs", "body": "Always be mindful of the local customs and traditions."},
    {"title": "Dress Modestly in Public Spaces", "body": "Avoid wearing revealing clothes in public areas."},
    {"title": "Helmet Safety", "body": "Always wear a helmet when riding bikes or scooters."},
    {"title": "Footwear Etiquette", "body": "Remove your shoes before entering temples or homes."},
    {"title": "Public Transport", "body": "Keep small change handy for bus and train fares."},
    {"title": "Wildlife Safety", "body": "Do not feed or disturb animals in national parks."},
]

class RegisterDeviceView(APIView):
    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendNotificationView(APIView):
    def post(self, request):
        registration_id = request.data.get('registration_id')
        title = request.data.get('title', 'Default Title')
        body = request.data.get('body', 'Default Body')

        if not registration_id:
            return Response({'error': 'Registration ID is required'}),

        result = send_push_notifications(registration_id, title, body)
        return Response(result, status=status.HTTP_200_OK)

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
