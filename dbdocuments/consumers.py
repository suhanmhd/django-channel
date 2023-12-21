# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyDocumentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        print("websocket received///////////", text_data)
        # Process your received data here
        await self.send(text_data=json.dumps({
            'message': 'Your response message',
        }))

    async def disconnect(self, close_code):
        print("websocket disconnected///////////", close_code)
        # Clean up any resources if needed


# from channels.generic.websocket import AsyncWebsocketConsumer

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class MyDocumentsConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

    