from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile, Note
from users.serializers import UserDetailSerializer, UserListSerializer

# ================================= PROFILES ================================= #

User = get_user_model()


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ("photo", "city", "user")


# ================================= NOTES ================================= #

class NoteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

    def validate_text(self, value):
        return value[:100] + "..."


class NoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class NoteCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = "__all__"
