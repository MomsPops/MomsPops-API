from channels.db import database_sync_to_async

from chats.consumers import ChatConsumerMixin, GroupConsumerMixin, MessageConsumerMixin
from users.models import Account
from service.consumers import BaseConsumer


class ChatConsumer(
    ChatConsumerMixin,
    GroupConsumerMixin,
    MessageConsumerMixin,
    BaseConsumer
):

    @database_sync_to_async
    def get_accounts_by_ids(self, ids: list):
        accounts = [
            account for account in
            Account.objects.filter(id__in=ids)
        ]
        return accounts

    async def notify_accounts_by_chat_or_group(self, chat_or_group, data):
        members = await self.get_members(chat_or_group)
        for member in members:
            await self.channel_layer.group_send(
                str(member.id),
                {
                    "type": "update_messages",
                    "message": data
                }
            )

    async def notify_accounts_by_list(self, accounts: list, data: dict):
        for account in accounts:
            await self.channel_layer.group_send(
                str(account.id),
                {
                    "type": "update_messages",
                    "message": data
                }
            )
