import firebase_admin
from firebase_admin import messaging, credentials
from django.admin import settings

def initialize_firebase():
    if not firebase_admin._apps: # Avoid re-initialization
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
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
