from django.db import connection
from channels.db import database_sync_to_async

def sync_check_geofence(longitude, latitude):
    # 7.089953576246863, 79.88710594626576
    query = """
    SELECT *
    FROM tracking_geofence
    WHERE ST_DWithin(
        ST_GeomFromGeoJSON(geojson)::geography,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        radius
    )
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [longitude, latitude])
            return cursor.fetchall()
    except Exception as e:
        print(f"Error checking geofence: {e}")
        return []
    

async def check_geofence(longitude, latitude):
    return await database_sync_to_async(sync_check_geofence)(longitude, latitude)
    

    # user_location = Point(longitude, latitude,  srid=4326) # 5234 - SriLanka (Kandawala / Sri Lanka Grid / 4326 - World Geodetic System 1984
    # return Geofence.objects.filter(area_intersects = user_location)


# Geofence.objects.annotate(distance=Distance('center', user_location)).order_by('distance').first()
# return nerarby geofences


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