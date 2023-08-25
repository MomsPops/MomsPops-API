from typing import Any

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from chats.models import Group
from coordinates.models import Coordinate
from service.models import TimeCreateUpdateModel, UUIDModel
from users.models import Account


class EventManager(models.Manager):
    """
    Custom manager for events.
    """
    def get(self, *args: Any, **kwargs: Any) -> Any:
        return super().select_related("creator", "group", "coordinate").get(*args, **kwargs)

    def all(self):
        return super().select_related("creator", "group", "coordinate").all()


class Event(UUIDModel, TimeCreateUpdateModel):
    """
    Models for events.
    """
    title = models.CharField("Название события", max_length=100)
    description = models.TextField("Описание события", max_length=500)
    creator = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        related_name="events",
        verbose_name="Создатель события",
        null=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="events",
        verbose_name="Группа события",
        null=True
    )
    coordinate = models.ForeignKey(
        Coordinate,
        on_delete=models.SET_NULL,
        related_name="events",
        verbose_name="Координаты события",
        null=True
    )
    time_started = models.DateTimeField("Время начала события")
    time_finished = models.DateTimeField("Время завершения события")

    objects = EventManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


@receiver(post_save, sender=Event)
def group_for_event_create(sender, instance, created, **kwargs):
    if created:
        Group.objects.create_group(
            title=instance.title,
            account=instance.creator
        )
