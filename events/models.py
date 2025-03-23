from django.db import models

# Create your models here.

class EventLocation(models.Model):
    event = models.OneToOneField('Event', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name