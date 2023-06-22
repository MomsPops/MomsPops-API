from django.db import models
from uuid import uuid4
from users.models import Account


def get_chat_preview_file_path(instance, filename):
    return instance.created.strftime("uploads/chat_previews/%Y/%m/%d/") + instance.id


def get_message_img_file_path(instance, filename):
    return instance.created.strftime("uploads/message_img/%Y/%m/%d/") + instance.id


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    owner = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name="Создатель чата",
        related_name="owner_chat",
    )
    members = models.ManyToManyField(Account, blank=True)

    meeting_time = models.DateTimeField(verbose_name="Время встречи")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    img_preview = models.ImageField(upload_to=get_chat_preview_file_path, null=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name="Автор сообщения",
        related_name="messages",
    )
    text = models.TextField(max_length=500, verbose_name="Текст сообщения")
    img = models.ImageField(upload_to=get_message_img_file_path, null=True)
    created = models.DateTimeField(auto_now_add=True)
