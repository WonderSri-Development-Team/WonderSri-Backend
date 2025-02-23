from django.db import models

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
