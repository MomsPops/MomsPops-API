from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import Serializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from users.models import Account
from .permissions import check_is_group_owner, check_is_group_public
from .serializers import (
    ChatListSerializer, ChatCreateSerializer, ChatDetailSerializer,
    GroupListSerializer, GroupCreateSerializer, GroupDetailSerializer, GroupUpdateSerializer,
    MessageDetailSerializer, MessageCreateSerializer, MessageUpdateSerializer, GroupJoinSerializer,
    GroupLeaveSerializer, GroupInviteSerializer
)
from .models import Chat, get_messenger_object, Group, Message


class MessengerGenericConsumerMixin:
    @database_sync_to_async
    def get_members(self, chat_or_group):
        return [m for m in chat_or_group.members.all()]


class ChatConsumerMixin(MessengerGenericConsumerMixin,
                        ObserverModelInstanceMixin,
                        GenericAsyncAPIConsumer):
    chat_actions = {
        "chat_create": ChatCreateSerializer,
        "chat_list": ChatListSerializer,
        "chat_detail": ChatDetailSerializer,

    }

    @database_sync_to_async
    def get_chat_serializer(self, action_kwargs: dict | None = None, *args, **kwargs) -> Serializer:
        action_ = action_kwargs.get("action")
        if action_ not in self.chat_actions:
            raise AssertionError(f"Please define action {action_}")
        serializer_class = self.chat_actions[action_]
        return serializer_class(*args, **kwargs)

    @action()
    async def chat_list(self, **kwargs):
        queryset = await sync_to_async(Chat.objects.all_account_chats)(self.account)
        serializer = await self.get_chat_serializer(action_kwargs=kwargs, instance=queryset, many=True)
        data = await self.get_serializer_data(serializer)
        data.update(action=kwargs['action'])
        await self.send_json(
            content=data
        )

    @action()
    async def chat_create(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_chat_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
            context={"request": await self.imitate_request(user=self.account)}
        )
        serializer.is_valid(raise_exception=True)
        account_id = serializer.validated_data.get('account_id')
        if account_id == self.account_id:
            await self.send_json({"detail": "Other user required"})
        else:
            account = await sync_to_async(Account.objects.get)(pk=account_id)
            if not Account.objects.is_blocked_by_you(kwargs['account'], account):
                raise PermissionDenied("You blocked this user")
            elif not Account.objects.are_you_blocked(kwargs['account'], account):
                raise PermissionDenied("User blocked you.")
            if account in await self.all_accounts_chatting(self.account):
                await self.send_json({"detail": "Chat already exists."})
            else:
                accounts = [self.account, account]
                chat = await self.save_serializer(serializer, members=accounts)
                last_message_serializer = await self.get_serializer(
                    action_kwargs={"action": "message_detail"},
                    instance=chat.last_message
                )
                data = await self.get_serializer_data(last_message_serializer)
                data.update(action=action_kwargs['action'])
                await self.notify_accounts_by_list(
                    accounts=accounts,
                    data=data
                )


