from django.db import models
from django.contrib.auth.models import User


class Coordinate(models.Model):
    """
    Coordinate model.
    """
    lat = models.DecimalField("Latitude", decimal_places=6, max_digits=8)
    lon = models.DecimalField("Longitude", decimal_places=6, max_digits=9)
    user = models.OneToOneField(User, related_name="+", on_delete=models.CASCADE)
    last_time = models.DateTimeField("Last time", auto_created=True, auto_now=True)

    object = models.Manager()

    def __str__(self):
        return f"{self.lat}; {self.lon}"
