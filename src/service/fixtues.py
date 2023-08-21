from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APIClient, APITestCase

from chats.models import Group, GroupMessage
from coordinates.models import Coordinate
from events.models import Event
from locations.models import City, Region
from notifications.models import Notification, NotificationAccount
from profiles.models import Post, Profile
from users.models import Account, FriendshipRequest, User


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


class TestEventsFixture(TestProfileFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event1 = Event.objects.create(
            creator=cls.user2_account,
            title="first_event",
            description="First event description.",
            time_started=timezone.now() + timedelta(hours=1),
            time_finished=timezone.now() + timedelta(hours=2)
        )
        coordinates_1 = Coordinate.objects.create(
            lat=10,
            lon=20,
        )
        cls.event1.coordinate = coordinates_1
        cls.event1.save()
        cls.event2 = Event.objects.create(
            creator=cls.user3_account,
            title="second_event",
            description="Second event description.",
            time_started=timezone.now() + timedelta(hours=2),
            time_finished=timezone.now() + timedelta(hours=4)
        )
        coordinates_2 = Coordinate.objects.create(
            lat=30,
            lon=20,
        )
        group_2 = Group.objects.create_group("second_event", cls.user3_account)
        cls.event2.group = group_2
        cls.event2.coordinate = coordinates_2
        cls.event2.save()
        cls.event3 = Event.objects.create(
            creator=cls.user3_account,
            title="past_event",
            description="Past event description.",
            time_started=timezone.now() - timedelta(hours=4),
            time_finished=timezone.now() - timedelta(hours=2)
        )
        coordinates_3 = Coordinate.objects.create(
            lat=34,
            lon=28,
        )
        group_3 = Group.objects.create_group("past_event", cls.user3_account)
        cls.event3.coordinate = coordinates_3
        cls.event3.group = group_3
        cls.event3.save()
