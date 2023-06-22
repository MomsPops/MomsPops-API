from django.db import models
from uuid import uuid4


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
