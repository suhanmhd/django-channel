from django.shortcuts import render

# Create your views here.
# dbuserapp/views.py
# Modify your view or API endpoint
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

def create_user_data(request):
    # Your logic to create user data

    # Assuming user_data is a dictionary with userid, username, and age
    user_data = {
        'userid': 'some_id',
        'username': 'some_username',
        'age': 25,
    }

    # Send WebSocket message to notify other users
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "user_data_group",
        {
            "type": "send.user_data",
            "data": user_data,
        },
    )

    return JsonResponse({"status": "success", "message": "User data created successfully."})

