from django.db import models
from uuid import uuid4
from users.models.account import Account


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    account = models.OneToOneField(
        Account, related_name="account", on_delete=models.CASCADE
    )


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    profile = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="uploads/post_img/", verbose_name="Фото", blank=True, null=True
    )  # TODO add table Post Images
