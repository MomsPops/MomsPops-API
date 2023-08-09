from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Account
from users.serializers import AccountIdSerializer
from .models import Notification, NotificationAccount


class NotificationDetailSerializer(ModelSerializer):
    """
    Serializer for notifications.
    """

    class Meta:
        model = Notification
        fields = ("id", 'text', 'link', 'time_created', "sender")


class NotificationListSerializer(ModelSerializer):
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


class NotificationAccountListSerializer(ModelSerializer):
    notification = NotificationListSerializer(read_only=True)

    class Meta:
        modul = NotificationAccount
        fields = ("notification", )


class NotificationCreateSerializer(ModelSerializer):
    sender_id = serializers.CharField(required=False)
    accounts = AccountIdSerializer(many=True)

    class Meta:
        model = Notification
        fields = ("text", "link", "sender_id", "accounts")

    def save(self, **kwargs):
        kwargs.update(self.validated_data)
        sender = None
        if kwargs['sender_id'] is not None:
            sender = Account.objects.get(id=kwargs.pop('sender_id'))
        notification = Notification.objects.create(
            sender=sender,
            **kwargs
        )
        return notification
