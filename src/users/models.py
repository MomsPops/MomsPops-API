from django.db import models
from django.contrib.auth.models import User
from typing import Dict

from service.models import UUIDModel

from locations.models import City
from profiles.models import Profile


class AccountManager(models.Manager):
    """
    Custom account manager.
    """

    def create_account(self, city_name: str, region_name: str, user: Dict[str, str]):
        city = City.objects.get(name=city_name, region__name=region_name)
        new_user = User.objects.create_user(**user)
        new_account = self.model(user=new_user, city=city)
        new_account.save(using=self._db)
        Profile.objects.create(account=new_account)
        return new_account

    def deactivate(self, instance):
        if instance.user.is_active:
            instance.user.is_active = False
            instance.user.save()
            instance.save()

    def activate(self, instance):
        if not instance.user.is_active:
            instance.user.is_active = True
            instance.save()

    def change_is_active(self, instance):
        instance.user = not instance.user
        instance.save()


class Account(UUIDModel):
    """
    Account model.
    """
    user: User = models.OneToOneField(
        User, related_name="account", on_delete=models.CASCADE
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город")
    black_list = models.ManyToManyField("self", blank=True, verbose_name="Игнор лист")

    objects = AccountManager()

    def __str__(self):
        return self.user.username
