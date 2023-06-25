from uuid import uuid4

from django.db import models


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
    # TODO: delet this model verbose_name - important !!!
    account = models.ForeignKey("users.Account", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AccountOneToOneModel(models.Model):
    # TODO: delet this model verbose_name - important !!!
    account = models.OneToOneField("users.Account", on_delete=models.CASCADE)

    class Meta:
        abstract = True
