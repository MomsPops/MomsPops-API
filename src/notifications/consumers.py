from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json

from users.models import Account
from .models import Notification
from .serializers import NotificationDetailSerializer


@database_sync_to_async
def get_account_by_id(account_id: str):
    return Account.objects.get(id=account_id)


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        """Redefine model to define custom instance attributes."""
        super().__init__(*args, **kwargs)
        self.user = None
        self.account = None
        self.account_id = None

    async def connect(self) -> None:
        """On socket connection. Allowed only for authorized users."""
        await self.accept()
        if self.scope['user'] is None:
            await self.close()
        self.user = self.scope['user']
        self.account = self.user.account
        self.account_id = str(self.account.id)
        await self.channel_layer.group_add(
            self.account_id,
            self.channel_name
        )

    async def disconnect(self, code) -> None:
        """On disconnect socket."""
        await self.channel_layer.group_discard(
            self.account_id,
            self.channel_name
        )
        await self.close(code)

    async def receive_json(self, content, *args, **kwargs) -> None:
        """
        Send notification to all account. First N.instance and its serializer are created.
        Then serializer data to all account groups.
        Receive data model:
        {
             "text": str | None,
             "accounts": list[str],
             "sender": str | None,
        }.
        """
        sender = None
        if content.get('sender') is not None:
            try:
                sender = await get_account_by_id(content['sender'])
            except Account.DoesNotExist as e:
                return
        notification = await Notification.objects.acreate(
            text=content["text"],
            sender=sender
        )
        serializer = NotificationDetailSerializer(instance=notification)
        for account_id in content['accounts']:
            account_id = str(account_id)
            account = await get_account_by_id(account_id)
            await sync_to_async(notification.accounts.add)(account)
            notification_data = serializer.data
            notification_data.update(sender=str(notification_data['sender']))
            notification_data.update(id=str(notification_data['id']))
            await self.channel_layer.group_send(
                account_id, {"type": "send_notification", "message": notification_data}
            )

    async def send_notification(self, event) -> None:
        """Receive notification by a single account websocket."""
        message = event['message']
        await self.send(text_data=json.dumps(message))
