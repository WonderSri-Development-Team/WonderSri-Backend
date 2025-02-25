from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .service import check_geofence, all_one

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
        if data.get('type') == 'location':
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # latitude = 7.089953576246863
            # longitude = 79.88710594626576
            #all_geofences = await all_one()
            in_geofence = await check_geofence(longitude=longitude, latitude=latitude)
            print(in_geofence)
            await self.send(json.dumps({
            'type': 'location',
            'latitude': latitude,
            'longitude': longitude,
            'in_geofence' : in_geofence
            }))
        elif data.get('type') == 'connection':
            await self.send(json.dumps({
                'type': data.get('type'),
                'status': data.get('status')
            }))
    
    async def disconnect(self, code):
        await self.send(json.dumps(
            {
                'type' : 'connection',
                'status' : "connection closed"
            }
        ))