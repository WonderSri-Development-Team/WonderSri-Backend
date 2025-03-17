from django.contrib.gis.db import models

class MainGeofence(models.Model):
    name = models.CharField(max_length=200)
    location = models.PolygonField(geography=True, srid=4326) 
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

class SubGeofence(models.Model):
    name = models.CharField(max_length=255)
    main_geofence = models.ForeignKey(MainGeofence, on_delete=models.CASCADE, related_name='sub_geofences')
    location = models.PolygonField(geography=True, srid=4326)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
