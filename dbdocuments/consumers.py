

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class MyDocumentsConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("user_data_group", self.channel_name)

#     async def receive(self, text_data):
#         print("websocket received///////////", text_data)

#         # Process your received data here
#         received_data = json.loads(text_data)

#         # Extract data from the received JSON
#         username = received_data.get('username')
#         title = received_data.get('title')
#         content = received_data.get('content')
        

#         # Send a message to the group (other users)
#         await self.channel_layer.group_send(
#             "user_data_group",
#             {
#                 "type": "send_user_data",
#                 "data": received_data,
#             },
#         )

#         # Send a response back to the original sender
#         await self.send(text_data=json.dumps({
#             "message": "Your response message",
#         }))

#     async def send_user_data(self, event):
#         data = event["data"]

#         # Send the data to the WebSocket
#         await self.send(text_data=json.dumps(data))

#     async def disconnect(self, close_code):
#         print("websocket disconnected///////////", close_code)

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, Documents
from django.core.serializers.json import DjangoJSONEncoder



class MyDocumentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("user_data_group", self.channel_name)

    async def receive(self, text_data):
        print("websocket received///////////", text_data)

        # Process your received data here
        received_data = json.loads(text_data)
        print("Received data:", received_data)
        action = received_data.get('title')
        print(action,"lllllll")

        document_data =  received_data.get('documentData')

        # Extract data from the received JSON
        userId=  document_data.get('userId')
        title =  document_data.get('title')
        content =  document_data.get('content')
        print(content, "////\\\\")

        # Get or create the user
        user = await database_sync_to_async(User.objects.get)(
            id=userId,
        )
        print(user, "sssssssssssssssssssssss")

        # Create a new Documents instance
        document = await database_sync_to_async(Documents.objects.create)(
            user=user,
            title=title,
            content=content,
        )
        print(document, "dddddddddddddddddddddddddddddddd")

        # Send a message to the group (other users)
        await self.channel_layer.group_send(
            "user_data_group",
            {
                "type": "send_user_data",
                "data": document.to_json(),
            },
        )

        # Send a response back to the original sender
        await self.send(text_data=json.dumps({
            "message": "Your response message",
        }))

    async def send_user_data(self, event):
        data = event["data"]
        print(data)
        # Send the data to the WebSocket
        await self.send(text_data=json.dumps(data, cls=DjangoJSONEncoder))

    async def disconnect(self, close_code):
        print("websocket disconnected///////////", close_code)
