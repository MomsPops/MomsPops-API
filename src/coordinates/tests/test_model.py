from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError  # , ObjectDoesNotExist
import random

from service.fixtues import TestAccountFixture
from coordinates.models import Coordinate
from users.models import Account


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


class TestCoordinatesManager(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account1 = Account.objects.create_account(user={"username": "maasldk", "password": "prasd56asgaas2mqwe"})
        cls.account2 = Account.objects.create_account(user={"username": "asfijasf", "password": "prasasgasfsfagmqwe"})
        cls.account3 = Account.objects.create_account(user={"username": "m9skmd", "password": "pragasgasdmqwe"})
        cls.account4 = Account.objects.create_account(user={"username": "masfkk", "password": "praagsdmqwe"})
        cls.account5 = Account.objects.create_account(user={"username": "ajsdnasd", "password": "prasdmqweas98df"})
        cls.accounts = [cls.account5, cls.account4, cls.account3, cls.account2, cls.account1]
        for ac in cls.accounts:
            Coordinate.coordinate_manager.create(random.uniform(20, 22), random.uniform(100, 102), ac)

    def test_filter_time_instance(self):
        filter_time_coords = Coordinate.coordinate_manager.filter_time()
        self.assertIsInstance(filter_time_coords, filter)

    def test_filter_time_count(self):
        filter_time_coords = Coordinate.coordinate_manager.filter_time()
        self.assertEqual(len([*filter_time_coords]), len(self.accounts))

    def test_all_near_instance(self):
        all_near_coords = Coordinate.coordinate_manager.all_near(self.account1.coordinate)
        self.assertIsInstance(all_near_coords, filter)

    def test_all_near_user_exclude(self):
        Coordinate_custom = Coordinate
        Coordinate_custom.coordinate_manager.distance_needed = 3_000_000
        all_near_coords = Coordinate_custom.coordinate_manager.all_near(self.account1.coordinate)
        self.assertNotIn(self.account1.coordinate, all_near_coords)

    def test_all_near_user_count(self):
        Coordinate_custom = Coordinate
        Coordinate_custom.coordinate_manager.distance_needed = 3_000_000
        all_near_coords = Coordinate_custom.coordinate_manager.all_near(self.account1.coordinate)
        self.assertEqual(len([*all_near_coords]), len(self.accounts) - 1)

    # def test_deactivate(self):
    #     self.assertIsInstance(self.account1.coordinate, Coordinate)
    #     Coordinate.coordinate_manager.deactivate(self.account1)
    #     self.account1.refresh_from_db()
    #     print(self.account1.coordinate)
    #     with self.assertRaises(ObjectDoesNotExist):
    #         print(self.account1.coordinate)
