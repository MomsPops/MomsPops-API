# from django.contrib.auth.models import User
# from django.db import transaction
# from django.test import TestCase
# from users.models import Account
# from chats.models import Chat, Message


# class ChatTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         user1 = User.objects.create_user(
#             username="test1",
#             password="secret",
#         )
#         user2 = User.objects.create_user(
#             username="test2",
#             password="secret",
#         )
#         Account.objects.create(user=user1)
#         Account.objects.create(user=user2)
#         ChatType.objects.create(title="test_chat_title1")

#     def test_create_chat(self):
#         account = Account.objects.first()
#         chat_type = ChatType.objects.first()

#         with transaction.atomic():
#             # check create without type
#             try:
#                 Chat.objects.create(owner=account)
#             except Exception:
#                 pass
#         self.assertEqual(Chat.objects.count(), 0)

#         chat = Chat.objects.create(owner=account, type=chat_type)

#         self.assertTrue(chat is not None)
#         self.assertEqual(Chat.objects.count(), 1)

#         chat = Chat.objects.create(type=chat_type)
#         self.assertTrue(chat is not None)
#         self.assertEqual(Chat.objects.count(), 2)

#     def test_add_members_in_chat(self):
#         account1 = Account.objects.first()
#         account2 = Account.objects.last()
#         chat_type = ChatType.objects.first()

#         chat = Chat.objects.create(type=chat_type)

#         self.assertEqual(chat.owner, None)

#         chat.members.add(account1)
#         self.assertEqual(chat.members.count(), 1)
#         chat.members.add(account2)
#         self.assertEqual(chat.members.count(), 2)

#         chat.members.add(account2)
#         self.assertEqual(chat.members.count(), 2)

#     def test_create_messages(self):
#         chat_type = ChatType.objects.first()
#         account = Account.objects.first()
#         chat = Chat.objects.create(type=chat_type)

#         message = Message.objects.create(
#             chat=chat, account=account, text="test message"
#         )

#         self.assertTrue(message is not None)
#         self.assertEqual(message.text, "test message")
#         self.assertEqual(message.viewed, False)
#         self.assertEqual(message.account, account)

#         self.assertEqual(chat.messages.count(), 1)
#         self.assertEqual(chat.messages.first(), message)
