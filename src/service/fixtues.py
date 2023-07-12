from rest_framework.test import APITestCase, APIClient

from locations.models import Region, City
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
