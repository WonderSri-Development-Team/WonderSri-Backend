from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .service import get_nearby_main_geofences, get_sub_geofences, get_current_main_geofence, get_current_sub_geofence
class locationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(json.dumps(
            {
                'type' : 'connection',
                'status' : "connection Accepted"
            }
        ))

    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        # return all Main geofences
        if data.get('type') == 'nearbygeofences':
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # return nearby Main geofences with sub geofences
            print(latitude, longitude)
            nearby_geofences = await get_nearby_main_geofences(latitude=latitude, longitude=longitude)
            print(nearby_geofences)
            await self.send(json.dumps({
                'type': 'nearbygeofences',
                'nearby_geofences': nearby_geofences
            }))

        # return all sub geofences related to a main geofence
        elif data.get('type') == 'subGeofences':
            main_geofence = data.get('main_geofence')
            main_geofence_id = main_geofence.get('id')
            print(main_geofence_id)
            sub_geofences = await get_sub_geofences(main_geofence_id)
            print(sub_geofences)
            await self.send(json.dumps({
                'type': 'subGeofences',
                'sub_geofences': sub_geofences
            }))
            
        elif data.get('type') == 'location':
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # latitude = 7.089953576246863
            # longitude = 79.88710594626576
            print(latitude, longitude)
            main_geofence = await get_current_main_geofence(latitude=latitude, longitude=longitude)
            print(main_geofence)
            sub_geofences = await get_current_sub_geofence(latitude=latitude, longitude=longitude)
            print(sub_geofences)
            await self.send(json.dumps({
                'type': 'location',
                'current_geofences' : main_geofence,
                'nearby_geofences' : sub_geofences
            }))
            
        elif data.get('type') == 'connection':
            await self.send(json.dumps({
                'type': data.get('type'),
                'status': data.get('status')
            }))
    
    async def disconnect(self, close_code):
        await self.send(json.dumps(
            {
                'type' : 'connection',
                'status' : close_code
            }
        ))