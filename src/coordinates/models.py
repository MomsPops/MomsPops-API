from django.db import models
from datetime import timedelta, datetime, timezone
from typing import Callable, Optional, Sequence, Generator

from .validators import validate_latitude, validate_longitude
from .service.calculations import calculate_distance_1, calculate_vector_distance, vectorize_queryset, \
    vectorize_queryset_related
from .service.google_api import get_location_details


class CoordinateManager(models.Manager):
    distance_needed: float = 3000  # in meters
    delta_limit: timedelta = timedelta(minutes=5)

    def update(self, instance, lat: float, lon: float):
        instance.lat = validate_latitude(lat)
        instance.lon = validate_longitude(lon)
        instance.save()

    def create(self, lat: float, lon: float, source):
        lat = validate_latitude(lat)
        lon = validate_longitude(lon)
        new_coordinate = Coordinate(lat=lat, lon=lon)
        new_coordinate.save()
        source.coordinate = new_coordinate
        source.save()
        return new_coordinate

    def create(self, lat: float, lon: float, user):
        lat = validate_latitude(lat)    # returns value if valid else raises an ValidationError
        lon = validate_longitude(lon)
        new_coordinate = Coordinate(lat=lat, lon=lon, user=user)
        new_coordinate.save()
        user.save()
        return new_coordinate

    @staticmethod
    def is_near(source_coordinate, distance) -> Callable:
        """Simple decorator to create namespace with given arguments."""
        def inner(source_) -> bool:
            return distance >= calculate_distance_1(
                lat1=source_.coordinate.lat,
                lat2=source_coordinate.lat,
                lon1=source_.coordinate.lon,
                lon2=source_coordinate.lon
            )
        return inner

    def all_near(
            self,
            source,
            distance: int = 5000,
            queryset: Optional[Sequence] = None,
            sort: bool = True
    ) -> filter | list | Generator:
        """Return all new users on given radius about `source_user`."""
        if source.coordinate is None:
            return []

        elif queryset is None:
            queryset = source.__class__.objects.all().filter(coordinate__isnull=False)
        else:
            queryset = (q for q in queryset if q.coordinate is not None)
        is_near = self.is_near(source.coordinate, distance)
        if not sort:
            return filter(
                lambda instance: is_near(instance) and instance != source,
                queryset
            )
        def filter_gen():
            """Inner complex generator."""
            nonlocal source, queryset
            for instance in queryset:
                dist = calculate_distance_1(
                    lat1=instance.coordinate.lat,
                    lat2=source.coordinate.lat,
                    lon1=instance.coordinate.lon,
                    lon2=source.coordinate.lon
                )
                if dist <= distance and instance != source:
                    yield instance, dist

        return (i[0] for i in sorted(filter_gen(), key=lambda el: el[1]))

    def all_near_fast(
            self,
            source,
            distance: int = 5000,
            queryset: Optional[Sequence] = None,
            sort: bool = True
    ) -> filter | list | Generator:
        """
        Return all new users on given radius about `source_user`, but faster.
        The idea is to reduce CPU time for taking over data and give the vector data to
        calculate for processor. Generator function is to reduce memory usage.
        """
        if source.coordinate is None:
            yield from []
            return

        elif queryset is None:
            queryset = source.__class__.objects.all().filter(coordinate__isnull=False)
            lat2, lon2 = vectorize_queryset_related(queryset)
        else:
            def gen(queryset_=queryset):
                for q in queryset_:
                    if q.coordinate is not None:
                        yield q
            queryset = gen
            lat2, lon2 = vectorize_queryset_related(queryset)
            queryset = queryset()
        if not sort:
            for d, instance in zip(
                    calculate_vector_distance(
                        lon1=source.coordinate.lon,
                        lat1=source.coordinate.lat,
                        lon2=lon2,
                        lat2=lat2
                    ),
                    queryset
            ):
                if d <= distance and instance != source:
                    yield instance
        else:
            def filter_gen():
                """Inner complex generator."""
                nonlocal source, queryset
                for d, instance in zip(
                        calculate_vector_distance(
                            lon1=source.coordinate.lon,
                            lat1=source.coordinate.lat,
                            lon2=lon2,
                            lat2=lat2
                        ),
                        queryset
                ):
                    if d <= distance and instance != source:
                        yield instance, d
            yield from (i[0] for i in sorted(filter_gen(), key=lambda el: el[1]))

    def decode(self, coord) -> str:
        """Returns place by coordinate."""
        return get_location_details(lat=coord.lat, lon=coord.lon)

    def deactivate(self, account) -> None:
        """Sets account coordinate to None"""
        account.coordinate = None
        account.save()


class Coordinate(models.Model):
    """
    Coordinate model.
    """
    lat = models.FloatField("Latitude")
    lon = models.FloatField("Longitude")
    last_time = models.DateTimeField("Last time", auto_created=True, auto_now=True)

    objects = models.Manager()
    coordinate_manager = CoordinateManager()

    def __str__(self):
        lat_mark = "с.ш." if self.lat >= 0 else "ю.ш."  # при отрицательной широте широта южная
        lon_mark = "в.д." if self.lon >= 0 else "з.д."  # при отрицательной долготе долгота южная
        return f"{self.lat} {lat_mark}; {self.lon} {lon_mark}"

    class Meta:
        verbose_name = "Координата"
        verbose_name_plural = "Координаты"
