from django.core.files.uploadedfile import SimpleUploadedFile

from chats.models import Chat, ChatMessage, Group, GroupMessage, Message, MessageMediaFile
from coordinates.models import Coordinate
from service.fixtues import TestAccountFixture


class GroupTest(TestAccountFixture):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

    def test_create_group(self):
        """Group creation test."""

        # Group creation without account test
        group1 = Group.group_manager.create_group(title="First Group", account=self.user2_account)
        self.assertTrue(group1 is not None)

        # Group creation without coordinates test
        account_without_coord = self.user_account
        group2 = Group.group_manager.create_group(title="Second Group", account=account_without_coord)
        self.assertTrue(group2 is not None)
        self.assertEqual(group2.coordinate, None)

        coordinate = Coordinate.objects.create(lat=1, lon=2)
        self.assertTrue(coordinate is not None)

        # Group creation with coordinates and members test
        account_with_coord = self.user_account
        account_with_coord.coordinate = coordinate
        group3 = Group.group_manager.create_group(
            title="Third Group",
            account=account_with_coord,
        )
        self.assertTrue(group3 is not None)
        self.assertEqual(account_with_coord.coordinate, coordinate)
        self.assertEqual(group3.coordinate, coordinate)
        self.assertTrue(group3.members is not None)
        self.assertEqual(group3.members.first(), account_with_coord)

        # Group image test
        self.assertFalse(group3.img_preview)
        group3.img_preview = self.uploaded
        self.assertTrue(group3.img_preview is not None)


class ChatTest(TestAccountFixture):
    """Chat creation test."""

    def test_create_simple_chat(self):
        """Simple chat creation test."""
        new_chat = Chat.objects.create(type='STND')
        new_chat.members.add(self.user_account, self.user2_account)
        self.assertTrue(new_chat is not None)
        self.assertTrue(self.user_account in new_chat.members.all())
        self.assertTrue(self.user2_account in new_chat.members.all())
        self.assertEqual(Chat.objects.count(), 1)

    def test_create_custom_chat(self):
        """Custom chat creation test."""
        list_of_account = [self.user_account, self.user2_account, self.user3_account]
        new_chat = Chat.objects.create(type='CSTM')
        new_chat.members.add(*list_of_account)
        self.assertTrue(new_chat is not None)
        self.assertTrue(self.user_account in new_chat.members.all())
        self.assertTrue(self.user2_account in new_chat.members.all())
        self.assertTrue(self.user3_account in new_chat.members.all())


class MessageTest(TestAccountFixture):
    """Message creation test."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.simple_chat = Chat.objects.create(type='STND')
        cls.simple_chat.members.add(cls.user_account, cls.user2_account)
        cls.group1 = Group.group_manager.create_group(title="First Group", account=cls.user_account)
        cls.group2 = Group.group_manager.create_group(title="Second Group", account=cls.user3_account)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

    def test_create_messages(self):
        """Message creation test."""
        message1 = Message.objects.create(account=self.user_account, text="Hello world")
        self.assertTrue(message1 is not None)
        self.assertEqual(Message.objects.count(), 1)

    def test_add_message_to_group(self):
        """Message relation witt groups and chats test."""
        message1 = Message.objects.create(account=self.user_account, text="Hello world")
        message2 = Message.objects.create(account=self.user_account, text="Foo Bar")

        # Message addition to group test
        message_for_group = GroupMessage.objects.create(group=self.group1, message=message1)
        self.assertTrue(message_for_group in self.group1.messages.all())

        # Message addition to group test
        message_for_chat = ChatMessage.objects.create(chat=self.simple_chat, message=message2)
        self.assertTrue(message_for_chat in self.simple_chat.messages.all())

    def test_create_message_with_media(self):
        """Media file for message creation test."""
        message = Message.objects.create(account=self.user_account, text="Hello world")
        self.assertFalse(message.media_files.exists())
        image = MessageMediaFile.objects.create(img=self.uploaded)
        message.media_files.add(image)
        self.assertTrue(image in message.media_files.all())
