from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from coordinates.models import Coordinate
from service.fixtues import TestAccountFixture


class TestCoordinateView(TestAccountFixture, APITestCase):

    def test_coordinate_set(self):
        data = {
            "lat": 10, "lon": 10
        }
        response = self.user_client.post(reverse("coordinates_create"), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)
        self.user_account.refresh_from_db()
        self.assertEqual(self.user_account.coordinate.lat, data['lat'])

    def test_coordinate_update(self):
        data = {
            "lat": 10, "lon": 100
        }
        response = self.user_client.post(reverse("coordinates_create"), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)
        self.user_account.refresh_from_db()
        self.assertEqual(self.user_account.coordinate.lat, data['lat'])
        new_data = {
            "lat": -11.123, "lon": .108
        }
        response = self.user_client.post(reverse("coordinates_create"), data=new_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), new_data)
        self.user_account.refresh_from_db()
        self.assertEqual(self.user_account.coordinate.lon, new_data['lon'])

    def test_coordinate_fail(self):
        data = {
            "lat": 90, "lon": 191
        }
        response = self.user_client.post(reverse("coordinates_create"), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'lon': ['Ensure this value is less than or equal to 180.0.']})
        self.user_account.refresh_from_db()
        self.assertEqual(self.user_account.coordinate, None)
