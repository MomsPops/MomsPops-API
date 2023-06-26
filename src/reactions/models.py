from django.db import models

from service.models import UUIDModel
from users.models import Account
from chats.models import Message


class Reaction(UUIDModel):
    """
    Reaction model.
    """
    owner = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name="Кто поставил",
        related_name="reactions"
    )
    item = models.ForeignKey(
        "ReactionItem",
        on_delete=models.CASCADE,
        verbose_name="Варианты реакций из определенного списка"
    )
    message: Message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение"
    )

    class Meta:
        verbose_name = "Реакция пользователя на пост/сообщение"
        verbose_name_plural = "Реакции пользователя на пост/сообщение"


def reaction_item_path(instance, *_, **__) -> str:
    return "uploads/reaction_images/" + instance.name   # type: ignore


class ReactionItem(UUIDModel):
    """
    Reaction item model.
    """
    image = models.ImageField(upload_to=reaction_item_path, unique=True)
    name = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Изображение реакции"
        verbose_name_plural = "Изображения реакций"
        unique_together = ("image", "name")
