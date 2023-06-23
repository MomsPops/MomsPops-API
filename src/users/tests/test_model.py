from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase
from django.contrib.auth import authenticate
from users.models import Account


class AccountTest(TestCase):
    def test_authenticate_user(self):
        User.objects.create_user(
            username="test1",
            password="secret",
        )
        user = authenticate(username="test1", password="secret")
        self.assertTrue((user is not None) and user.is_authenticated)

    def create_account_test(self):
        user1 = User.objects.create(username="test_user1")
        user1 = User.objects.create(username="test_user1")
        user2 = User.objects.last()
        account1 = Account.objects.create(user=user1)

        self.assertTrue(account1 is not None)
        self.assertEqual(Account.objects.count(), 1)

        # account2 = Account.objects.create_account
