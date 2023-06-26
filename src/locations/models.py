from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(
        to="Region",
        on_delete=models.CASCADE,
        related_name="cities",
        null=True
    )
    objects = models.Manager()

    def get_full_name(self):
        return f"{self.name}, {self.region.name}"

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "region")


class Region(models.Model):
    name = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name
