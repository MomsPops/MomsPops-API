from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Group, Chat, ChatMessage, GroupMessage, Message
from reactions.serializers import ReactionSerializer
from users.serializers import AccountDetailSerializer


class MessageSerializer(ModelSerializer):
    account_id = serializers.CharField(source="account.id")
    username = serializers.CharField(source="account.user.username")
    reactions = ReactionSerializer()

    class Meta:
        model = Message
        fields = ("id", "account_id", "username", "text", "viewed", "reactions")
        related_fields = ["account"]


class GroupSerializer(ModelSerializer):
    owner = AccountDetailSerializer()
    members = AccountDetailSerializer(many=True)

    class Meta:
        model = Group
        fields = ("id", "title", "owner", "members", "img_preview")


class ChatSerializer(ModelSerializer):
    members = AccountDetailSerializer(many=True)

    class Meta:
        model = Chat
        fields = ("id", "type", "members")
