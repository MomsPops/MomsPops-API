from rest_framework.serializers import ModelSerializer

from users.serializers import AccountDetailSerializer

from .models import Notification, NotificationAccount


class NotificationSerializer(ModelSerializer):
    """
    Serializer for notifications.
    """

    class Meta:
        model = Notification
        fields = ('id', 'text', 'links', 'time_created')


class NotificationAccountSerializer(ModelSerializer):
    """
    Serializer for personal notifications.
    """

    notification = NotificationSerializer(read_only=True)
    account = AccountDetailSerializer(read_only=True)

    class Meta:
        model = NotificationAccount
        fields = ('id', 'account', 'notification', 'viewed')
