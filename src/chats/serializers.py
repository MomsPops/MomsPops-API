from rest_framework import serializers

from reactions.serializers import ReactionSerializer
from users.serializers import AccountDetailSerializer
from profiles.serializers import ProfileListSerializer
from .models import Chat, ChatMessage, Message, MessageMediaFile, Group


class MessageMediaFileSerializer(serializers.ModelSerializer):
    """
    Serializer for media files of messages.
    """
    img = serializers.ImageField

    class Meta:
        model = MessageMediaFile
        fields = ('img', 'time_created')


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages.
    """
    account = AccountDetailSerializer()
    media_files = MessageMediaFileSerializer(many=True)
    reactions = ReactionSerializer(many=True)

    class Meta:
        model = Message
        fields = ('account', 'text', 'media_files', 'available', 'viewed', 'reactions', 'time_created')


class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for chats.
    """
    members = AccountDetailSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('type', 'members', 'time_created', 'time_updated')


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages from certain chat.
    """
    chat = ChatSerializer()
    message = MessageSerializer(many=True)

    class Meta:
        model = ChatMessage
        fields = ('chat', 'message')


class GroupListSerializer(serializers.ModelSerializer):
    owner = ProfileListSerializer(source="owner.profile")

    class Meta:
        model = Group
        fields = ("title", "owner", "get_image_preview_url", )


class GroupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('title', "img_preview", "coordinate")


class GroupDetailSerializer(serializers.ModelSerializer):
    owner = ProfileListSerializer(source="owner.profile")

    class Meta:
        model = Group
        fields = ("title", "owner", "get_image_preview_url", )
