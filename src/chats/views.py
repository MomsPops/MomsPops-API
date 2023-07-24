from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from http import HTTPStatus

from .models import ChatMessage, Group
from .serializers import ChatMessageSerializer, GroupListSerializer, GroupCreateSerializer, GroupDetailSerializer
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
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return GroupListSerializer(*args, **kwargs)
        elif self.action == "create":
            return GroupCreateSerializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_group = serializer.save(owner=request.user.account)
        return Response(GroupDetailSerializer(new_group).data, status=HTTPStatus.CREATED)

    def list(self, request, *args, **kwargs):
        filters = GroupFilter(data=request.GET, queryset=self.get_queryset())
        queryset = filters.qs
        distance = request.GET.get("distance")
        if distance is not None:
            if request.user.account.coordinate is None:
                return Response([])
            queryset = request.user.account.coordinate.__class__.coordinate_manager.all_near(
                source=request.user.account,
                distance=int(distance),
                queryset=queryset
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
