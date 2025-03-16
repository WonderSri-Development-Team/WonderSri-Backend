import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WonderSri_backend.settings')
django.setup()

from tracking.models import MainGeofence, SubGeofence
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import Polygon

main_latlngs = [
    (6.030287, 80.213537),
    (6.026841, 80.213923),
    (6.02379, 80.217571),          
    (6.024526,80.219888),
    (6.027492, 80.219964),          
    (6.029455,80.219159),
    (6.030853, 80.217035),
    (6.030287, 80.213537)
]

main_polygon_obj = Polygon(main_latlngs)

galle_fort, created = MainGeofence.objects.get_or_create(
    name='Galle Fort',
    defaults={
        'location': main_polygon_obj,
        'description': 'A UNESCO World Heritage Site, built by the Portuguese in 1588 and fortified by the Dutch in 1649.'
    }
)
if created:
    print("New MainGeofence created:", galle_fort)
else:
    print("MainGeofence already exists:", galle_fort)

sub_geofences_data = [
    # name, polygon, description
    (
        "Galle Fort main entrance", 
        Polygon([
            (6.030314, 80.21601),
            (6.030002, 80.216034),
            (6.030031, 80.216176),
            (6.030341, 80.216158),
            (6.030314, 80.21601)
        ]),
        "The main entrance to the fort, facing the Galle International Cricket Stadium."
    ),
    (
        "Galle Lighthouse", 
        Polygon([
            (6.024571, 80.219349),
            (6.024595,80.219465),
            (6.024496, 80.219489),
            (6.024494, 80.219339),
            (6.024571, 80.219349)
        ]), 
        "Oldest lighthouse in Sri Lanka, offering a stunning ocean view."
    ),
    (
        "Galle Services club",
        Polygon([
            (6.029898, 80.215531),
            (6.029682, 80.215545),
            (6.029583, 80.215835),
            (6.029602, 80.216076),
            (6.029954, 80.216041),
            (6.029898, 80.215531)
        ]), 
        ""
    ),
    (
        "Galle Clock Tower",
        Polygon([
            (6.030069, 80.215035),
            (6.029991, 80.215049),
            (6.030002, 80.215116),
            (6.030069, 80.215108),
            (6.030069, 80.215035)
        ]), 
        ""
    ),
    (
        "Dutch Reformed Church", 
        6.0285, 80.2168, 
        "A historic church built in 1755 with colonial architecture."
    ),
    (
        "National Maritime Museum", 
        6.0290, 80.2176, 
        "A museum showcasing maritime history and artifacts."
    ),
    (
        "Old Dutch Hospital", 
        6.0267, 80.2158, 
        "A colonial-era hospital, now a shopping and dining complex."
    )
]

for name, polygon, description in sub_geofences_data:
    sub_geofences, created = SubGeofence.objects.get_or_create(
        name = name,
        main_geofence = galle_fort,
        defaults= {
            'location': polygon,
            'description': description
        }
    )

print("Galle Fort and its SubGeofences have been saved successfully!")