from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4
from passlib.hash import django_pbkdf2_sha256


# for more comfort of changing hashing algorithm
password_hasher = django_pbkdf2_sha256


class User(AbstractUser):
    """User model."""
    id = models.UUIDField(primary_key=True, default=uuid4)

    USERNAME_FIELD = "username"

    @classmethod
    def create(cls, **data) -> models.Model:
        psw = data.get('password')
        if psw is not None:
            hash_pws = password_hasher.hash(psw)
            data.update(password=hash_pws)

            new_user = cls.objects.create(**data)
            return new_user

    @classmethod
    def login(cls, username: str, password: str) -> models.Model | None:
        try:
            user = cls.objects.get(username=username)
            if password_hasher.verify(password, user.password):
                return user
        except cls.DoesNotExist:
            pass

        return None     # return None if user does not exist or password is not correct

    def deactivate(self):
        self.is_active = False
        self.save()

    class Meta:
        ordering = ['last_login']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

