from rest_framework import serializers

from .models import Profile, Note


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

