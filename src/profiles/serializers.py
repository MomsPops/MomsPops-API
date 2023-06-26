from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Profile


class AbstractProfileSerializer(ModelSerializer):
    first_name = serializers.CharField(source="account.user.first_name")
    last_name = serializers.CharField(source="account.user.last_name")

    class Meta:
        model = Profile
        absract = True


class ProfileListSerializer(AbstractProfileSerializer):

    class Meta:
        model = Profile
        fields = ("bio", "get_photo_url", "get_profile_url", "first_name", "last_name", )


class ProfileDetailSerializer(AbstractProfileSerializer):

    class Meta:
        model = Profile
        fields = ("bio", "sex", "get_photo_url", "birthday", "tags", "status", "first_name", "last_name", )
