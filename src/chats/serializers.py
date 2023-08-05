from datetime import datetime

from django.core.files.base import ContentFile
from rest_framework import serializers
from uuid import uuid4

from rest_framework.exceptions import PermissionDenied

from users.models import Account
from .models import Chat, Message, MessageMedia, Group, get_messenger_object, message_types_choices
from users.serializers import AccountDetailSerializer


class MessageMediaCreateSerializer(serializers.ModelSerializer):
    media = serializers.CharField()

    class Meta:
        model = MessageMedia
        fields = ("media", "extension")


class MessageCreateSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=message_types_choices)
    account = serializers.HiddenField(default=serializers.CurrentUserDefault())
    medias = MessageMediaCreateSerializer(many=True)
    content_object = serializers.CharField()

    class Meta:
        model = Message
        fields = ("text", "account", "content_object", "source", "medias", "type")

    def save(self, **kwargs):
        kwargs.update(self.validated_data)
        content_object = get_messenger_object(
            type_=kwargs.get("type"),
            id_=kwargs.get('content_object')
        )
        if isinstance(content_object, Chat):
            for member in content_object.members.all():
                if member != kwargs['account']:
                    if not Account.objects.is_blocked_by_you(kwargs['account'], member):
                        raise PermissionDenied("You blocked this user")
                    elif not Account.objects.are_you_blocked(kwargs['account'], member):
                        raise PermissionDenied("User blocked you.")
        message = content_object.__class__.objects.add_message(
            obj=content_object,
            text=kwargs.get("text"),
            account=kwargs.get("account"),
            source=kwargs.get("source"),
        )
        for media in kwargs.get('medias', []):
            extension = media.get('extension')
            name = f"{str(uuid4())}.{extension}" if extension is not None else f"{str(uuid4())}"
            file = ContentFile(media['media'].encode(), name=name)
            MessageMedia.objects.create(
                message=message,
                media=file,
                extension=media.get('extension')
            )
        return message


class MessageDetailSerializer(serializers.ModelSerializer):
    account = AccountDetailSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "account",
            "text",
            "time_send",
            "time_update",

        )


class MessageUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    text = serializers.CharField(required=False)

    class Meta:
        model = Message
        fields = (
            "id",
            "text",

        )

    def update(self, instance, **kwargs):
        kwargs.update(self.validated_data)
        kwargs.pop('id')
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.time_update = datetime.now()
        print(instance.text, kwargs)
        print(self.validated_data)
        instance.save()
        return instance


class MessageListSerializer(serializers.ModelSerializer):
    account = AccountDetailSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "account",
            "text",
            "source",

        )


class ChatCreateSerializer(serializers.ModelSerializer):
    account = serializers.HiddenField(default=serializers.CurrentUserDefault())
    message = MessageCreateSerializer()
    account_id = serializers.CharField()

    class Meta:
        model = Chat
        fields = ("account_id", "message", "account")

    def save(self, **kwargs):
        kwargs.update(self.validated_data)
        kwargs.pop("account_id")
        chat = self.Meta.model.objects.create_chat(kwargs['members'])
        message = Chat.objects.add_message(
            obj=chat,
            account=kwargs['message']['account'],
            text=kwargs['message']['text'],
            source=kwargs['message'].get('source')
        )
        for media in kwargs['message'].get('medias'):
            extension = media.get('extension')
            name = f"{str(uuid4())}.{extension}" if extension is not None else f"{str(uuid4())}"
            file = ContentFile(media['media'].encode(), name=name)
            MessageMedia.objects.create(
                message=message,
                media=file,
                extension=media.get('extension')
            )
        return chat


class ChatListSerializer(serializers.ModelSerializer):
    messages = MessageListSerializer(many=True)

    class Meta:
        model = Chat
        fields = ("id", "members", "messages")


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = MessageDetailSerializer(many=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "members",
            "messages",

        )


class AccountIdSerializer(serializers.Serializer):
    account_id = serializers.CharField()


class GroupCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    accounts = AccountIdSerializer(required=False, default=[], many=True)
    photo = serializers.CharField(required=False)
    is_public = serializers.BooleanField(default=True)

    class Meta:
        model = Group
        fields = ("owner", "accounts", "photo", "is_public", "title")

    def save(self, **kwargs):
        kwargs.update(self.validated_data)
        kwargs.pop("accounts")
        photo = kwargs.get("photo")
        if photo is not None:
            photo = ContentFile(photo.encode(), name=f"{str(uuid4())}.png")
        group = self.Meta.model.objects.create_group(
            members=kwargs['members'],
            title=kwargs['title'],
            photo=photo,
            is_public=kwargs['is_public'],
            owner=kwargs['owner']
        )
        return group


class GroupListSerializer(serializers.ModelSerializer):
    messages = MessageListSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "get_photo_url",
            "title",

        )


class GroupDetailSerializer(serializers.ModelSerializer):
    messages = MessageDetailSerializer(many=True)
    owner = AccountDetailSerializer(read_only=True)
    members = AccountDetailSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "members",
            "messages",
            "get_photo_url",
            'is_public',
            "title",
            "owner",
            "time_created",

        )


class GroupUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    photo = serializers.CharField(required=False)
    is_public = serializers.BooleanField(required=False)
    title = serializers.CharField(required=False, max_length=255)

    class Meta:
        model = Group
        fields = (
            "id",
            "photo",
            'is_public',
            "title",

        )

    def update(self, instance, **kwargs):
        kwargs.update(self.validated_data)
        kwargs.pop('id')
        photo = kwargs.get("photo")
        if photo is not None:
            photo = ContentFile(photo.encode(), name=f"{str(uuid4())}.png")
        kwargs['photo'] = photo
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class GroupJoinSerializer(serializers.Serializer):
    group_id = serializers.CharField()
    account = serializers.HiddenField(default=serializers.CurrentUserDefault())


class GroupLeaveSerializer(serializers.Serializer):
    group_id = serializers.CharField()
    account = serializers.HiddenField(default=serializers.CurrentUserDefault())


class GroupInviteSerializer(serializers.Serializer):
    group_id = serializers.CharField()
    account_id = serializers.CharField()
