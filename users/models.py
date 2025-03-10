from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=10, default='en')
    notification_radius = models.IntegerField(default=100, help_text="Preferred notification radius in meters")
    interests = models.JSONField(default=list, blank=True)
    visited_locations = models.ManyToManyField('location.Location', through='UserVisit')
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class UserVisit(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey('location.Location', on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['user_profile', 'location', 'visited_at']

class SavedItem(models.Model):
    ITEM_TYPES = [
        ('venue', 'Venue'),
        ('event', 'Event'),
        ('location', 'Location'),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    item_id = models.IntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['user_profile', 'item_type', 'item_id']
