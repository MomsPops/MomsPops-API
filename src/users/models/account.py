from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

from .city import City


class AccountManager(models.Manager):
    def create_account(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        city_name: str,
        country_name: str,
        email: str | None = None,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        city = City.objects.get(
            name=city_name, country__name=country_name
        )  # TODO: need unique fields
        account = self.model(user=user, city=city)
        account.save(using=self._db)
        return account


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
