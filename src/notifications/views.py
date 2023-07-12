from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import NotificationAccount
from .serializers import NotificationAccountSerializer
from .permissions import RecepientOnlyPermission


class PersonalNotificationViewSet(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
    View set for notifications.
    """

    serializer_class = NotificationAccountSerializer
    permission_classes = (RecepientOnlyPermission,)

    def get_queryset(self):
        account = self.request.user.account
        return NotificationAccount.objects.filter(account=account)

    @action(detail=True, methods=['post'], permission_classes=[RecepientOnlyPermission])
    def viewed(self, request, **kwargs):
        """Mark notification as viewed."""

        notification = self.get_object()
        notification.is_viewed()
        return Response(NotificationAccountSerializer(notification).data)
