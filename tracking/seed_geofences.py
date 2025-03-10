import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WonderSri_backend.settings')
django.setup()

from tracking.models import MainGeofence, SubGeofence
from django.contrib.gis.geos import Point

galle_fort, created = MainGeofence.objects.get_or_create(
    name='Galle Fort',
    defaults={
        'location': Point(80.2170, 6.0267, srid=4326),
        'radius': 1000,
        'description': 'A UNESCO World Heritage Site, built by the Portuguese in 1588 and fortified by the Dutch in 1649.'
    }
)
if created:
    print("New MainGeofence created:", galle_fort)
else:
    print("MainGeofence already exists:", galle_fort)

sub_geofences_data = [
    ("Galle Lighthouse", 6.0253, 80.2174, 50, "Oldest lighthouse in Sri Lanka, offering a stunning ocean view."),
    ("Dutch Reformed Church", 6.0285, 80.2168, 40, "A historic church built in 1755 with colonial architecture."),
    ("National Maritime Museum", 6.0290, 80.2176, 60, "A museum showcasing maritime history and artifacts."),
    ("Old Dutch Hospital", 6.0267, 80.2158, 70, "A colonial-era hospital, now a shopping and dining complex."),
]

for name, latitude, longitude, radius, description in sub_geofences_data:
    sub_geofences, created = SubGeofence.objects.get_or_create(
        name = name,
        main_geofence = galle_fort,
        defaults= {
            'location': Point(longitude, latitude, srid=4326),
            'radius': radius,
            'description': description
        }
    )

print("Galle Fort and its SubGeofences have been saved successfully!")