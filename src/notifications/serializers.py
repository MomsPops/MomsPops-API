from rest_framework.serializers import ModelSerializer

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

    class Meta:
        model = NotificationAccount
        fields = ('id', 'notification', 'viewed')
