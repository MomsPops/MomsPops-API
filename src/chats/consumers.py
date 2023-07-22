from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Chat, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    Consumer for chats.
    """

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

    @database_sync_to_async
    def add_message(self, chat: Chat, message: Message):
        return chat.messages.add(message)

    async def connect(self):
        """Сonnection to websocket."""
        if self.scope.get('user', None) is not None:
            if self.scope['user'].is_anonymous:
                await self.close()
            self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
            self.account = self.scope['user'].account
            self.chat = await Chat.objects.aget(id=self.chat_id)
            self.room_group_name = "chat_%s" % self.chat_id
            await self.accept()
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Disconnecting from websocket."""

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            message = await Message.objects.acreate(text=content['message'], account=self.account)
            await self.add_message(chat=self.chat, message=message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message_echo",
                    "message": await self.serialize_message(message),
                },
            )
        return super().receive_json(content, **kwargs)

    async def chat_message_echo(self, event):
        await self.send_json(event)
