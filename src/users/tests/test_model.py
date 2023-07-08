from django.http import Http404
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


class TestBlockUserModel(TestAccountFixture, APITestCase):

    def test_block_user(self):
        amount_blocked_before = self.user_account.black_list.count()
        Account.objects.block_user(self.user_account, self.user2.username)
        self.user_account.refresh_from_db()

        self.assertEqual(self.user_account.black_list.count() - amount_blocked_before, 1)
        self.assertTrue(self.user_account.black_list.filter(user=self.user2).exists())

    def test_block_user_fail_yourself(self):
        with self.assertRaises(ValueError):
            Account.objects.block_user(account=self.user_account, username=self.user_account.user.username)

    def test_block_user_fail_not_found(self):
        with self.assertRaises(Http404):
            Account.objects.block_user(account=self.user_account, username="Not_found_name")

    def test_user_unblock(self):
        amount_blocked_before = self.user_account.black_list.count()
        Account.objects.block_user(self.user_account, self.user2.username)
        self.user_account.refresh_from_db()
        self.assertEqual(self.user_account.black_list.count() - amount_blocked_before, 1)
        Account.objects.unblock_user(self.user_account, self.user2.username)
        self.assertEqual(self.user_account.black_list.count(), amount_blocked_before)

    def test_unblock_user_fail_yourself(self):
        with self.assertRaises(ValueError):
            Account.objects.unblock_user(account=self.user_account, username=self.user_account.user.username)

    def test_unblock_user_fail_not_found(self):
        with self.assertRaises(Http404):
            Account.objects.unblock_user(account=self.user_account, username="Not_found_name")
