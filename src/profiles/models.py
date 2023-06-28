from typing import Optional

from django.db import models
from django.urls import reverse
from django.conf import settings

from service.models import UUIDModel, TimeCreateUpdateModel, AccountOneToOneModel

# choices for Profile.sex field
SEX_CHOICES = (("Не выбран", "Не выбран"), ("Мужской", "Мужской"), ("Женский", "Женский"), ("Другой", "Другой"))


class Profile(UUIDModel, AccountOneToOneModel):  # type: ignore
    """
    Profile model. It looks like a profile in a social network: VK or Facebook.
    Profile is an one2one field for Account, which consists of profile information and related
    posts.
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

    def get_absolute_url(self):
        return reverse("profiles_detail", kwargs={"username": self.account.user.username})


class PostManager(models.Manager):
    def all_by_username(self, username):
        posts = self.all().filter(profile__account__user__username=username)
        return posts


class Post(UUIDModel, TimeCreateUpdateModel):  # type: ignore
    """
    Post model. Post is a note pinned on some account`s profile.
    """
    profile: Profile = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="uploads/post_img/", verbose_name="Фото", blank=True, null=True
    )  # TODO add table Post Images
    reactions = models.ManyToManyField("reactions.Reaction", related_name="posts")

    objects = models.Manager()
    post_manager = PostManager()

    def get_photo_url(self) -> Optional[str]:
        if self.photo:
            return "http://127.0.0.1:8000" + self.photo.url   # type: ignore
        return None

    def get_preview_text(self) -> str:
        return self.text[:150] + "..."  # type: ignore

    def get_absolute_url(self) -> str:
        return reverse("posts_detail", kwargs={'id': self.id})  # type: ignore

    def __str__(self):
        return self.get_preview_text()


SOCIAL_NETWORK_LINK_NAME = (  # Choices
    ("VK", "Вконтакте"),
    ("INST", "Instagram"),
    ("FB", "Facebook"),
    ("WA", "WhatsApp"),
    ("YT", "YouTube"),
)


class SocialNetworkLink(UUIDModel):
    """
    Social network link model.
    """
    profile = models.ForeignKey(
        "profiles.Profile",
        verbose_name="Пользователь",
        related_name="social_network_links",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=4, choices=SOCIAL_NETWORK_LINK_NAME, default="VK")
    links = models.URLField()

    def __str__(self):
        return f"{self.get_name_display()}:{self.links}"

    class Meta:
        verbose_name = "Ссылка на социальные сети"
        verbose_name_plural = "Ссылки на социальные сети"


class Tag(UUIDModel):
    """
    Tag model.
    Like #programming, #cats. Interests and hobbies of a person.
    """
    name = models.TextField(max_length=20, unique=True)
