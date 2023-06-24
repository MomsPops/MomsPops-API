from rest_framework.test import APITestCase
from service.fixtues import TestUserFixture

from coordinates.models import Coordinate


# class TestCoordinate(TestUserFixture):
#
#     def test_create_coordinate(self):
#         coord = Coordinate.object.create(
#             lon=0,
#             lat=20,
#             account=...
#         )
