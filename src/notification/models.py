from django.db import models
from uuid import uuid4


class Notification(models.Model):
    """
    Notification model.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    links = models.URLField()

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
