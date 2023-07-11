from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import Account
from service.models import UUIDModel


class ReactionLike(UUIDModel):
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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Реакция пользователя на пост/сообщение"
        verbose_name_plural = "Реакции пользователя на пост/сообщение"


class ReactionItem(UUIDModel):
    image = models.ImageField(upload_to="uploads/reaction_images/")

    objects = models.Manager()

    class Meta:
        verbose_name = "Изображение реакции"
        verbose_name_plural = "Изображения реакций"
