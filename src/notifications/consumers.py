from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async
from django.db.transaction import atomic
from asgiref.sync import sync_to_async
import json
from users.models import Account

from service.consumers import BaseConsumer
from .models import NotificationAccount
from .serializers import NotificationDetailSerializer, NotificationCreateSerializer, NotificationAccountListSerializer


class NotificationConsumer(BaseConsumer):
    notification_actions = {
        "notification_list": NotificationAccountListSerializer,
        "notification_create": NotificationCreateSerializer,
        "notification_detail": NotificationDetailSerializer,

    }

    @database_sync_to_async
    def get_notification_serializer(self, action_kwargs, *args, **kwargs):
        return

    @database_sync_to_async
    def get_all_notifications_by_account(self, account):
        return [
            na for na in NotificationAccount.notification_account_manager.get_all_by_account(account)
        ]

    @action()
    async def notification_list(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_notification_serializer(
            action_kwarg=action_kwargs,
            instance=await self.get_all_notifications_by_account(self.account),
            many=True
        )
        serializer.is_valid(raise_exception=True)
        data = await self.get_serializer_data(serializer)
        data.update(action=action_kwargs['action'])
        await self.send_json(content=data)

    @action()
    @atomic
    async def notification_create(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        create_serializer = await self.get_notification_serializer(
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
            await sync_to_async(notification.accounts.add)(account)
            await self.channel_layer.group_send(
                str(account.id),
                {
                    "type": "update_messages",
                    "notification": detail_serializer_data
                }
            )

    async def send_notification(self, event) -> None:
        """Receive notification by a single account websocket."""
        message = event['message']
        await self.send(text_data=json.dumps(message))
