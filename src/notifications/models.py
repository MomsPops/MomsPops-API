from django.db import models

from service.models import UUIDModel, TimeCreateModel


class Notification(UUIDModel, TimeCreateModel):
    """
    Notification model.
    """

    text = models.TextField(max_length=300)
    links = models.URLField(blank=True)
    account = models.ManyToManyField(
        to="users.Account",
        related_name="notifications",
        through='NotificationAccount'
    )

    objects = models.Manager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"


class NotificationAccount(models.Model):
    """
    Model for notification and account relation.
    """

    account = models.ForeignKey(
        to="users.Account",
        on_delete=models.CASCADE
    )

    notification = models.ForeignKey(
        to=Notification,
        on_delete=models.CASCADE
    )

    viewed = models.BooleanField(default=False)

    def is_viewed(self):
        """Sets viewed to `True`."""

        self.viewed = True
        self.save()

    def __str__(self):
        return f'{self.account}: {self.notification}'

    class Meta:
        unique_together = ('account', 'notification')
        verbose_name = 'Уведомление для пользователя'
        verbose_name_plural = 'Уведомления для пользователей'
