from django.db import connection
from channels.db import database_sync_to_async

def sync_check_geofence(longitude, latitude, user_radius = 5):
    query = """
    SELECT *
    FROM Geofence
    WHERE ST_DWithin(
        ST_GeomFromGeoJSON(geojson),
        ST_SetSRID(ST_MakePoint(%s, %s), 4326),
        %s
    )
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [longitude, latitude, user_radius]) 
        return cursor.fetchall()
    
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
