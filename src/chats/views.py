from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet fo chats.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        account = self.request.user.account
        return ChatMessage.objects.filter('chat__members__in' == account)
