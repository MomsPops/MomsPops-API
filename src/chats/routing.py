from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/chats/<uuid:chat_id>/", consumers.ChatConsumer.as_asgi()),

]
