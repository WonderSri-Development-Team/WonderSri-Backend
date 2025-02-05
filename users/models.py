from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.IntegerField(help_text="Radius in meters for triggering notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TouristTip(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tips')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.location.name}"

class Venue(models.Model):
    VENUE_TYPES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Café'),
        ('bar', 'Bar'),
        ('attraction', 'Tourist Attraction'),
        ('shop', 'Shop'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    venue_type = models.CharField(max_length=20, choices=VENUE_TYPES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='venues')
    description = models.TextField()
    opening_hours = models.JSONField(null=True, blank=True)
    contact_info = models.JSONField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_venue_type_display()})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=10, default='en')
    notification_radius = models.IntegerField(default=100, help_text="Preferred notification radius in meters")
    interests = models.JSONField(default=list, blank=True)
    visited_locations = models.ManyToManyField(Location, through='UserVisit')
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"

class UserVisit(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
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
