from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device
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

def notify_user(user, title, body):
    devices = Device.objects.filter(user=user)
    for device in devices:
        send_push_notifications(device.fcm_token, title, body)