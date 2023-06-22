from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Account


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")


class AccountCreateSerializer(ModelSerializer):
    country_name = serializers.CharField(max_length=100, source="city.country.name")
    city_name = serializers.CharField(max_length=100, source="city.name")
    user = UserCreateSerializer()

    class Meta:
        model = Account
        fields = ("user", "city_name", "country_name")


class AccountDetailSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
