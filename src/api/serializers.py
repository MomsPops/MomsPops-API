from rest_framework.serializers import ModelSerializer

from notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    """
    Serializer for notifications.
    """

    class Meta:
        model = Notification
        fields = ('id', 'is_active', 'text', 'links', 'time_created')
