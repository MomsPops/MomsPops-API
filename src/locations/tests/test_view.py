from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from locations.models import Region, City


class TestUserSettings(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(TestUserSettings, cls).setUpClass()
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


class TestLoadData(TestUserSettings):

    def test_load_data_regions(self):
        response = self.superuser_client.post(reverse("locations_load_data_regions"))
        assert response.status_code == 200
        assert response.json() == {"detail": "Regions` data loaded successfully."}

    def test_load_data_fail(self):
        response = self.user_client.post(reverse("locations_load_data"))
        assert response.status_code == 403
        assert response.json() == {'detail': 'You do not have permission to perform this action.'}


class TestViews(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        cls.region1 = Region.objects.create(name='Абхадул')
        cls.region2 = Region.objects.create(name='Королевство франков')
        cls.city1 = City.objects.create(name='Москва', region=cls.region1)
        cls.city2 = City.objects.create(name='Париж', region=cls.region2)

    def test_location_list(self):
        response = self.client.get(reverse("locations_all"))
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": self.region1.id,
                "name": self.region1.name,
                "cities": [
                    {
                        "id": self.city1.id,
                        "name": self.city1.name
                    }
                ]
            },
            {
                "id": self.region2.id,
                "name": self.region2.name,
                "cities": [
                    {
                        "id": self.city2.id,
                        "name": self.city2.name
                    }
                ]
            }
        ]
