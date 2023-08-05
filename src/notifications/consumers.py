from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json

from django.db.transaction import atomic
from djangochannelsrestframework.decorators import action

from users.models import Account
from service.consumers import BaseConsumer
from .models import Notification, NotificationAccount
from .serializers import NotificationDetailSerializer, NotificationCreateSerializer, NotificationAccountListSerializer


@database_sync_to_async
def get_account_by_id(account_id: str):
    return Account.objects.get(id=account_id)


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    @atomic
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
            except Account.DoesNotExist:
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


class NotificationConsumer(BaseConsumer):
    notification_actions = {
        "notification_list": NotificationAccountListSerializer,
        "notification_create": NotificationCreateSerializer,
        "notification_detail": NotificationDetailSerializer,

    }

    async def send_notification(self, event) -> None:
        """Receive notification by a single account websocket."""
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_notification_serializer(self, action_kwargs, *args, **kwargs):
        return

    @database_sync_to_async
    def get_all_notifications_by_account(self, account):
        return [
            na for na in NotificationAccount.notification_account_manager.get_all_by_account(account)
        ]

    @action
    async def notification_list(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_reaction_serializer(
            action_kwarg=action_kwargs,
            instance=await self.get_all_notifications_by_account(self.account),
            many=True
        )
        serializer.is_valid(raise_exception=True)
        data = await self.get_serializer_data(serializer)
        data.update(action=action_kwargs['action'])
        await self.send_json(content=data)

    @action
    @atomic
    async def notification_create(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        create_serializer = await self.get_reaction_serializer(
            action_kwarg=action_kwargs,
            data=kwargs
        )
        create_serializer.is_valid(raise_exception=True)
        notification = await self.save_serializer(create_serializer)
        detail_serializer = await self.get_serializer_data(
            action_kwargs={
                "action": "notification_detail",
                "request_id": action_kwargs['request_id']
            },
            instance=notification
        )
        detail_serializer_data = await self.get_serializer_data(detail_serializer)
        for account in create_serializer.validated_data.get('accounts'):
            account_id = account.validated_data.get("account_id")
            account = await sync_to_async(Account.objects.get)(id=account_id)
            await self.channel_layer.group_send(
                str(account.id),
                {
                    "type": "update_messages",
                    "notification": detail_serializer_data
                }
            )
