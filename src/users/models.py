from django.db import models
from django.contrib.auth.models import User
from typing import Dict

from service.models import UUIDModel
from profiles.models import Profile
from locations.models import City
from typing import Union


class AccountManager(models.Manager):
    """
    Custom account manager.
    """
    def create_account(
        self,
        user: Dict[str, str],
        city_name: Union[str, None] = None,
        region_name: Union[str, None] = None,
    ):
        city = None
        if city_name and region_name:
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
    Account model. It`s User model extension with OneToOne relationship, not more.
    """
    user: User = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город", null=True, blank=True)
    black_list = models.ManyToManyField("self", blank=True, verbose_name="Игнор лист")
    coordinate = models.OneToOneField("coordinates.Coordinate", on_delete=models.SET_NULL,
                                      null=True, related_name="source")

    objects = AccountManager()

    def __str__(self):
        return self.user.username
