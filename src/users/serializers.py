from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from .models import Account, User, FriendshipRequest


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
        fields = ("id", "user", "city_name", "region_name")


class BlockUserCreateSerializer(ModelSerializer):
    username = serializers.CharField(source="account.user.username")

    class Meta:
        model = Account
        fields = ("username", )


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)


class FriendshipRequestListSerializer(ModelSerializer):
    to_account = AccountDetailSerializer()
    from_account = AccountDetailSerializer()

    class Meta:
        model = FriendshipRequest
        fields = ("id", "to_account", "from_account")


class FriendshipRequestCreateSerializer(ModelSerializer):
    to_account_id = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FriendshipRequest
        fields = ("user", "to_account_id")

    def save(self, **kwargs):
        kwargs.update(self.validated_data)
        to_account = Account.objects.get(id=kwargs['to_account_id'])
        if kwargs['user'].account.incoming_requests.filter(from_account=to_account).exists():
            raise ValidationError("Cannot send friendship request, place accept incoming one.")
        if kwargs['user'].account.friends.filter(id=kwargs['to_account_id']).exists():
            raise ValidationError("Account is already a friend.")
        with transaction.atomic():
            obj = FriendshipRequest.friendship_request_manager.create_friendship_request(
                from_account=kwargs['user'].account,
                to_account=to_account
            )
            return obj
