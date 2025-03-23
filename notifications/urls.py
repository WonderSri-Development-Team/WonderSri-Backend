from django.urls import path
from .views import RegisterDeviceView, SendNotificationView, GetNotificationSchemaView

urlpatterns = [
    path('register-device/', RegisterDeviceView.as_view(), name='register_device'),
    path('send-notification/', SendNotificationView.as_view(), name='send_notification'),
    path('get-notification-schema/', GetNotificationSchemaView.as_view(), name='get_notification_schema'),
]