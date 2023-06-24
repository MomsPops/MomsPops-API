from django.db import models

from service.models import UUIDModel, TimeCreateModel


class Notification(UUIDModel, TimeCreateModel):
    """
    Notification model.
    """
    text = models.TextField(max_length=300)
    is_active = models.BooleanField(default=True)
    links = models.URLField()
    account = models.ManyToManyField(
        to="users.Account",
        related_name="notifications"
    )

    objects = models.Manager()

    def deactivate(self):
        """Sets is_active to `False`"""
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
