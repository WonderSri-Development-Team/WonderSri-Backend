from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class MainGeofence(models.Model):
    name = models.CharField(max_length=200)
    location = models.PolygonField(geography=True, srid=4326) 
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    main_point = models.PointField(geography=True, default=Point(0.0, 0.0) , srid=4326)

class SubGeofence(models.Model):
    name = models.CharField(max_length=255)
    main_geofence = models.ForeignKey(MainGeofence, on_delete=models.CASCADE, related_name='sub_geofences')
    location = models.PolygonField(geography=True, srid=4326)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    main_point = models.PointField(geography=True, default=Point(0.0, 0.0), srid=4326)
