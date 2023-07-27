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
            url_path="create_chat/(?P<account_id>[^/.]+)",
            url_name="create_chat")
    def create_chat(self, request, account_id):
        sender = self.request.user.account
        reciever = get_object_or_404(Account, pk=account_id)
        new_chat = Chat.chat_manager.create_standart_chat(sender, reciever)
        return Response(ChatSerializer(new_chat).data)
