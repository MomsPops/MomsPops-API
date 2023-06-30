from django.contrib.auth.models import User

# from django.db import transaction
from django.test import TestCase
from users.models import Account
from chats.models import Chat, Group, Message
from coordinates.models import Coordinate


class GroupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="test1",
            password="secret",
        )
        User.objects.create_user(
            username="test2",
            password="secret",
        )

    def test_create_group(self):
        group1 = Group.objects.create_group(title="First Group")
        self.assertTrue(group1 is not None)
        self.assertEqual(group1.location_coordinate, None)

        account_without_coord = Account.objects.create(user=User.objects.last())
        group2 = Group.objects.create_group(title="Second Group", account=account_without_coord)
        self.assertTrue(group2 is not None)
        self.assertEqual(group2.location_coordinate, None)

        coordinate = Coordinate.object.create(lat=1, lon=2)
        self.assertTrue(coordinate is not None)

        account_with_coord = Account.objects.create(user=User.objects.first(), coordinate=coordinate)
        group3 = Group.objects.create_group(title="Third Group", account=account_with_coord)

        self.assertTrue(group3 is not None)
        self.assertEqual(account_with_coord.coordinate, coordinate)
        self.assertEqual(group3.location_coordinate, coordinate)
        self.assertTrue(group3.members is not None)
        self.assertEqual(group3.members.first(), account_with_coord)


class ChatTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="test1")
        user2 = User.objects.create_user(username="test2")
        user3 = User.objects.create_user(username="test3")

        self.account1 = Account.objects.create(user=user1)
        self.account2 = Account.objects.create(user=user2)
        self.account3 = Account.objects.create(user=user3)

    def test_create_simple_chat(self):
        new_chat = Chat.objects.get_or_create_simple_chat(sender=self.account1, reciever=self.account2)
        self.assertTrue(new_chat is not None)

        self.assertTrue(self.account1 in new_chat.members.all())
        self.assertTrue(self.account2 in new_chat.members.all())
        self.assertEqual(Chat.objects.count(), 1)

    def test_create_custom_chat(self):
        list_of_account = [self.account1, self.account2, self.account3]
        new_chat = Chat.objects.create_custom_chat(account_list=list_of_account)

        self.assertTrue(new_chat is not None)

        self.assertTrue(self.account1 in new_chat.members.all())
        self.assertTrue(self.account2 in new_chat.members.all())
        self.assertTrue(self.account3 in new_chat.members.all())


class MessageTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="test1")
        user2 = User.objects.create_user(username="test2")
        user3 = User.objects.create_user(username="test3")

        self.account1 = Account.objects.create(user=user1)
        self.account2 = Account.objects.create(user=user2)
        self.account3 = Account.objects.create(user=user3)

        self.simmple_chat = Chat.objects.get_or_create_simple_chat(sender=self.account1, reciever=self.account2)
        self.simmple_chat = Chat.objects.get_or_create_simple_chat(sender=self.account1, reciever=self.account2)

    def test_create_messages(self):
        message1 = Message.objects.create(account=self.account1, text="Hello world")

        self.assertTrue(message1 is not None)
        self.assertEqual(Message.objects.count(), 1)
