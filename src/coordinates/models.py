from django.db import models
from datetime import timedelta, datetime, timezone

from .validators import validate_latitude, validate_longitude
from .service.calculations import calculate_distance_1, calculate_vector_distance, vectorize_queryset
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

    def filter_time(self, queryset=None) -> filter:
        if queryset is None:
            queryset = self.all()
        now_time = datetime.now(timezone.utc)
        return filter(
            lambda coord: now_time - coord.last_time <= self.delta_limit,
            queryset
        )

    def is_near(self, source_coordinate):
        def inner(coord):
            return self.distance_needed >= calculate_distance_1(
                lat1=coord.lat,
                lat2=source_coordinate.lat,
                lon1=coord.lon,
                lon2=source_coordinate.lon
            )
        return inner

    def all_near(self, source_coordinate) -> filter:
        is_near = self.is_near(source_coordinate)
        time_filtered_coords = self.filter_time(queryset=filter(lambda x: x != source_coordinate, self.all()))
        return filter(is_near, time_filtered_coords)

    def all_near_fast(self, source_coordinate):
        now_time = datetime.now(timezone.utc)
        time_filtered_coords = filter(  # noqa: E731
            lambda coord: now_time - coord.last_time <= self.delta_limit and coord != source_coordinate,
            self.all()
        )
        lat2, lon2 = vectorize_queryset(time_filtered_coords)
        for d, instance in zip(
                calculate_vector_distance(lon1=source_coordinate.lon, lat1=source_coordinate.lat, lon2=lon2, lat2=lat2),
                time_filtered_coords
        ):
            if d <= self.delta_limit:
                yield instance

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

    object = models.Manager()
    coordinate_manager = CoordinateManager()

    def __str__(self):
        lat_mark = "с.ш." if self.lat >= 0 else "ю.ш."  # при отрицательной широте широта южная
        lon_mark = "в.д." if self.lon >= 0 else "з.д."  # при отрицательной долготе долгота южная
        return f"{self.lat} {lat_mark}; {self.lon} {lon_mark}"

    class Meta:
        verbose_name = "Координата"
        verbose_name_plural = "Координаты"
