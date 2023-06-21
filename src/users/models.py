from django.db import models
from django.contrib.auth.models import UserManager, BaseUserManager
from django.contrib.auth.models import AbstractUser

from uuid import uuid4
from passlib.hash import django_pbkdf2_sha256


class UserCustomManager(UserManager):
    """
    Custom manager for user model.
    """
    password_hasher = django_pbkdf2_sha256

    def create(self, **kwargs):
        """
        Create function. Creates user with given data, but password is hashed.
        """
        psw = kwargs.get('password')
        if psw is not None:
            hash_pws = self.password_hasher.hash(psw)
            kwargs.update(password=hash_pws)
            new_user = self._model(**kwargs)
            new_user.save()
            return new_user

    def login(self, username: str, password: str) -> models.Model | None:
        """
        Login function. Checks if there is a user with the data, after checks the password.
        """
        try:
            user = self.get_queryset().get(username=username)
            if self.password_hasher.verify(password, user.password):
                return user
        except self._model.DoesNotExist:
            pass

        return None  # return None if user does not exist or password is not correct


class User(AbstractUser):
    """User model."""
    id = models.UUIDField(primary_key=True, default=uuid4)

    USERNAME_FIELD = "username"
    user_objects = UserCustomManager()

    def deactivate(self):
        """Sets user active attribute to `False`"""
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_login']

