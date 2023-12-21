from django.urls import path
from dbdocuments.consumers import MyDocumentsConsumer



websocket_urlpatterns = [

    path('ws/documents/', MyDocumentsConsumer.as_asgi()),
    # Add more WebSocket URL patterns if needed
]
