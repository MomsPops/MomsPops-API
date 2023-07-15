from rest_framework.serializers import ModelSerializer

from .models import Notification, NotificationAccount


class NotificationDetailSerializer(ModelSerializer):
    """
    Serializer for notifications.
    """

    class Meta:
        model = Notification
        fields = ("id", 'text', 'link', 'time_created', "sender")


class NotificationAccountDetailSerializer(ModelSerializer):
    notification = NotificationDetailSerializer(read_only=True)

    class Meta:
        model = NotificationAccount
        fields = ("notification", "viewed", "get_view_url")
