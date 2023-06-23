from django.db import models
from django.core.files import File
from service.models import UUIDModel, TimeCreateUpdateModel, AccountOneToOneModel


def upload_default_photo():  # TODO
    return File(...)


class Profile(UUIDModel, AccountOneToOneModel):
    """
    Profile model.
    """

    objects = models.Manager()


class Post(UUIDModel, TimeCreateUpdateModel):
    """
    Post model.
    """
    profile = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="uploads/post_img/", verbose_name="Фото", blank=True, null=True
    )  # TODO add table Post Images

    objects = models.Manager()
