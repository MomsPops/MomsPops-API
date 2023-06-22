from django.db import models
from uuid import uuid4


class Notification(models.Model):
    """
    Notification model.
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    text = models.TextField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    links = models.URLField()

    objects = models.Manager()

    def deactivate(self):
        """Sets is_active to `False`"""
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
