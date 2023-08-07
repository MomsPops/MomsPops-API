from django.http import Http404
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.test import APITestCase
from django.core.exceptions import ObjectDoesNotExist
from service.fixtues import TestAccountFixture

from users.models import Account, FriendshipRequest
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


class TestFriendshipRequestModel(TestAccountFixture, APITestCase):

    def test_request_create_success(self):
        request = FriendshipRequest.friendship_request_manager.create_friendship_request(
            from_account=self.user_account,
            to_account=self.user2_account
        )
        self.assertEqual(request.from_account, self.user_account)
        self.assertEqual(request.to_account, self.user2_account)
        self.assertEqual(request.to_account.user.username, self.user2_account.user.username)

    def test_request_create_fail_same_account(self):
        with self.assertRaises(ValidationError):
            FriendshipRequest.friendship_request_manager.create_friendship_request(
                from_account=self.user2_account,
                to_account=self.user2_account
            )

    def test_request_create_fail_to_in_black_list(self):
        with self.assertRaises(PermissionDenied):
            self.user_account.black_list.add(self.user2_account)
            FriendshipRequest.friendship_request_manager.create_friendship_request(
                from_account=self.user_account,
                to_account=self.user2_account
            )

    def test_request_create_fail_from_in_black_list(self):
        with self.assertRaises(PermissionDenied):
            self.user2_account.black_list.add(self.user_account)
            FriendshipRequest.friendship_request_manager.create_friendship_request(
                from_account=self.user_account,
                to_account=self.user2_account
            )

    def test_request_accept(self):
        user_account_friends_amount_before = len(self.user_account.friends.all())
        user2_account_friends_amount_before = len(self.user2_account.friends.all())
        request = FriendshipRequest.friendship_request_manager.create_friendship_request(
            from_account=self.user_account,
            to_account=self.user2_account
        )
        request.accept()
        user_account_friends = self.user_account.friends.all()
        user2_account_friends = self.user2_account.friends.all()
        self.assertEqual(len(user_account_friends) - user_account_friends_amount_before, 1)
        self.assertEqual(len(user2_account_friends) - user2_account_friends_amount_before, 1)
        self.assertIn(self.user_account, user2_account_friends)
        self.assertIn(self.user2_account, user_account_friends)
