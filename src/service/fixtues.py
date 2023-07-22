from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient

from chats.models import Chat, Group, Message
from locations.models import Region, City
from notifications.models import NotificationAccount, Notification
from profiles.models import Profile, Post
from users.models import Account, User


class TestUserFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User(username='michael7123', password='rammqueen123')
        cls.user.set_password('rammqueen123')
        cls.user.save()
        cls.superuser = User.objects.create_superuser(username='admin12', password='password12')
        cls.superuser.set_password('password12')
        cls.superuser.save()

        cls.user2 = User(username='mi123achael7123', password='rammqsfasgueen123')
        cls.user2.set_password('mi123achael7123')
        cls.user2.save()
        cls.user3 = User(username='a0sdiami123achael7123', password='rammqsfasgueen123')
        cls.user3.set_password('a0sdiami123achael7123')
        cls.user3.save()

        cls.user_client = APIClient()
        cls.user_client.force_login(cls.user)
        cls.superuser_client = APIClient()
        cls.superuser_client.force_login(cls.superuser)
        cls.user2_client = APIClient()
        cls.user2_client.force_login(cls.user2)
        cls.user3_client = APIClient()
        cls.user3_client.force_login(cls.user3)


class TestLocationFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.region1 = Region.objects.create(name='Абхадул')
        cls.region2 = Region.objects.create(name='Королевство франков')
        cls.city1 = City.objects.create(name='Москва', region=cls.region1)
        cls.city2 = City.objects.create(name='Париж', region=cls.region2)


class TestAccountFixture(TestUserFixture, TestLocationFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_account = Account.objects.create(
            city=cls.city1,
            user=cls.user
        )
        cls.superuser_account = Account.objects.create(
            city=cls.city2,
            user=cls.superuser
        )

        cls.user2_account = Account.objects.create(user=cls.user2)
        cls.user3_account = Account.objects.create(user=cls.user3)


class TestProfileFixture(TestAccountFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_pofile = Profile.objects.create(
            account=cls.user_account
        )
        cls.superuser_pofile = Profile.objects.create(
            account=cls.superuser_account
        )


class TestPostFixture(TestProfileFixture, APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_post = Post.objects.create(
            profile=cls.user_pofile
        )
        cls.superuser_post = Post.objects.create(
            profile=cls.superuser_pofile
        )


class TestNotificationAccountFixture(TestAccountFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.notification_1 = Notification.objects.create(text="hello everybody!")
        cls.notification_account_1_user_2 = NotificationAccount.objects.create(
            account=cls.user2_account,
            notification=cls.notification_1
        )
        cls.notification_account_1_user_3 = NotificationAccount.objects.create(
            account=cls.user3_account,
            notification=cls.notification_1
        )

        cls.notification_2 = Notification.objects.create(text="New court is opened!")
        cls.notification_account_2_user_1 = NotificationAccount.objects.create(
            account=cls.user_account,
            notification=cls.notification_2
        )


class TestChatGroupFixture(TestAccountFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.message = Message.objects.create(text='Test', account=cls.user_account)
        cls.simple_chat = Chat.objects.create(type="STND")
        cls.simple_chat.members.add(cls.user_account, cls.user2_account)
        cls.simple_chat_2 = Chat.objects.create(type="STND")
        cls.simple_chat_2.members.add(cls.user_account, cls.user3_account)
        cls.group1 = Group.group_manager.create_group(title="First Group")
        cls.group2 = Group.group_manager.create_group(title="Second Group")
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
