from rest_framework.serializers import ModelSerializer

from coordinates.models import Coordinate
from coordinates.serializers import CoordinateCreateSerializer
from users.serializers import AccountDetailSerializer

from .models import Event
from .validators import EventValidator


class EventCreateSerializer(ModelSerializer):
    """
    Serializer for event creation.
    """
    coordinate = CoordinateCreateSerializer()

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "coordinate",
            "time_started",
            "time_finished"
        ]
        validators = [EventValidator()]

    def create(self, validated_data):
        coordinate = validated_data.pop("coordinate")
        event = Event.objects.create(**validated_data)
        event_coordinate = Coordinate.objects.create(lat=coordinate["lat"], lon=coordinate["lon"])
        event.coordinate = event_coordinate
        event.save()
        return event


class EventDetailSerializer(ModelSerializer):
    """
    Serializer for event detail.
    """
    creator = AccountDetailSerializer(read_only=True)
    coordinate = CoordinateCreateSerializer()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "creator",
            "group",
            "time_started",
            "time_finished",
            "coordinate",
        ]
