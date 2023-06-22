from django.db import models

from .country import Country


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="+"
    )

    objects = models.Manager()

    def get_full_name(self):
        return f"{self.name}, {self.country.name}"

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "country")
