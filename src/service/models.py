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

    time_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class TimeCreateUpdateModel(models.Model):
    """
    Generic model with auto created and updated time.
    """
    time_created = models.DateTimeField(auto_now_add=True, null=True)
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


def AccountOneToOneFunc(related_name=None, verbose_name=None, null=False):
    """Abstract model decorator."""
    class InnerModel(models.Model):
        account = models.OneToOneField(
            to="users.Account",
            verbose_name=verbose_name,
            related_name=related_name,
            on_delete=models.CASCADE,
            null=null
        )
    return InnerModel


def AccountForeignFunc(related_name=None, verbose_name=None, null=False):
    """Abstract model decorator."""
    class InnerModel(models.Model):
        account = models.ForeignKey(
            to="users.Account",
            verbose_name=verbose_name,
            related_name=related_name,
            on_delete=models.CASCADE,
            null=null
        )
    return InnerModel
