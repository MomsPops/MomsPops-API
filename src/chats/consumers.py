from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Chat, ChatMessage, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    Consumer for chats.
    """

    async def connect(self):
        """Сonnection to websocket."""

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat, _ = await Chat.objects.aget_or_create(id=self.chat_id)
        self.room_group_name = "chat_%s" % self.chat_id
        await self.accept()
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

    async def disconnect(self, close_code):
        """Disconnecting from websocket."""

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            message = await Message.objects.acreate(text=content['message'])
            await ChatMessage.objects.acreate(chat=self.chat, message=message)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message_echo",
                    "message": MessageSerializer(message).data,
                },
            )
        return super().receive_json(content, **kwargs)

    async def chat_message_echo(self, event):
        await self.send_json(event)
