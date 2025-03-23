from django.db import models
from django.contrib.auth import get_user_model
from users.models import User

User = get_user_model()

class userDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Now a ForeignKey
    fcm_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.fcm_token}"
