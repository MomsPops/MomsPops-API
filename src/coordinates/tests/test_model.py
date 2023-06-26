from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError

from service.fixtues import TestAccountFixture
from coordinates.models import Coordinate


class TestCoordinate(TestAccountFixture, APITestCase):

    def test_coordinate_create1(self):
        user_coord = Coordinate.coordinate_manager.create(
            lat=60.0, lon=80.0, account=self.user_account
        )
        self.assertEqual(user_coord.account.city, self.user_account.city)
        self.assertEqual(user_coord.lat, 60.0)
        self.assertEqual(user_coord.lon, 80.0)
        self.assertEqual(self.user_account.coordinate, user_coord)

    def test_coordinate_create2(self):
        user_coord = Coordinate.coordinate_manager.create(
            lat=90.0, lon=-180, account=self.user_account
        )
        self.assertEqual(user_coord.account.city, self.user_account.city)
        self.assertEqual(user_coord.lat, 90.0)
        self.assertEqual(user_coord.lon, -180.0)

    def test_coordinate_lat_fail1(self):
        with self.assertRaises(ValidationError):
            Coordinate.coordinate_manager.create(
                lat=-90.011123123112, lon=123, account=self.user_account
            )

    def test_coordinate_lat_fail2(self):
        with self.assertRaises(ValidationError):
            Coordinate.coordinate_manager.create(
                lat=191, lon=-100, account=self.user_account
            )

    def test_coordinate_lon_fail1(self):
        with self.assertRaises(ValidationError):
            Coordinate.coordinate_manager.create(
                lat=11.123, lon=-181.0, account=self.user_account
            )

    def test_coordinate_lon_fail2(self):
        with self.assertRaises(ValidationError):
            Coordinate.coordinate_manager.create(
                lat=.0, lon=180.0, account=self.user_account
            )
