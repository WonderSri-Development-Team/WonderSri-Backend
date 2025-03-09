from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import userDevice
from .serializers import DeviceSerializer
from .notifications import send_push_notifications

# Create your views here.

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

def notify_user(user, title, body):
    devices = Device.objects.filter(user=user)
    for device in devices:
        response = send_push_notifications(device.fcm_token, title, body)
        print(f"Notification sent to {device.user_id}: {response}") # for debugging
        