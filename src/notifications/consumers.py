from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
import json

from users.models import Account
from .models import Notification
from .serializers import NotificationDetailSerializer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        """Redefine model to define custom instance attributes."""
        super().__init__(*args, **kwargs)
        self.user = None
        self.account_id = None

    async def connect(self) -> None:
        """On socket connection. Allowed only for authorized users."""
        if self.scope['user'] is None:
            await self.close()
        self.user = self.scope['user']
        self.account_id = str(self.user.account.id)
        await self.accept()
        await self.channel_layer.group_add(self.account_id, self.channel_name)

    async def disconnect(self, code) -> None:
        """On disconnect socket."""
        await self.channel_layer.group_discard(self.account_id, self.channel_name)
        await self.close(code)

    async def receive_json(self, content, **kwargs) -> None:
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
                sender = sync_to_async(Account.objects.get)(id=content['sender'])
            except Account.DoesNotExist as e:
                print(e)
                return
        notification = Notification(text=content["text"], sender=sender)
        serializer = NotificationDetailSerializer(instance=notification)
        for account_id in content['accounts']:
            account = sync_to_async(Account.objects.get)(account_id)
            await self.channel_layer.group_send(
                account_id, {"type": "send_notification", "message": serializer.data}
            )
            sync_to_async(notification.accounts.add)(account)

        sync_to_async(notification.save)()

    async def send_notification(self, event) -> None:
        """Receive notification by a single account websocket."""
        message = event['message']
        await self.send(text_data=json.dumps(message))
