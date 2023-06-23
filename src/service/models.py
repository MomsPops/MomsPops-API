from django.db import models

from uuid import uuid4


class UUIDModel(models.Model):
    """
    Generic with pk represented as UUID.
    """
    id = models.UUIDField(primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class TimeCreateModel(models.Model):
    """
    Generic model with auto created time.
    """
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimeCreateUpdateModel(models.Model):
    """
    Generic model with auto created and updated time.
    """
    time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountForeignModel(models.Model):
    account = models.ForeignKey("users.Account", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AccountOneToOneModel(models.Model):
    account = models.OneToOneField("users.Account", on_delete=models.CASCADE)

    class Meta:
        abstract = True
