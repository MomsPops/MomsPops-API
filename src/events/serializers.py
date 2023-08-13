from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import DateTimeField, ModelSerializer

from coordinates.models import Coordinate
from coordinates.serializers import CoordinateCreateSerializer
from users.serializers import AccountDetailSerializer

from .models import Event


class EventCreateSerializer(ModelSerializer):
    """
    Serializer for event creation.
    """
    coordinates = CoordinateCreateSerializer()
    event_start_time = DateTimeField()
    event_end_time = DateTimeField()

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "coordinates",
            "event_start_time",
            "event_end_time"
        ]

    def create(self, validated_data):
        if "coordinates" not in self.initial_data:
            user = CurrentUserDefault()
            coordinates = user.account.coordinate
            event = Event.objects.create(**validated_data)
            event.coordinates = coordinates
            return event
        coordinates = validated_data.pop("coordinates")
        event = Event.objects.create(**validated_data)
        Coordinate.objects.create(lat=coordinates["lat"], lon=coordinates["lon"], source=event)
        return event


class EventDetailSerializer(ModelSerializer):
    """
    Serializer for event detail.
    """
    creator = AccountDetailSerializer(read_only=True)
    coordinates = CoordinateCreateSerializer()
    event_start_time = DateTimeField()
    event_end_time = DateTimeField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "creator",
            "group",
            "event_start_time",
            "event_end_time",
            "coordinates",
        ]
