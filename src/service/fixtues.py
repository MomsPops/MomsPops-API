from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from locations.models import Region, City
from users.models import Account


class TestUserFixture(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User(username='michael7', password='rammqueen')
        cls.user.set_password('rammqueen')
        cls.user.save()
        cls.superuser = User.objects.create_superuser(username='admin', password='password')
        cls.superuser.set_password('passowrd')
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


class TestAccountFixture(TestUserFixture):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_account = Account.objects.create_account()
