from rest_framework import mixins, viewsets, views, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import NotificationAccount
from .serializers import NotificationAccountDetailSerializer


class NotificationAccountViewSet(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = NotificationAccount.notification_account_manager.all()
    lookup_field = "id"
    lookup_url_kwarg = "notification_account_id"

    def get_serializer(self, *args, **kwargs):
        return NotificationAccountDetailSerializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        notification_accounts = NotificationAccount.notification_account_manager.get_all_by_account(
            request.user.account
        )
        serializer = self.get_serializer(notification_accounts, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def view(self, request, notification_account_id: str):
        notification_account = self.get_object()
        if not notification_account.viewed:
            notification_account.view()
            return Response(f"Notification {notification_account_id} viewed.")
        return Response(f"Notification {notification_account_id} is already viewed.")
