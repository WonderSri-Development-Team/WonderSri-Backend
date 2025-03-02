from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from channels.db import database_sync_to_async
from .models import Geofence
from django.db import connection


# Geofence.objects.create(
#     name="Central Park",
#     geojson={"type": "Point", "coordinates": [-73.9654, 40.7829]},
#     radius=500  # Radius in meters
# )

def all_sync():
    query = """
    SELECT *
    FROM tracking_geofence
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error checking geofence: {e}")
        return []
    

async def all_one():
    return await database_sync_to_async(all_sync)()

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