from rest_framework.test import APITestCase
from django.core.exceptions import ObjectDoesNotExist
from service.fixtues import TestAccountFixture

from users.models import Account
from profiles.models import Profile


class TestAccountModel(TestAccountFixture, APITestCase):

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
        self.assertEqual(account.city, self.city1)

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
        self.assertIsInstance(account.profile, Profile)
        self.assertEqual(account.city, self.city2)

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

    def test_account_deactivate(self):
        self.assertTrue(self.user_account.user.is_active)
        Account.objects.deactivate(self.user_account)
        self.assertFalse(self.user_account.user.is_active)
        Account.objects.deactivate(self.user_account)
        self.assertFalse(self.user_account.user.is_active)

    def test_account_activate(self):
        self.assertTrue(self.superuser_account.user.is_active)
        Account.objects.deactivate(self.superuser_account)
        self.assertFalse(self.superuser_account.user.is_active)
        Account.objects.activate(self.superuser_account)
        self.assertTrue(self.superuser_account.user.is_active)
        Account.objects.activate(self.superuser_account)
        self.assertTrue(self.superuser_account.user.is_active)
