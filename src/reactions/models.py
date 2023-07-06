from django.db import models

from users.models import Account
from service.models import UUIDModel


class Reaction(UUIDModel):
    owner = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        verbose_name="Кто поставил",
        related_name="reactions",
    )
    reaction_option = models.ForeignKey(
        "ReactionItem",
        on_delete=models.CASCADE,
        verbose_name="Варианты реакций из определенного списка",
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Реакция пользователя на пост/сообщение"
        verbose_name_plural = "Реакции пользователя на пост/сообщение"


class ReactionItem(UUIDModel):
    image = models.ImageField(upload_to="uploads/reaction_images/")

    objects = models.Manager()

    class Meta:
        verbose_name = "Изображение реакции"
        verbose_name_plural = "Изображения реакций"
