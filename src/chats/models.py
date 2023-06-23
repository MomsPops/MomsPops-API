from django.db import models
from service.models import UUIDModel, TimeCreateModel, TimeCreateUpdateModel, AccountForeignModel
from users.models import Account


def get_group_preview_file_path(instance, *_, **__):
    return instance.created.strftime("uploads/chat_previews/%Y/%m/%d/") + instance.id


def get_message_img_file_path(instance, *_, **__):
    return instance.created.strftime("uploads/message_img/%Y/%m/%d/") + instance.id


class Group(TimeCreateUpdateModel, UUIDModel):
    """
    Group model.
    """
    owner = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name="Создатель группы",
        related_name="owner_chat",
    )
    members = models.ManyToManyField(Account, blank=True)

    meeting_time = models.DateTimeField(verbose_name="Время встречи")
    img_preview = models.ImageField(upload_to=get_group_preview_file_path, null=True)


class Message(UUIDModel, TimeCreateModel, AccountForeignModel):
    """
    Message model.
    """
    chat = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name="Автор сообщения",
        related_name="messages",
    )
    text = models.TextField(max_length=500, verbose_name="Текст сообщения")
    img = models.ImageField(upload_to=get_message_img_file_path, null=True)
