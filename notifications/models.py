from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# class Device(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
#     fcm_token = models.CharField(max_length=255, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

class userDevice(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    fcm_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.user.username} - {self.fcm_token}"
