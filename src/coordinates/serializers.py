from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Coordinate


class CoordinateCreateSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Coordinate
        fields = "__all__"


class CoordinateListSerializer(ModelSerializer):
    get_profile_url = serializers.URLField(source="account.profile.get_profile_url")

    class Meta:
        model = Coordinate
        fields = ('lat', "lon", "get_profile_url")
