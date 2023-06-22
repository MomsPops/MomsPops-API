from django.db import models
from uuid import uuid4
from users.models import Account


class Profile(models.Model):
    """
    Profile model.
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    account = models.OneToOneField(
        Account, related_name="account", on_delete=models.CASCADE
    )

    objects = models.Manager()


class Post(models.Model):
    """
    Post model.
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    profile = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="uploads/post_img/", verbose_name="Фото", blank=True, null=True
    )  # TODO add table Post Images

    objects = models.Manager()
