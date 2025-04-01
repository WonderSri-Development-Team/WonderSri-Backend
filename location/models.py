from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator

class Location(models.Model):
    """Represents a geographic location, including attractions, restaurants, shops, etc."""

    VENUE_TYPES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Café'),
        ('bar', 'Bar'),
        ('attraction', 'Tourist Attraction'),
        ('shop', 'Shop'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    coordinates = gis_models.PointField(geography=True, spatial_index=True, default=Point(0.0, 0.0))
    category = models.CharField(max_length=20, choices=VENUE_TYPES, null=True, blank=True)
    radius = models.PositiveIntegerField(
        help_text="Radius in meters for triggering notifications",
        validators=[MinValueValidator(1)],
        default=100
    )
    description = models.TextField(null=True, blank=True)
    opening_hours = models.JSONField(null=True, blank=True)
    contact_info = models.JSONField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display() if self.category else 'General Location'})"


class TouristTip(models.Model):
    """Tourist tips related to specific locations."""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tips')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tip: {self.title} at {self.location.name}"


class Event(models.Model):
    """Represents an event happening at a specific location."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events', default=3)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.location.name}"


class Activity(models.Model):
    """Represents an activity available at a location."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='activities')
    operating_hours = models.JSONField(null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.location.name}"


class Food(models.Model):
    """Represents local food or specialty dishes related to a location."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.description})"
