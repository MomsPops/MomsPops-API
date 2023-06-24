from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Account


class UserCreateSerializer(ModelSerializer):
    first_name = serializers.CharField(max_length=30, allow_null=False)
    last_name = serializers.CharField(max_length=30, allow_null=False)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class AccountCreateSerializer(ModelSerializer):
    region_name = serializers.CharField(max_length=100, source="city.region.name")
    city_name = serializers.CharField(max_length=100, source="city.name")
    user = UserCreateSerializer()

    class Meta:
        model = Account
        fields = ("user", "city_name", "region_name")


class AccountDetailSerializer(ModelSerializer):
    user = UserDetailSerializer()
    city_name = serializers.CharField(source="city.name")
    region_name = serializers.CharField(source="city.region.name")

    class Meta:
        model = Account
        fields = ("user", "city_name", "region_name")
