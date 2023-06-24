from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import Account
from service.fixtues import TestLocationFixture, TestUserFixture


class TestAccountView(TestLocationFixture, TestUserFixture, APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account = Account.objects.create(
            city=cls.city1,
            user=cls.user
        )

    def test_account_create(self):
        data = {
            "region_name": self.city1.region.name,
            "city_name": self.city1.name,
            "user": {
                "username": "asdoaipodija",
                "password": "super_mouser9100",
                "first_name": "Snoop",
                'last_name': "Dogg",
                "email": "mokky@mail.ru"
            }
        }
        response = self.client.post(path=reverse("accounts_create"), data=data, format='json')
        assert response.status_code == 201
        user_data = data['user']
        user_data.pop("password")
        data['user'] = user_data
        assert response.json() == data

    def test_account_create_fail(self):
        data = {
            "region_name": self.city1.region.name,
            "city_name": self.city1.name,
            "user": {
                "username": "asdoaipodija",
                "password": "super_mouser9100",
            }
        }
        response = self.client.post(path=reverse("accounts_create"), data=data, format='json')
        assert response.status_code == 400
        assert response.json() == {'user': {'first_name': ['This field is required.'],
                                            'last_name': ['This field is required.']}}

    def test_account_retrieve(self):
        response = self.user_client.get(reverse("accounts_me"))
        assert response.status_code == 200
        assert response.json() == {
            "city_name": self.city1.name,
            "region_name": self.city1.region.name,
            "user": {
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            }
        }
