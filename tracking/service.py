from django.contrib.gis.geos import Point
from channels.db import database_sync_to_async
from .models import MainGeofence, SubGeofence
from .serializers import AllGeofenceSerializer, SubGeofenceSerializer, GeofenceSerializer

# 5234 - SriLanka (Kandawala / Sri Lanka Grid , 4326 - World Geodetic System 1984

@database_sync_to_async
def get_all_geofences_sync():
    """
    returns all main geofences with sub geofences
    """
    all_geofences = MainGeofence.objects.all()
    serialized_all_geofences = AllGeofenceSerializer(all_geofences, many=True)
    return serialized_all_geofences.data

@database_sync_to_async
def get_current_main_geofence_sync(longitude, latitude):
    """
    returns current main geofence
    """
    user_point = Point(longitude, latitude, srid=4326)
    current_geofence = MainGeofence.objects.filter(
        location__contains = user_point
    ).first()
    serialized_current_main_geofence = GeofenceSerializer(current_geofence, many=False)
    return serialized_current_main_geofence.data

@database_sync_to_async
def get_current_sub_geofence_sync(longitude, latitude):
    """
    returns current sub geofence
    """
    user_point = Point(longitude, latitude, srid=4326)
    current_sub_geofence = SubGeofence.objects.filter(
        location__contains = user_point
    ).first()
    serialized_current_sub_geofences = SubGeofenceSerializer(current_sub_geofence, many=False)
    return serialized_current_sub_geofences.data

@database_sync_to_async
def get_nearby_main_geofences_sync(longitude, latitude):
    """
    returns only nearby main geofences
    .prefetch_related('sub_geofence') - to get related sub geofences - use with AllGeofenceSerializer
    MainGeofence - to get only main geofences
    """
    user_point = Point(longitude, latitude, srid=4326)
    nearby_main_geofences = MainGeofence.objects.filter(
        location__dwithin = (user_point, 1000 )
    ).exclude(
        location__contains = user_point  # exclude user's current geofence
    ).prefetch_related('sub_geofence')
    serialized_nearby_main_geofences = AllGeofenceSerializer(nearby_main_geofences, many=True)
    return serialized_nearby_main_geofences.data

@database_sync_to_async
def get_sub_geofences_sync(main_geofence_id):
    """
    returns all sub geofences related to a main geofence
    """
    sub_geofences = SubGeofence.objects.filter(main_geofence = main_geofence_id).all()
    serialized_sub_geofences = SubGeofenceSerializer(sub_geofences, many=True)
    return serialized_sub_geofences.data


async def get_all_geofences():
    return await get_all_geofences_sync()

async def get_current_main_geofence(longitude, latitude):
    return await get_current_main_geofence_sync(longitude, latitude)

async def get_current_sub_geofence(longitude, latitude):
    return await get_current_sub_geofence_sync(longitude, latitude)

async def get_nearby_main_geofences(longitude, latitude):
    return await get_nearby_main_geofences_sync(longitude, latitude)

async def get_sub_geofences(main_geofence_id):
    return await get_sub_geofences_sync(main_geofence_id)


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