class GroupConsumerMixin(MessengerGenericConsumerMixin,
                         ObserverModelInstanceMixin,
                         GenericAsyncAPIConsumer):
    group_actions = {
        "group_create": GroupCreateSerializer,
        "group_list": GroupListSerializer,
        "group_detail": GroupDetailSerializer,
        "group_update": GroupUpdateSerializer,
        "group_join": GroupJoinSerializer,
        "group_leave": GroupLeaveSerializer,
        "group_invite": GroupInviteSerializer,

    }

    @database_sync_to_async
    def get_group_serializer(self, action_kwargs: dict | None = None, *args, **kwargs) -> Serializer:
        action_ = action_kwargs.get("action")
        if action_ not in self.group_actions:
            raise AssertionError(f"Please define action {action_}")
        serializer_class = self.group_actions[action_]
        return serializer_class(*args, **kwargs)

    @action()
    async def group_create(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_group_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
            context={"request": await self.imitate_request(user=self.account)}
        )
        serializer.is_valid(raise_exception=True)
        accounts_ids = [i['account_id'] for i in serializer.validated_data.get('accounts')]
        if self.account_id in accounts_ids:
            await self.send_json({"detail": "Other users required"})
        else:
            accounts = await self.get_accounts_by_ids(accounts_ids)
            if len(accounts) != len(accounts_ids):
                await self.send_json({"detail": "Some of users are not found."})
                return
            accounts.append(self.account)
            group = await self.save_serializer(serializer, members=accounts)
            group_detail_serializer = await self.get_serializer(
                action_kwargs={
                    "request_id": action_kwargs['request_id'],
                    "action": "group_detail"
                },
                instance=group
            )
            data = await self.get_serializer_data(group_detail_serializer)
            data.update(action=action_kwargs['action'])
            await self.notify_accounts_by_list(
                accounts=accounts,
                data=data
            )

    @action()
    async def group_update(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_group_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
            context={"request": await self.imitate_request(user=self.account)}
        )
        serializer.is_valid(raise_exception=True)
        group = await sync_to_async(Group.objects.get)(id=serializer.validated_data.get('id'))
        check_is_group_owner(self.account, group)
        group = await self.update_serializer(serializer, instance=group)
        group_detail_serializer = await self.get_serializer(
            action_kwargs={
                "request_id": action_kwargs['request_id'],
                "action": "group_detail"
            },
            instance=group
        )
        data = await self.get_serializer_data(group_detail_serializer)
        data.update(action=action_kwargs['action'])
        await self.notify_accounts_by_chat_or_group(
            chat_or_group=group,
            data=data,
            context={"request": await self.imitate_request(user=self.account)}
        )

    @action()
    async def group_join(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_group_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
        )
        serializer.is_valid(raise_exception=True)
        group = await sync_to_async(Group.objects.get)(id=serializer.validated_data.get('id'))
        check_is_group_public(group)
        if self.account in await self.get_members(group):
            raise PermissionDenied("Group")
        data = await self.get_serializer_data(serializer)
        data.update(action=action_kwargs['action'])
        await self.notify_accounts_by_chat_or_group(
            chat_or_group=group,
            data=data
        )

    @action()
    async def group_leave(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_group_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
        )
        serializer.is_valid(raise_exception=True)
        group = await sync_to_async(Group.objects.get)(id=serializer.validated_data.get('group_id'))
        if self.account not in await self.get_members(group):
            raise PermissionDenied("You are not in the group.")
        data = await self.get_serializer_data(serializer)
        data.update(action=action_kwargs['action'])
        await self.notify_accounts_by_chat_or_group(
            chat_or_group=group,
            data=data
        )

    @action()
    async def group_invite(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_group_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
        )
        serializer.is_valid(raise_exception=True)
        group = await sync_to_async(Group.objects.get)(id=serializer.validated_data.get('account_id'))
        check_is_group_owner(self.account, group)
        account = await sync_to_async(Group.objects.get)(id=serializer.validated_data.get('group_id'))
        if account in await self.get_members(group):
            raise PermissionDenied("Account is already in the group.")
        data = await self.get_serializer_data(serializer)
        data.update(action=action_kwargs['action'])
        await self.notify_accounts_by_chat_or_group(
            chat_or_group=group,
            data=data
        )


class MessageConsumerMixin(ObserverModelInstanceMixin,
                           GenericAsyncAPIConsumer):
    message_actions = {
        "send_message": MessageCreateSerializer,
        "message_detail": MessageDetailSerializer,
        "message_update": MessageUpdateSerializer,

    }

    @database_sync_to_async
    def get_message_serializer(self, action_kwargs: dict | None = None, *args, **kwargs) -> Serializer:
        action_ = action_kwargs.get("action")
        if action_ not in self.message_actions:
            raise AssertionError(f"Please define action {action_}")
        serializer_class = self.message_actions[action_]
        return serializer_class(*args, **kwargs)

    @action()
    async def message_update(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        serializer = await self.get_message_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
            context={"request": await self.imitate_request(user=self.account)}
        )
        serializer.is_valid(raise_exception=True)
        message = await sync_to_async(Message.objects.get)(id=serializer.validated_data.get('id'))
        if message.account != self.account:
            await self.send_json({"detail": "You are not message sender."})
        else:
            message = await self.update_serializer(serializer, instance=message)
            message_detail_serializer = await self.get_message_serializer(
                action_kwargs={
                    "request_id": action_kwargs['request_id'],
                    "action": "message_detail"
                },
                instance=message
            )
            data = await self.get_serializer_data(message_detail_serializer)
            data.update(action=action_kwargs['action'])
            await self.notify_accounts_by_chat_or_group(
                chat_or_group=message.content_object,
                data=data
            )

    @action()
    async def message_send(self, **kwargs):
        action_kwargs = self.prepare_data(**kwargs)
        create_serializer = await self.get_message_serializer(
            action_kwargs=action_kwargs,
            data=kwargs,
            context={"request": await self.imitate_request(user=self.account)}
        )
        create_serializer.is_valid(raise_exception=True)
        content_object = await sync_to_async(get_messenger_object)(
            id_=create_serializer.validated_data.get('content_object'),
            type_=create_serializer.validated_data.get("type")
        )
        message = await self.save_serializer(create_serializer)
        if message is None:
            await self.send_json({"detail": "You are not is the chat."})
        else:
            detail_serializer = await self.get_message_serializer(
                action_kwargs={
                    "request_id": action_kwargs['request_id'],
                    "action": "message_detail"
                },
                instance=message
            )
            data = await self.get_serializer_data(detail_serializer)
            data.update(action=action_kwargs['action'])
            await self.notify_accounts_by_chat_or_group(
                chat_or_group=content_object,
                data=data
            )
