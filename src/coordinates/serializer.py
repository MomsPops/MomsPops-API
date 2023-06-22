from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Coordinate


class CoordinateCreateSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Coordinate
        fields = "__all__"


class CoordinateListSerializer(ModelSerializer):

    class Meta:
        model = Coordinate
        fields = "__all__"
