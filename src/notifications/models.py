from django.db import models
from django.urls import reverse

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
        through="NotificationAccount"
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


class NotificationAccountManager(models.Manager):
    """
    Notification account manager all. Optimizes orm-queries.
    """
    def get(self, *args, **kwargs):
        return self.select_related().get(*args, **kwargs)

    def all(self):
        return self.select_related().all()

    def get_all_by_account(self, account):
        return self.select_related().filter(account=account)

    def select_related(self):
        return super().select_related("account", "notification")


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
    notification_account_manager = NotificationAccountManager()

    def view(self):
        """Sets viewed to `True`."""
        self.viewed = True
        self.save()

    def get_view_url(self):
        """Get url for view notification account."""
        return reverse('notifications_view', kwargs={'notification_account_id': self.pk})

    def __str__(self):
        return f'{self.account}: {self.notification}'

    class Meta:
        ordering = ('viewed', "notification__time_created")
        unique_together = ('account', 'notification')
        verbose_name = 'Уведомление для пользователя'
        verbose_name_plural = 'Уведомления для пользователей'
