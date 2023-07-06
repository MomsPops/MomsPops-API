from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import City, Region


class CityListSerializer(ModelSerializer):
    region_name = serializers.CharField(source="region.name")

    class Meta:
        model = City
        fields = ("name", "region_name")


class CityDetailSerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


class LocationListSerializer(ModelSerializer):
    cities = CityDetailSerializer(many=True)

    class Meta:
        model = Region
        fields = ("id", "name", "cities")
