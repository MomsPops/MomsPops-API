from django.core.files import File
from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()


def load_default_photo():
    with open("../media/profiles/default.jpg") as file:
        return File(file, name='default.png')


class ProfileManager(models.Manager):
    def get_by_user(self, user: User):
        profile = super().get_queryset().get(user=user)
        return profile

    def get_all_active(self):
        profiles = super().get_queryset().filter(user__is_active=True)
        return profiles


class Profile(models.Model):
    objects = ProfileManager()

    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profiles/", default=load_default_photo)
    birth_date = models.DateField("Birthday date")
    bio = models.TextField()
    country = models.CharField("Country", max_length=100, null=True)
    city = models.CharField("City", max_length=100, null=True)
    interests = models.TextField("Interests", max_length=400)

    def __str__(self):
        return str(self.user)


class NoteManager(models.Manager):

    def get_by_username(self, username):
        return self.get_queryset().filter(user__username=username)


class Note(models.Model):
    objects = NoteManager()

    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    photo = models.ImageField(upload_to="notes/", null=True, blank=True)
    time_created = models.DateTimeField(auto_created=True)
    time_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:100] + "..."

