from rest_framework.test import APITestCase
from django.core.exceptions import ObjectDoesNotExist
from service.fixtues import TestUserFixture, TestLocationFixture

from users.models import Account


class TestAccountModel(TestUserFixture, TestLocationFixture, APITestCase):

    def test_account_create(self):
        user_data = {
            "username": "harry_potter",
            "password": "asda-sd3r2io3trn",
            "first_name": "Snoop",
            "last_name": "Dogg"
        }
        account = Account.objects.create_account(
            user=user_data,
            city_name=self.city1.name,
            region_name=self.city1.region.name
        )
        assert account.city == self.city1

    def test_account_create_2(self):
        user_data = {
            "username": "asdad;las;ldkas;ldka",
            "password": "0a9d000"
        }
        account = Account.objects.create_account(
            user=user_data,
            city_name=self.city2.name,
            region_name=self.city2.region.name
        )
        assert account.city == self.city2

    def test_account_create_fail(self):
        user_data = {
            "username": "asdad;las;ldkas;ldka",
            "password": "0a9d000"
        }
        with self.assertRaises(ObjectDoesNotExist):
            Account.objects.create_account(
                user=user_data,
                city_name=self.city1.name,
                region_name=self.region2.name
            )
