from django.db import models
from django.contrib.auth.models import User

from service.models import UUIDModel

from locations.models import City
from notifications.models import Notification


class AccountManager(models.Manager):
    """
    Custom account manager.
    """

    def create_account(self, city_name: str, country_name: str, user: dict[str, str]):
        city = City.objects.get(name=city_name, country__name=country_name)
        new_user = User.objects.create_user(**user)
        new_account = self.model(user=new_user, city=city)
        new_account.save(using=self._db)
        return new_account


class Account(UUIDModel):
    """
    Account model.
    """
    user: User = models.OneToOneField(
        User, related_name="account", on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True, null=True, verbose_name="Биография")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="День рождения")
    photo = models.ImageField(
        upload_to="uploads/account_img/", verbose_name="Фото", blank=True, null=True
    )
    status = models.CharField(max_length=100, verbose_name="Статус", blank=True)

    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город")
    black_list = models.ManyToManyField("self", blank=True, verbose_name="Игнор лист")
    notifications = models.ManyToManyField(
        Notification, related_name="account", blank=True
    )
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="account")
    objects = AccountManager()

    def __str__(self):
        return self.user.username


SOCIAL_NETWORK_LINK_NAME = (    # Choices
    ("VK", "Вконтакте"),
    ("INST", "Instagram"),
    ("FB", "Facebook"),
    ("WA", "WhatsApp"),
    ("YT", "YouTube"),
)


class SocialNetworkLink(UUIDModel):
    """
    Social network link model.
    """
    account = models.ForeignKey(
        Account,
        verbose_name="Пользователь",
        related_name="social_network_links",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=4, choices=SOCIAL_NETWORK_LINK_NAME, default="VK"
    )
    links = models.URLField()

    def __str__(self):
        return f"{self.get_name_display()}:{self.links}"

    class Meta:
        verbose_name = "Ссылка на социальные сети"
        verbose_name_plural = "Ссылки на социальные сети"


class Tag(UUIDModel):
    """
    Tag model.
    """
    name = models.TextField(max_length=20)
