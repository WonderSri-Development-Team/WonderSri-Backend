from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .service import check_geofence

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
            print(data.get('type'))
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            in_geofence = check_geofence(longitude=longitude, latitude=latitude)
            #print(in_geofence)
            await self.send(json.dumps({
            'type': 'location',
            'latitude': latitude,
            'longitude': longitude,
            }))
        elif data.get('type') == 'connection':
            print(data.get('type'))
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