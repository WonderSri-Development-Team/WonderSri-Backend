from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator

class Location(models.Model):
    """Represents a geographic location with a notification radius."""
    name = models.CharField(max_length=200)
    coordinates = gis_models.PointField(geography=True, spatial_index=True, default=Point(0.0, 0.0))  # ✅ Default Point (0,0)
    radius = models.PositiveIntegerField(
        help_text="Radius in meters for triggering notifications",
        validators=[MinValueValidator(1)]  # ✅ Ensuring positive radius
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.radius}m radius)"

class TouristTip(models.Model):
    """Tourist tips related to specific locations."""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tips')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tip: {self.title} at {self.location.name}"

class Venue(models.Model):
    """Represents a venue like restaurants, attractions, shops, etc."""
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
        return f"{self.name} ({self.get_venue_type_display()}) - {self.location.name}"

class Event(models.Model):
    """Represents an event happening at a venue or a specific location."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)]  # ✅ Ensuring non-negative price
    )
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.venue.name if self.venue else 'No Venue'}"
