from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Coordinate


class CoordinateCreateSerializer(ModelSerializer):
    lat = serializers.FloatField(max_value=90, min_value=-90)
    lon = serializers.FloatField(max_value=179.9999999999999999999999999999, min_value=-180)

    class Meta:
        model = Coordinate
        fields = ("lat", "lon")


class CoordinateListSerializer(ModelSerializer):
    get_profile_url = serializers.URLField(source="account.profile.get_profile_url")

    class Meta:
        model = Coordinate
        fields = ('lat', "lon", "get_profile_url")
