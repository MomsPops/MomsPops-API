from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.core.files import File
from django.urls import reverse

from .models import Profile, Note, User


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


class ProfileSettings(UserSettings):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        file = File(open("media/profiles/images_1.png", 'rb'))
        cls.profile_data = {
            "user": cls.user,
            "photo": file,
            "country": "Russia",
            "city": "Ekaterinburg",
            "interests": "Programming",
            "bio": "I was born in RF. I am living.",
            "birth_date": "2023-06-19"
        }
        cls.profile = Profile.objects.create(**cls.profile_data)


class TestProfileModel(ProfileSettings):

    def setUp(self) -> None:
        self.user_client = APIClient()
        self.set_credentials(self.user_client,
                             self.user_data['username'], self.user_data['password'])
        self.user_client.force_login(self.user)

        self.superuser_client = APIClient()
        self.set_credentials(self.superuser_client,
                             self.superuser_data['username'], self.superuser_data['password'])
        self.user_client.force_login(self.superuser)

    def test_create_profile(self):
        # file = open("../media/profiles/images_1.png")
        profile_data = {
            # "photo": file,
            "country": "Russia",
            "city": "Moscow",
            "interests": "Programming, painting",
            "bio": "I was born in RF. I am living. I like sport.",
            "birth_date": "2023-06-19"
        }
        superuser_client = APIClient()
        superuser_client.credentials(HTTP_AUTHORIZAION="Brearer " + self.get_token(
            self.superuser_data['username'], self.superuser_data['password']
        )['access'])
        response = superuser_client.post(
            path=reverse("profiles_create"),
            data=profile_data
        )
        print(response.json())
        self.assertEqual(response.status_code, 200)




