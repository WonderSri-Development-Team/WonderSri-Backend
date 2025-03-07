#from django.db import models
from django.contrib.gis.db import models


# class Geofence(models.Model):
#     name = models.CharField(max_length=100)
#     location = models.PointField()
#     radius = models.FloatField(help_text="Radius in meters")
#     area = models.PolygonField(blank=True, null=True)

#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         buffer_distance = self.radius / 111320.0
#         self.area = self.location.buffer(buffer_distance)
#         super(Geofence, self).save(*args, **kwargs)

class Geofence(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField() 
    radius = models.FloatField()    # Radius in meters
    description = models.TextField(blank=True, null=True)

class SubGeofence(models.Model):
    name = models.CharField(max_length=255)
    main_geofence = models.OneToOneField(Geofence, on_delete=models.CASCADE, related_name='sub_geofence')
    location = models.PointField()
    radius = models.FloatField()
    description = models.TextField(blank=True, null=True)
