from pyfcm import FCMNotification
from django.conf import settings

push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)

def send_push_notifications(registration_id, title, body):
    result = push_service.notify_single_device(
        registration_id=registration_id,
        message_title=title,
        message_body=body,
    )
    return result