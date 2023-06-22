from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

from locations.models import City


class AccountManager(models.Manager):
    def create_account(
        self,
        city_name: str,
        country_name: str,
        user: dict[str, str]
    ):
        city = City.objects.get(
            name=city_name, country__name=country_name
        )
        new_user = User.objects.create_user(**user)
        new_account = self.model(user=new_user, city=city)
        new_account.save(using=self._db)
        return new_account


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user: User = models.OneToOneField(
        User, related_name="account", on_delete=models.CASCADE
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    followers = models.ManyToManyField("self", blank=True)  # TODO: naming
    black_list = models.ManyToManyField("self", blank=True)

    objects = AccountManager()

    def __str__(self):
        return self.user.username
