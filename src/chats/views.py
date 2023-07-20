from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatMessage, Group
from .serializers import ChatMessageSerializer, GroupListSerializer
from .filters import GroupFilter


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet fo chats.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        account = self.request.user.account
        return ChatMessage.objects.filter('chat__members__in' == account)


class GroupViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return GroupListSerializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        filters = GroupFilter(data=request.GET, queryset=self.get_queryset())
        queryset = filters.qs
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
