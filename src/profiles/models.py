from django.db import models
from django.urls import reverse
from django.conf import settings

from service.models import UUIDModel, TimeCreateUpdateModel, AccountOneToOneModel


SEX_CHOICES = (("Не выбран", "Не выбран"), ("Мужской", "Мужской"), ("Женский", "Женский"), ("Другой", "Другой"))


class Profile(UUIDModel, AccountOneToOneModel):  # type: ignore
    """
    Profile model.
    """

    bio = models.TextField(default="", verbose_name="Биография")
    photo = models.ImageField(
        upload_to="uploads/profile_img/", verbose_name="Фото", blank=True, null=True
    )  # default='default_image.jpg'
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="День рождения")
    status = models.CharField(max_length=100, verbose_name="Статус", default="")
    tags = models.ManyToManyField("Tag", verbose_name="profiles", related_name="profiles")
    sex = models.IntegerField("Пол", choices=SEX_CHOICES, default=0)

    objects = models.Manager()

    def get_photo_url(self):
        path_for_default_img = settings.MEDIA_URL + "default_img/user_standart_avatar.png"
        if self.photo:
            return "http://127.0.0.1:8000" + self.photo.url
        return "http://127.0.0.1:8000" + path_for_default_img

    def get_profile_url(self):
        return reverse("profiles_detail", kwargs={"username": self.account.user.username})


class Post(UUIDModel, TimeCreateUpdateModel):  # type: ignore
    """
    Post model.
    """

    profile = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="uploads/post_img/", verbose_name="Фото", blank=True, null=True
    )  # TODO add table Post Images
    reactions = models.ManyToManyField("reactions.Reaction", related_name="posts")

    objects = models.Manager()

    def get_preview_text(self):
        return self.text[:150] + "..."

    def __str__(self):
        return self.get_preview_text()


class Tag(UUIDModel):
    """
    Tag model.
    """

    name = models.TextField(max_length=30, unique=True)
