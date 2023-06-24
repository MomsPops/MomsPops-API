from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from locations.models import Region, City
from profiles.models import Profile
from users.models import Account


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
        cls.user_client = APIClient()
        cls.user_client.force_login(cls.user)
        cls.superuser_client = APIClient()
        cls.superuser_client.force_login(cls.superuser)


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


class TestProfileFixture(TestAccountFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_pofile = Profile.objects.create(
            account=cls.user_account
        )
