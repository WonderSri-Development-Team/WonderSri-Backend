from channels.generic.websocket import AsyncWebsocketConsumer
import json

class locationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        pass

    async def receive(self, text_data):
        pass
    
    async def disconnect(self, code):
        pass
