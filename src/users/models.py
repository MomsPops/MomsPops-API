from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.http import Http404
from typing import Dict, Union

from service.models import UUIDModel
from profiles.models import Profile
from locations.models import City


class CustomUserManager(UserManager):
    def get(self, *args, **kwargs):
        return super().select_related('account', "account__coordinate").get(*args, **kwargs)


class User(AbstractUser):
    objects = CustomUserManager()


class AccountManager(models.Manager):
    """
    Custom account manager.
    """
    def all(self):
        return (
            super()
            .select_related("user", "coordinate", "profile")
        )

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
        new_user.is_active = False    # for email validation
        new_user.save()
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
            instance.user.save()
            instance.save()

    def change_is_active(self, instance):
        instance.user = not instance.user
        instance.save()

    def get_by_username(self, username: str):
        try:
            account = self.all().select_related('profile').get(user__username=username)
            return account
        except self.model.DoesNotExist:
            raise Http404("User with such username is not found.")

    def block_user(self, account, username: str) -> None:
        if account.user.username == username:
            raise ValueError("Cannot not block yourself.")
        account_to_block = self.get_by_username(username)
        account.black_list.add(account_to_block)
        account.save()

    def unblock_user(self, account, username: str) -> None:
        if account.user.username == username:
            raise ValueError("Cannot not unblock yourself.")

        if account.black_list.filter(user__username=username).exists():
            account_to_block = self.get_by_username(username)
            account.black_list.remove(account_to_block)
            account.save()
        else:
            raise Http404("User was not blocked.")


class Account(UUIDModel):
    """
    Account model. It`s User model extension with OneToOne relationship, not more.
    """
    user: User = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город", null=True, blank=True)
    black_list = models.ManyToManyField("self", blank=True, verbose_name="Игнор лист")
    coordinate = models.OneToOneField("coordinates.Coordinate", on_delete=models.SET_NULL,
                                      null=True, related_name="source", blank=True)

    objects = AccountManager()

    def __str__(self):
        return self.user.username
