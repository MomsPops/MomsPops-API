from django.urls import path

from .consumers import ChatConsumer


websocket_urlpatterns = [
    path("chats/", ChatConsumer.as_asgi()),

]
