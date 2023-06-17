from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4


User = get_user_model()


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profiles/")
    birth_date = models.DateField("Birthday date")
    bio = models.TextField()
    country = models.CharField("Country", max_length=100, null=True)
    city = models.CharField("City", max_length=100, null=True)
    interests = models.TextField("Interests", max_length=400)

    def __str__(self):
        return str(self.user)


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    profile = models.ForeignKey(to="Profile", on_delete=models.CASCADE)
    text = models.TextField()
    photo = models.ImageField(upload_to="notes/", null=True, blank=True)
    time_created = models.DateTimeField(auto_created=True)
    time_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:100] + "..."

