# your_app/consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class MyDocumentsConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def receive(self, text_data):
#         print("websocket received///////////", text_data)
#         # Process your received data here
#         await self.send(text_data=json.dumps({
#             'message': 'Your response message',
#         }))

#     async def disconnect(self, close_code):
#         print("websocket disconnected///////////", close_code)
#         # Clean up any resources if needed


# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, Documents

class MyDocumentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        print("websocket received///////////", text_data)

        # Process your received data here
        received_data = json.loads(text_data)

        # Extract data from the received JSON
        # username = received_data.get('username')
        # age = received_data.get('age')
        title = received_data.get('title')
        content = received_data.get('content')

        # Get or create the user (uncomment if needed)
        # user, created = await database_sync_to_async(User.objects.get_or_create)(
        #     username=username, defaults={'age': age}
        # )

        # Create a new Documents instance
        document = await database_sync_to_async(Documents.objects.create)(
            title=title, content=content
        )

        # Send a response back to the sender
        await self.send(text_data=json.dumps({
            'message': 'Your response message',
        }))

        # Send real-time updates to other users
        await self.send_realtime_updates(document)

    async def disconnect(self, close_code):
        print("websocket disconnected///////////", close_code)

    async def send_realtime_updates(self, document):
        # Get data in JSON format
        document_data = document.to_json()

        # Send a message to the group (other users)
        await self.channel_layer.group_send(
            "user_data_group",
            {
                "type": "send.user_data",
                "data": document_data,
            },
        )
