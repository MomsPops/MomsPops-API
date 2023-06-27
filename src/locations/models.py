from django.db import models


class City(models.Model):
    """
    City model.
    """
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
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Region(models.Model):
    """
    Region model.
    """
    name = models.CharField(max_length=100, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
