from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from rest_framework.exceptions import ValidationError
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
    Account model.
    """
    user: User = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город", null=True, blank=True)
    coordinate = models.OneToOneField(
        "coordinates.Coordinate",
        on_delete=models.SET_NULL,
        null=True,
        related_name="source",
        blank=True
    )
    black_list = models.ManyToManyField("self", blank=True, verbose_name="Игнор лист")
    friends = models.ManyToManyField("self", blank=True, verbose_name="Friends")

    objects = AccountManager()

    def __str__(self):
        return self.user.username


class FriendshipRequestManager(models.Manager):
    """
    Friend request manager.
    """

    def create_friendship_request(self, from_account, to_account):
        if from_account == to_account:
            raise ValidationError("Cannot send friendship request to yourself.")

        if from_account.black_list.filter(id=to_account.id).exists():
            raise ValidationError("Account to send request is in the black list.")
        if to_account.black_list.filter(id=from_account.id).exists():
            raise ValidationError("Account to send friendship request blocked you.")

        obj = super().create(from_account=from_account, to_account=to_account)
        return obj


class FriendshipRequest(UUIDModel):
    """
    Friend request model.
    """
    from_account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="outcoming_requests")
    to_account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="incoming_requests")

    def accept(self):
        """Accept request method."""
        self.from_account.friends.add(self.to_account)
        self.to_account.friends.add(self.from_account)
        self.delete()

    friendship_request_manager = FriendshipRequestManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.from_account.user.username} -> {self.to_account.user.username}"

    class Meta:
        verbose_name = "Friendship request"
        verbose_name_plural = "Friendship requests"
