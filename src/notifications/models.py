from django.db import models

from service.models import TimeCreateModel, UUIDModel


class Notification(UUIDModel, TimeCreateModel):
    """
    Notification model.
    """

    text = models.TextField("Текст", max_length=300)
    link = models.URLField("Ссылка", blank=True)
    accounts = models.ManyToManyField(
        verbose_name="Аккаунт",
        to="users.Account",
        related_name="notifications",
        through="NotificationAccount",
    )
    sender = models.ForeignKey(
        verbose_name="sender",
        to="users.Account",
        on_delete=models.CASCADE,
        null=True
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
        verbose_name="Аккаунт",
        to="users.Account",
        on_delete=models.CASCADE
    )

    notification = models.ForeignKey(
        verbose_name="Уведомление",
        to=Notification,
        on_delete=models.CASCADE
    )
    viewed = models.BooleanField("Viewed", default=False, null=True)

    objects = models.Manager()
    # notification_account_manager = NotificationAccountManager()

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
