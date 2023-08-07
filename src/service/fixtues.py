from rest_framework.test import APITestCase, APIClient

from coordinates.models import Coordinate
from locations.models import Region, City
from notifications.models import NotificationAccount, Notification
from profiles.models import Profile, Post
from users.models import Account, User, FriendshipRequest
from chats.models import Group, GroupMessage


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
        cls.superuser_account.friends.add(cls.user3_account)


class TestFriendshipRequestFixture(TestAccountFixture, APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.friendship_request_from_1_to_2 = FriendshipRequest.friendship_request_manager.create_friendship_request(
            from_account=cls.user_account,
            to_account=cls.user2_account
        )
        cls.friendship_request_from_3_to_2 = FriendshipRequest.friendship_request_manager.create_friendship_request(
            from_account=cls.user3_account,
            to_account=cls.user2_account
        )


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
        cls.user2_pofile = Profile.objects.create(
            account=cls.user2_account
        )
        cls.user3_pofile = Profile.objects.create(
            account=cls.user3_account
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


class TestGroupFixture(TestProfileFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group1 = Group.group_manager.create_group(
            title="Football league.",
            account=cls.user_account
        )
        Coordinate.coordinate_manager.create(
            lat=20,
            lon=20,
            source=cls.group1
        )
        cls.group1.save()
        cls.group2 = Group.group_manager.create_group(
            title="C# is better than Python",
            account=cls.user2_account
        )
        Coordinate.coordinate_manager.create(
            lat=20.001,
            lon=20,
            source=cls.group2
        )
        cls.group2.members.add(cls.user_account)
        cls.group2.save()
        cls.group2_message1 = GroupMessage.group_message_manager.create(
            text="I think Unity sucks. Unreal, but Unreal is cooler.",
            group=cls.group2,
            account=cls.user_account
        )
        cls.group2_message2 = GroupMessage.group_message_manager.create(
            text="However I love VS.",
            group=cls.group2,
            account=cls.user_account
        )
        cls.group3 = Group.group_manager.create_group(
            title="Snoop Dogg concert.",
            account=cls.user3_account
        )
        Coordinate.coordinate_manager.create(
            lat=20.01,
            lon=20,
            source=cls.group3
        )
