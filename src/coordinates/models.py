from django.db import models
from datetime import datetime, timedelta

from service.models import AccountOneToOneModel
from users.models import Account
from .service.calculations import coordinates_distance
from .service.google_api import decode_coordinate
from .validators import validate_latitude, validate_longitude


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

    def filter_time(self) -> filter:
        now_time = datetime.now()
        return filter(
            lambda coord: now_time - coord.last_time <= self.delta_limit,
            self.get_queryset()
        )

    def all_near(self, user_coordinate) -> filter:
        def is_near(coord) -> bool:
            distance = coordinates_distance(
                lat1=coord.lat,
                lat2=user_coordinate.lat,
                lon1=coord.lon,
                lon2=user_coordinate.lon
            )
            return distance <= self.distance_needed

        filtered_coords = self.filter_time()
        return filter(
            is_near,
            filtered_coords
        )

    def decode(self, coord) -> str:
        """Returns place by coordinate."""
        return decode_coordinate(lat=coord.lat, lon=coord.lon)

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
        return f"{self.lat}; {self.lon}"
