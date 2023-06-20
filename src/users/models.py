from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import get_hasher

from uuid import uuid4
from passlib.hash import django_pbkdf2_sha256


# for more comfort of changing hashing algorithm
password_hasher = django_pbkdf2_sha256


class UserCustomManager(UserManager):
    def create(self, **data):
        data['password'] = password_hasher.hash(data.get("password"))
        try:
            new_user: User = self.model(
                **data
            )
            new_user.save()
            return new_user
        except IntegrityError:
            return None

    def login(self, username: str, password: str) -> models.Model | None:
        try:
            user = super().get_queryset().get(username=username)
            if get_hasher().verify(password, user.password):
                return user
        except self.model.DoesNotExist:
            pass
        return None  # return None if user does not exist or password is not correct


class User(AbstractUser):
    """User model."""
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.CharField("Email", max_length=100)
    first_name = models.CharField("First name", max_length=100)
    last_name = models.CharField("Last name", max_length=100)

    USERNAME_FIELD = "username"

    objects = UserCustomManager()

    def deactivate(self) -> None:
        self.is_active = False
        self.save()

    class Meta:
        ordering = ['last_login']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


