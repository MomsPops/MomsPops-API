from rest_framework.test import APITestCase

from locations.models import City, Region


class TestLocations(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(TestLocations, cls).setUpClass()
        cls.region1 = Region.objects.create(name='Абхадул')
        cls.region2 = Region.objects.create(name='Королевство франков')
        cls.city1 = City.objects.create(name='Москва', region=cls.region1)
        cls.city2 = City.objects.create(name='Париж', region=cls.region2)

    def test_region_create(self):
        region = Region.objects.create(
            name="Свердловская область"
        )
        assert region.name == "Свердловская область"

    def test_city_create(self):
        city = City.objects.create(
            name="Ектеринбург", region=self.region1
        )
        assert city.region == self.region1
