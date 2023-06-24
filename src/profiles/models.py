from django.db import models
from service.models import UUIDModel, TimeCreateUpdateModel, AccountOneToOneModel
from settings.settings import MEDIA_URL


class Profile(UUIDModel, AccountOneToOneModel):
    """
    Profile model.
    """
    bio = models.TextField(blank=True, null=True, verbose_name="Биография")
    photo = models.ImageField(
        upload_to="uploads/profile_img/", verbose_name="Фото", blank=True, null=True
    )   # default='default_image.jpg'
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="День рождения")
    status = models.CharField(max_length=100, verbose_name="Статус", blank=True)
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="profile")
    objects = models.Manager()

    def get_image(self):
        path_for_default_img = MEDIA_URL + "default_img/user_standart_avatar.png"
        if self.photo:
            return "http://127.0.0.1:8000" + self.photo.url
        return "http://127.0.0.1:8000" + path_for_default_img 


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


SOCIAL_NETWORK_LINK_NAME = (    # Choices
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
    account = models.ForeignKey(
        "Profile",
        verbose_name="Профиль",
        related_name="social_network_links",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=4, choices=SOCIAL_NETWORK_LINK_NAME, default="VK"
    )
    links = models.URLField()

    def __str__(self):
        return f"{self.get_name_display()}:{self.links}"

    class Meta:
        verbose_name = "Ссылка на социальные сети"
        verbose_name_plural = "Ссылки на социальные сети"


class Tag(UUIDModel):
    """
    Tag model.
    """
    name = models.TextField(max_length=20)
