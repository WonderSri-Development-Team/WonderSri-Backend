import firebase_admin
from firebase_admin import credentials
# from django.admin import settings
import base64
import json
from decouple import config

def initialize_firebase():
    if not firebase_admin._apps: # Avoid re-initialization
        firebase_creds = json.loads(base64.b64decode(config("FIREBASE_CREDENTIALS_BASE64")).decode("utf-8"))
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)

initialize_firebase()
