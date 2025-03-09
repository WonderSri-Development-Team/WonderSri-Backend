from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from channels.db import database_sync_to_async
from .models import MainGeofence, SubGeofence
from .serializers import AllGeofenceSerializer, SubGeofenceSerializer, GeofenceSerializer

def sync_check_geofence(longitude, latitude):
    # 7.089953576246863, 79.88710594626576
    user_location = Point(longitude, latitude,  srid=4326) # 5234 - SriLanka (Kandawala / Sri Lanka Grid , 4326 - World Geodetic System 1984
    return MainGeofence.objects.filter(area__intersects=user_location)
    
def sync_nearby_geofence(longitude, latitude):
    """
    returns only nearby main geofences
    .prefetch_related('sub_geofences') - to get all sub geofences use with AllGeofenceSerializer
    """
    user_point = Point(longitude, latitude, srid=4326)
    nearby_geofences = MainGeofence.objects.filter(
        location__distance_lte=(user_point, Distance(m=100))
    ).exclude(
        area__intersects=user_point  # exclude current geofence
    ).prefetch_related('sub_geofences')
    return nearby_geofences


async def check_geofence(longitude, latitude):
    current_geofences = await database_sync_to_async(sync_check_geofence)(longitude, latitude)
    nearby_geofences = await database_sync_to_async(sync_nearby_geofence)(longitude, latitude)
    serializered_current_geofences = GeofenceSerializer(current_geofences, many=True)
    serializered_nearby_geofences = GeofenceSerializer(nearby_geofences, many=True)
    return {
        'current_geofences': serializered_current_geofences.data,
        'nearby_geofences': serializered_nearby_geofences.data
    }

async def nearBy_geofence(longitude, latitude):
    nearBy_geofence = await database_sync_to_async(sync_nearby_geofence)(longitude, latitude) 
    serialized_nearBy_geofence = GeofenceSerializer(nearBy_geofence, many=True)
    return serialized_nearBy_geofence.data

async def sub_geofence(main_geofence_id):
    sub_geofence = await database_sync_to_async(SubGeofence.objects.filter(main_geofence=main_geofence_id).all)()
    serialized_sub_geofence = SubGeofenceSerializer(sub_geofence, many=True)
    return serialized_sub_geofence.data

async def main_geofence_all():
    all_main_geofences = await database_sync_to_async(MainGeofence.objects.all)()
    serialized_main_geofence =  GeofenceSerializer(all_main_geofences, many=True)
    return serialized_main_geofence.data

# Geofence.objects.create(
#     name="Central Park",
#     geojson={"type": "Point", "coordinates": [-73.9654, 40.7829]},
#     radius=500  # Radius in meters
# )

# def all_sync():
#     query = """
#     SELECT *
#     FROM tracking_geofence
#     """
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             return cursor.fetchall()
#     except Exception as e:
#         print(f"Error checking geofence: {e}")
#         return []
    

# async def all_one():
#     return await database_sync_to_async(all_sync)()

# query = """
    # SELECT *
    # FROM tracking_geofence
    # WHERE ST_DWithin(
    #     ST_GeomFromGeoJSON(geojson)::geography,
    #     ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
    #     radius
    # )
    # """
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute(query, [longitude, latitude])
    #         return cursor.fetchall()
    # except Exception as e:
    #     print(f"Error checking geofence: {e}")
    #     return []