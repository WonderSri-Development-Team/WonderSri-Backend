from django.urls import path
from .views import RegisterDeviceView, SendNotificationView, get_notification_schema, check_nearby_events

urlpatterns = [
    path('register-device/', RegisterDeviceView.as_view(), name='register_device'),
    path('send-notification/', SendNotificationView.as_view(), name='send_notification'),
    path('get-notification-schema/', get_notification_schema(), name='get_notification_schema'),
    path('check-nearby-events/', check_nearby_events, name='check_nearby_events'),
]