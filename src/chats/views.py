import uuid

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import Account

from .models import Chat
from .serializers import ChatSerializer


class ChatViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for chats.
    """
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        account = self.request.user.account
        return Chat.chat_manager.get_all_chats_by_account(account)

    @action(methods=["post"],
            detail=False,
            url_path="create_stnd_chat/(?P<account_id>[^/.]+)",
            url_name="create_stnd_chat")
    def create_stnd_chat(self, request, account_id):
        sender = self.request.user.account
        reciever = get_object_or_404(Account, pk=account_id)
        new_chat = Chat.chat_manager.create_standart_chat(sender, reciever)
        return Response(ChatSerializer(new_chat).data)

    @action(methods=['post'],
            detail=False,
            url_path='create_cstm_chat/(?P<account_ids>[^/.]+)',
            url_name='create_custom_chat')
    def create_custom_chat(self, request, account_ids):
        # TODO 1) How to fetch list of uuids? 2) Use regexp for replase
        ids_list = account_ids.replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').split(',')
        accounts = [get_object_or_404(Account, pk=uuid.UUID(account_id).hex) for account_id in ids_list]
        sender = self.request.user.account
        accounts.append(sender)
        new_chat = Chat.chat_manager.create_custom_chat(accounts)
        return Response(ChatSerializer(new_chat).data)

    @action(methods=['post'], detail=True, url_path='leave_chat', url_name='leave_chat')
    def leave_chat(self, request, pk):
        chat = self.get_object()
        if chat.type == "CSTM":
            chat.leave_chat(request.user.account)
            return Response(f"You have left the chat {chat.id}.")
        return Response("You can't leave personal chat.")
