from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .service import check_geofence, nearBy_geofence

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
        if data.get('type') == 'NearByLocation':
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            nearby_geofences = await nearBy_geofence(longitude=longitude, latitude=latitude)
            print(nearby_geofences)
            await self.send(json.dumps({
                'type': 'NearByLocation',
                'nearby_geofences': nearby_geofences
            }))
            
        elif data.get('type') == 'location':
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # latitude = 7.089953576246863
            # longitude = 79.88710594626576
            #all_geofences = await all_one()
            geofence = await check_geofence(longitude=longitude, latitude=latitude)
            print(geofence)
            await self.send(json.dumps({
            'type': 'location',
            'latitude': latitude,
            'longitude': longitude,
            'current_geofences' : geofence['current_geofences'],
            'nearby_geofences' : geofence['nearby_geofences']
            }))
        elif data.get('type') == 'connection':
            await self.send(json.dumps({
                'type': data.get('type'),
                'status': data.get('status')
            }))
    
    async def disconnect(self):
        await self.send(json.dumps(
            {
                'type' : 'connection',
                'status' : "connection closed"
            }
        ))