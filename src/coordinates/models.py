from django.db import models
from datetime import datetime, timedelta, timezone

from service.models import AccountOneToOneModel
from users.models import Account
from .validators import validate_latitude, validate_longitude
from .service.calculations import calculate_distance_1
from .service.google_api import get_location_details


class CoordinateManager(models.Manager):
    distance_needed: float = 3000  # in meters
    delta_limit: timedelta = timedelta(minutes=5)

    def update(self, instance, lat: float, lon: float):
        instance.lat = validate_latitude(lat)
        instance.lon = validate_longitude(lon)
        instance.save()

    def create(self, lat: float, lon: float, account: Account):
        lat = validate_latitude(lat)
        lon = validate_longitude(lon)
        new_coordinate = Coordinate(lat=lat, lon=lon, account=account)
        new_coordinate.save()
        return new_coordinate

    def filter_time(self, queryset=None) -> filter:
        if queryset is None:
            queryset = self.all()
        now_time = datetime.now(timezone.utc)
        return filter(
            lambda coord: now_time - coord.last_time <= self.delta_limit,
            queryset
        )

    def all_near(self, user_coordinate) -> filter:
        is_near = lambda coord: calculate_distance_1(   # noqa: E731
            lat1=coord.lat,
            lat2=user_coordinate.lat,
            lon1=coord.lon,
            lon2=user_coordinate.lon
        ) <= self.distance_needed

        time_filtered_coords = self.filter_time(queryset=filter(lambda x: x != user_coordinate, self.all()))
        return filter(
            is_near,
            time_filtered_coords
        )

    def all_near_fast(self, user_coordinate) -> filter:
        is_near = lambda coord:  calculate_distance_1(   # noqa: E731
                lat1=coord.lat,
                lat2=user_coordinate.lat,
                lon1=coord.lon,
                lon2=user_coordinate.lon
            ) <= self.distance_needed
        now_time = datetime.now(timezone.utc)
        time_filtered_coords = filter(  # noqa: E731
            lambda coord: now_time - coord.last_time <= self.delta_limit and coord != user_coordinate,
            self.all()
        )
        return filter(is_near, time_filtered_coords)

    def decode(self, coord) -> str:
        """Returns place by coordinate."""
        return get_location_details(lat=coord.lat, lon=coord.lon)

    def deactivate(self, account) -> None:
        """Sets account coordinate to None"""
        account.coordinate = None
        account.save()


class Coordinate(AccountOneToOneModel):
    """
    Coordinate model.
    """
    lat = models.FloatField("Latitude", validators=[validate_latitude])
    lon = models.FloatField("Longitude", validators=[validate_longitude])
    account = models.OneToOneField(Account, related_name="coordinate", on_delete=models.CASCADE, null=True)
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
