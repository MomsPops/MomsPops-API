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

    def test_create_account(self):
        user1 = User.objects.create(username="test_user1")
        # user2 = User.objects.create(username="test_user2")
        account1 = Account.objects.create(user=user1)

        self.assertTrue(account1 is not None)
        self.assertEqual(Account.objects.count(), 1)

        user_data = {"username": "created_test_user1", "email": "test@mail.com"}
        
        account2 = Account.objects.create_account(user=user_data)
        self.assertTrue(account2 is not None)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(account2.birthday, None)
        self.assertEqual(account2.bio, None)
        self.assertEqual(account2.status, "")
        self.assertEqual(account2.city, None)

        with transaction.atomic():
            # check create without username
            try:
                Account.objects.create_account(user={"email": "test@mail.com"})
            except Exception:
                pass
        self.assertEqual(Account.objects.count(), 2)
