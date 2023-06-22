from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="+"
    )
    region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name="city")

    objects = models.Manager()

    def get_full_name(self):
        return f"{self.name}, {self.region.name}"

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "region")


class Region(models.Model):
    name = models.CharField(max_length=100)
