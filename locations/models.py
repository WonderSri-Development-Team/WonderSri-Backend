from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name