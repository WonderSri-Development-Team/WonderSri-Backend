from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField( null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    pic_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"Profile of {self.user.username}"

