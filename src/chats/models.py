from django.db import models
from service.models import (
    UUIDModel,
    TimeCreateModel,
    TimeCreateUpdateModel,
    AccountForeignModel,
)
from users.models import Account
from coordinates.models import Coordinate


def get_group_preview_file_path(instance, *_, **__):
    return instance.created.strftime("uploads/chat_previews/%Y/%m/%d/") + instance.id


def get_message_img_file_path(instance, *_, **__):
    return instance.created.strftime("uploads/message_img/%Y/%m/%d/") + instance.id


class ChatType(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название чата")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип чата"
        verbose_name_plural = "Тип чата"


class Chat(TimeCreateUpdateModel, UUIDModel):
    """
    Chat model.
    """

    type = models.ForeignKey(
        ChatType,
        related_name="chats",
        on_delete=models.PROTECT,
        verbose_name="Тип чата",
    )
    owner = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        verbose_name="Создатель группы",
        related_name="owner_chat",
        null=True,
        blank=True,
    )
    members = models.ManyToManyField(Account, blank=True)

    meeting_time = models.DateTimeField(verbose_name="Время встречи", blank=True, null=True)
    lacations_coordinates = models.ForeignKey(
        Coordinate,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Координаты",
    )
    img_preview = models.ImageField(upload_to=get_group_preview_file_path, null=True)

    def __str__(self):
        return f"{self.type.title}:{self.id}"

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class Message(UUIDModel, TimeCreateModel, AccountForeignModel):
    """
    Message model. Fields: id, time_created,
    """

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name="Автор сообщения",
        related_name="messages",
    )
    text = models.TextField(max_length=500, verbose_name="Текст сообщения")
    img = models.ImageField(
        upload_to=get_message_img_file_path, null=True
    )  # TODO: added extra models FK
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Account: {self.account.id}, viewed: {self.viewed}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
