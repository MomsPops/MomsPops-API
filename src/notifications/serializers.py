from rest_framework.serializers import ModelSerializer

from .models import Notification


class NotificationDetailSerializer(ModelSerializer):
    """
    Serializer for notifications.
    """

    class Meta:
        model = Notification
        fields = ('id', 'text', 'link', 'time_created', "sender", "viewed")
