from django.db import models


class CityManager(models.Manager):
    def all(self):
        return (
            super()
            .select_related("region")
            .all()
        )


class RegionManager(models.Manager):
    def all(self):
        return (
            super()
            .prefetch_related("cities")
            .all()
        )


class City(models.Model):
    """
    City model.
    """
    name = models.CharField(max_length=100, db_index=True)
    region = models.ForeignKey(
        to="Region",
        on_delete=models.CASCADE,
        related_name="cities",
        null=True
    )

    objects = models.Manager()
    city_manager = CityManager()

    def get_full_name(self):
        return f"{self.name}, {self.region.name}"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ("name", "region")
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Region(models.Model):
    """
    Region model.
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)

    objects = models.Manager()
    region_manager = RegionManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
