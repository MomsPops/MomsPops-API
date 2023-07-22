from rest_framework import serializers

from reactions.serializers import ReactionSerializer
from users.serializers import AccountDetailSerializer

from .models import Chat, ChatMessage, Message, MessageMediaFile


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
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('type', 'members', 'time_created', 'time_updated', 'messages')


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages from certain chat.
    """
    chat = ChatSerializer()
    message = MessageSerializer(many=True)

    class Meta:
        model = ChatMessage
        fields = ('chat', 'message')
