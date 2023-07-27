from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# from reactions.models import Reaction
from users.models import Account

from .models import Chat, Message
from .serializers import MessageSerializer


@database_sync_to_async
def is_in_chat_members(account: Account, chat: Chat):
    return account.chats.filter(pk=chat.id).exists()


@database_sync_to_async
def message_is_viewed(message: Message):
    return message.view()


@database_sync_to_async
def message_get_account(message: Message):
    return message.account


@database_sync_to_async
def add_message(chat: Chat, message: Message):
    return chat.messages.add(message)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    Consumer for chats.
    """

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account: Account | None = None
        self.chat: Chat | None = None

    async def connect(self):
        """Сonnection to websocket."""
        if self.scope.get('user', None) is not None:
            if self.scope['user'].is_anonymous:
                await self.close()
            self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
            self.chat = await Chat.objects.aget(id=self.chat_id)
            self.account = self.scope['user'].account
            self.group_name = f'chat_{self.chat_id}'
            if not await is_in_chat_members(self.account, self.chat):
                await self.close()
            await self.accept()
            await self.channel_layer.group_add(
                self.group_name, self.channel_name
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Disconnecting from websocket."""

        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "send_message":
            message = await Message.objects.acreate(text=content['message']["text"], account=self.account)
            await add_message(chat=self.chat, message=message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message": await self.serialize_message(message),
                },
            )

        if message_type == "change_message":
            message = await Message.objects.aget(pk=content["message"]["id"])
            if message.viewed is False and await message_get_account(message) == self.account:
                message.text = content["message"]["text"]
                await message.asave()
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "message": await self.serialize_message(message),
                    },
                )

        if message_type == "viewed":
            message = await Message.objects.aget(pk=content["message"]["id"])
            if message.viewed is False:
                await message_is_viewed(message)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "message": await self.serialize_message(message),
                    },
                )

    async def chat_message(self, event):
        await self.send_json(event)
