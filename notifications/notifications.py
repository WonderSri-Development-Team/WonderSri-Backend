import firebase_admin
from firebase_admin import messaging, credentials
# from django.admin import settings
import base64
import json
from decouple import config

import random
from notifications.constants import GENERAL_TIPS
from .models import User, userDevice

def initialize_firebase():
    if not firebase_admin._apps: # Avoid re-initialization
        firebase_creds = json.loads(base64.b64decode(config("FIREBASE_CREDENTIALS_BASE64")).decode("utf-8"))
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)

initialize_firebase()

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
    devices = userDevice.objects.filter(user=User)

    for device in devices:
        send_push_notifications(device.fcm_token, tip["title"], tip["body"])
        print(f"Notification sent to {device.user_id}")