from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from rest_framework.exceptions import NotFound, PermissionDenied
from django.conf import settings
from typing import Union


class MessengerManager(models.Manager):
    def get(self, *args, **kwargs):
        try:
            obj = (
                super()
                .prefetch_related("messages", "members", "messages__account", "messages__medias")
                .get(*args, **kwargs)
            )
            return obj
        except self.model.DoesNotExist:
            raise NotFound()

    def filter(self, **kwargs):
        return (
            super()
            .prefetch_related("messages", "members", "messages__account")
            .filter(**kwargs)
        )

    def all(self):
        return (
            super()
            .prefetch_related("messages", "members", "messages__account")
            .all()
        )

    def add_message_instance(self, obj, message):
        obj.last_message = message
        obj.save()

    def add_message(self, obj, text: str, account, source):
        if obj.members.filter(id=account.id).exists():
            message = Message(
                content_object=obj,
                text=text,
                account=account,
                source=source
            )
            message.save()
            obj.last_message = message
            obj.save()
            return message

        raise PermissionDenied()

    def all_account_in_account_chats(self, account):
        members = []
        for ac in account.chats.all():
            for member in ac.members.all():
                if member != account:
                    members.append(member)
        return members


class ChatManager(MessengerManager):

    def create_chat(self, members: list):
        chat = Chat()
        chat.save()
        chat.members.add(*members)
        return chat

    def all_account_chats(self, account):
        return account.chats.all()


class Chat(models.Model):
    members = models.ManyToManyField(
        "users.Account",
        verbose_name="Members",
        related_name="chats",
    )
    messages = GenericRelation("Message", object_id_field="id")
    last_message = models.OneToOneField("Message", on_delete=models.SET_NULL, null=True, blank=True)

    objects = ChatManager()


class GroupManager(MessengerManager):

    def get(self, *args, **kwargs):
        try:
            obj = (
                super()
                .prefetch_related(
                    "messages", "members", "messages__account",
                    "messages__medias", "owner",
                )
                .get(*args, **kwargs)
            )
            return obj
        except self.model.DoesNotExist:
            raise NotFound()

    def create_group(
            self,
            members: list,
            title: str,
            owner,
            photo: ContentFile | None = None,
            is_public: bool = True,
    ):
        group = Group(
            title=title,
            photo=photo,
            is_public=is_public,
            owner=owner
        )
        group.save()
        group.members.add(*members)
        return group

    def all_account_groups(self, account):
        return account.groups.all()


class Group(models.Model):
    members = models.ManyToManyField(
        "users.Account",
        verbose_name="Members",
        related_name="group_chats",
    )
    is_public = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_created=True, auto_now=True)
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        to="users.Account",
        on_delete=models.CASCADE,
        related_name="own_groups"
    )
    photo = models.ImageField(null=True, upload_to="uploads/groups/")
    messages = GenericRelation("Message", object_id_field="id")

    objects = GroupManager()

    def get_photo_url(self):
        if self.photo:
            return settings.MEDIA_URL + self.photo.url
        return settings.MEDIA_URL + "uploads/groups/default.png"


class MessageManager(models.Manager):
    def get(self, *args, **kwargs):
        try:
            obj = (
                super()
                .prefetch_related("account", "content_object")
                .get(*args, **kwargs)
            )
            return obj
        except self.model.DoesNotExist:
            raise NotFound()

    def check_member_permissions(self, obj, account):
        if account not in obj.members.all():
            raise PermissionDenied("Account is not the member of the chat or group.")


class Message(models.Model):
    content_object = GenericForeignKey(ct_field="content_type", fk_field="id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    account = models.ForeignKey("users.Account", on_delete=models.CASCADE)
    text = models.TextField(max_length=2000, null=True)
    source = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    viewed = models.BooleanField(default=False)
    time_send = models.DateTimeField("Time send", auto_created=True, auto_now=True)
    time_update = models.DateTimeField("Time update", null=True, auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return self.text


def media_upload_to(odj, *args, **kwargs):
    return f"uploads/{odj.message.id}"


class MessageMedia(models.Model):
    media = models.FileField("Media", upload_to=media_upload_to)
    message = models.ForeignKey("Message", on_delete=models.CASCADE, related_name="medias")
    extension = models.CharField(max_length=20, null=True)

    objects = models.Manager()


message_types_models = {
    "chat": Chat,
    "group": Group,

}

message_types_choices = (
    ('chat', "chat"),
    ("group", "group"),

)


Messenger = Union[Chat, Group]


def get_messenger_object(type_: str, id_: str) -> Messenger:
    content_object_model = message_types_models.get(type_)
    if content_object_model is None:
        raise ValueError
    content_object = content_object_model.objects.get(id=id_)
    return content_object
