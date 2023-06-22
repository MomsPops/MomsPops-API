from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(
        User,
        related_name="account",
        on_delete=models.CASCADE
    )
    # extra

    def __str__(self):
        return self.user.username


