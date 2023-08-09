from typing import Optional

from django.db import models
from django.urls import reverse
from django.conf import settings

from service.models import UUIDModel, TimeCreateUpdateModel, AccountOneToOneModel

# choices for Profile.sex field
SEX_CHOICES = (("Не выбран", "Не выбран"), ("Мужской", "Мужской"), ("Женский", "Женский"), ("Другой", "Другой"))


class ProfileManager(models.Manager):
    def all(self):
        return (
            super()
            .select_related("account", "account__user")
            .prefetch_related("account__friends")
            .all()
        )

    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("account", "account__user", "account__coordinate")
            .prefetch_related("account__friends")
            .get(*args, **kwargs)
        )


class Profile(UUIDModel, AccountOneToOneModel):  # type: ignore
    """
    Profile model. It looks like a profile in a social network: VK or Facebook.
    Profile is an OneToOne field for Account, which consists of profile information and related
    posts.
    """
    bio = models.TextField(null=True, blank=True, verbose_name="Биография")
    photo = models.ImageField(
        upload_to="uploads/profile_img/", verbose_name="Фото", blank=True, null=True
    )
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="День рождения")
    status = models.CharField(max_length=100, verbose_name="Статус", blank=True, null=True)
    tags = models.ManyToManyField("Tag", verbose_name="profiles", related_name="tags", blank=True)
    sex = models.CharField("Пол", choices=SEX_CHOICES, default="Не выбран", max_length=10)

    objects = ProfileManager()
    profile_manager = ProfileManager()

    def get_photo_url(self) -> str:
        """Static url to user photo"""
        if not self.photo:
            return settings.MEDIA_URL + "uploads/profile_img/default_avatar.png"       # type: ignore
        return self.photo.url   # type: ignore

    def get_absolute_url(self) -> str:
        """Reversed url to single profile."""
        return reverse("profiles_detail", kwargs={"username": self.account.user.username})     # type: ignore


class PostManager(models.Manager):
    def all_by_username(self, username):
        """
        Get all posts on account`s user`s username.
        """
        posts = self.all().filter(profile__account__user__username=username)
        return posts


class Post(UUIDModel, TimeCreateUpdateModel):  # type: ignore
    """
    Post model. Post is a note pinned on some account`s profile.
    """
    profile: Profile = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    photo = models.ImageField(
        upload_to="uploads/post_img/", verbose_name="Фото", blank=True, null=True
    )
    reactions = models.ManyToManyField("reactions.Reaction", related_name="posts")

    objects = models.Manager()
    post_manager = PostManager()

    def get_photo_url(self) -> Optional[str]:
        if self.photo:
            return self.photo.url   # type: ignore
        return None

    def get_preview_text(self) -> str:  # type: ignore
        if self.text is not None:
            return self.text[:150] + "..."  # type: ignore

    def get_absolute_url(self) -> str:
        return reverse("posts_detail", kwargs={'id': self.id})  # type: ignore

    def __str__(self):
        string = self.get_preview_text()
        if string is None:
            return str(self.id)


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

    objects = models.Manager()

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

    objects = models.Manager()
