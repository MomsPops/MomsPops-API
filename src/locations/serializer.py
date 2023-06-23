from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import City   # , Region


class CitiesListSerializer(ModelSerializer):
    region_name = serializers.CharField(source="region.name")

    class Meta:
        model = City
        fields = ("name", "region_name")
