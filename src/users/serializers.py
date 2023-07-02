from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Account, User


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
    region_name = serializers.CharField(max_length=100, source="city.region.name",
                                        allow_null=True, allow_blank=True, required=False)
    city_name = serializers.CharField(max_length=100, source="city.name",
                                      allow_null=True, allow_blank=True, required=False)
    user = UserCreateSerializer()

    class Meta:
        model = Account
        fields = ("user", "city_name", "region_name")


class AccountDetailSerializer(ModelSerializer):
    user = UserDetailSerializer()
    city_name = serializers.CharField(source="city.name", allow_null=True, allow_blank=True, required=False)
    region_name = serializers.CharField(source="city.region.name", allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Account
        fields = ("user", "city_name", "region_name")


class BlockUserSerializer(ModelSerializer):
    username = serializers.CharField(source="account.user.username")

    class Meta:
        model = Account
        fields = ("username", )
