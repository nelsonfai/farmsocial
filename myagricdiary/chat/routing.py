
from django.urls import path
from .import consumers

websocket_urlpatterns =[
     path('chat/chatroom/<slug:slug>',consumers.ChatConsumer.as_asgi()) ,
]

