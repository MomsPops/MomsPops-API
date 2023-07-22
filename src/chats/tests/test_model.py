from chats.models import Chat, ChatMessage, Group, GroupMessage, Message, MessageMediaFile
from coordinates.models import Coordinate
from service.fixtues import TestChatGroupFixture


class GroupTest(TestChatGroupFixture):
    """Group model test."""
    def test_create_group(self):
        """Group creation test."""

        # Group creation without account test
        group1 = Group.group_manager.create_group(title="First Group")
        self.assertTrue(group1 is not None)
        self.assertEqual(group1.location_coordinate, None)

        # Group creation without coordinates test
        account_without_coord = self.user_account
        group2 = Group.group_manager.create_group(title="Second Group", account=account_without_coord)
        self.assertTrue(group2 is not None)
        self.assertEqual(group2.location_coordinate, None)

        coordinate = Coordinate.objects.create(lat=1, lon=2)
        self.assertTrue(coordinate is not None)

        # Group creation with coordinates and members test
        account_with_coord = self.user_account
        account_with_coord.coordinate = coordinate
        group3 = Group.group_manager.create_group(title="Third Group", account=account_with_coord)
        self.assertTrue(group3 is not None)
        self.assertEqual(account_with_coord.coordinate, coordinate)
        self.assertEqual(group3.location_coordinate, coordinate)
        self.assertTrue(group3.members is not None)
        self.assertEqual(group3.members.first(), account_with_coord)

        # Group image test
        self.assertFalse(group3.img_preview)
        group3.img_preview = self.uploaded
        self.assertTrue(group3.img_preview is not None)


class ChatTest(TestChatGroupFixture):
    """Chat creation test."""

    def test_create_simple_chat(self):
        """Simple chat creation test."""
        new_chat = Chat.chat_manager.create_standart_chat(self.user_account, self.user2_account)
        self.assertTrue(new_chat is not None)
        self.assertEqual(new_chat.type, 'STND')
        self.assertTrue(self.user_account in new_chat.members.all())
        self.assertTrue(self.user2_account in new_chat.members.all())
        self.assertEqual(Chat.objects.count(), 3)

    def test_create_custom_chat(self):
        """Custom chat creation test."""
        list_of_account = [self.user_account, self.user2_account, self.user3_account]
        new_chat = Chat.chat_manager.create_custom_chat(list_of_account)
        self.assertTrue(new_chat is not None)
        self.assertEqual(new_chat.type, 'CSTM')
        self.assertTrue(self.user_account in new_chat.members.all())
        self.assertTrue(self.user2_account in new_chat.members.all())
        self.assertTrue(self.user3_account in new_chat.members.all())

    def test_get_all_chats_by_account(self):
        chats = Chat.chat_manager.get_all_chats_by_account(self.user3_account)
        self.assertEqual(len(chats), 1)

    def test_leave_chat(self):
        self.simple_chat.leave_chat(self.user2_account)
        self.assertEqual(self.simple_chat.members.count(), 1)


class MessageTest(TestChatGroupFixture):
    """Message creation test."""

    def test_create_messages(self):
        """Message creation test."""
        message1 = Message.objects.create(account=self.user_account, text="Hello world")
        self.assertTrue(message1 is not None)
        self.assertEqual(Message.objects.count(), 2)

    def test_add_message_to_group(self):
        """Message relation witt groups and chats test."""
        message1 = Message.objects.create(account=self.user_account, text="Hello world")
        message2 = Message.objects.create(account=self.user_account, text="Foo Bar")

        # Message addition to group test
        message_for_group = GroupMessage.objects.create(group=self.group1, message=message1)
        self.assertTrue(message_for_group in self.group1.messages.all())

        # Message addition to group test
        self.simple_chat.messages.add(message2)
        self.assertTrue(message2 in self.simple_chat.messages.all())
        self.assertTrue(ChatMessage.objects.filter(chat=self.simple_chat, message=message2).exists())

    def test_create_message_with_media(self):
        """Media file for message creation test."""
        message = Message.objects.create(account=self.user_account, text="Hello world")
        self.assertFalse(message.media_files.exists())
        image = MessageMediaFile.objects.create(img=self.uploaded)
        message.media_files.add(image)
        self.assertTrue(image in message.media_files.all())
