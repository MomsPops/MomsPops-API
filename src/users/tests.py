from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

from .models import User


class UserSettings(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_data = dict(
            username="michael7nightingale",
            first_name='Michael',
            last_name='Nightingale',
            email='mightbe@mail.ru',
            password='qwerty23'
        )
        cls.superuser_data = dict(
            username='admin290',
            password="apdasda1294",
            first_name="string",
            email='suslanchikmopl@mail.ru'
        )
        cls.user = User.objects.create(**cls.user_data)
        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

        cls.user_client = APIClient()
        cls.set_credentials(cls.user_client,
                            cls.user_data['username'], cls.user_data['password'])

        cls.superuser_client = APIClient()
        cls.set_credentials(cls.superuser_client,
                            cls.superuser_data['username'], cls.superuser_data['password'])

    @classmethod
    def set_credentials(cls, client, username, password):
        tokens = cls.get_token(username, password)
        client.credentials(HTTP_AUTORIZATION="Bearer " + tokens['access'])

    @classmethod
    def get_token(cls, username, password):
        response = APIClient().post(
            path=reverse("token_obtain"),
            data={"username": username, "password": password}
        )
        return response.json()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.superuser.delete()


class TestUserModel(UserSettings):

    def test_login(self):
        user = User.objects.login(
            username=self.user_data['username'],
            password=self.user_data['password']
        )
        self.assertEqual(user, self.user)

    def test_login_fail(self):
        user = User.objects.login(
            username='some_username',
            password='some_psw'
        )
        self.assertEqual(user, None)


class TestUserUrl(UserSettings):

    def setUp(self) -> None:
        self.user1_data = {
            "username": "1asfaskda",
            "password": "a9r12uru1n",
            "email": "suialsdn@gmail.ru",
        }

        response = self.client.post(
            path=reverse("token_obtain"),
            data={"username": self.user_data['username'],
                  'password': self.user_data["password"]}
        )
        self.assertEqual(response.status_code, 200)
        self.access_token = response.json()['access']
        self.refresh_token = response.json()['refresh']
        self.headers = {"Authentication": f"Bearer {self.access_token}"}

    def test_create(self):
        response = self.client.post(
            path=reverse("users_create"),
            data=self.user1_data,
        )
        self.assertEqual(response.status_code, 200)

    def test_create_fail(self):
        response = self.client.post(reverse("users_create"))
        self.assertEqual(response.status_code, 403)

    # def test_update(self):
    #     client = APIClient()
    #     client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
    #     user_data = self.user_data.copy()
    #     user_data.update(first_name='Jager')
    #     response = client.put(
    #         path=reverse("users_update"),
    #         data=user_data
    #     )
    #     self.assertEqual(response.status_code, 200)



