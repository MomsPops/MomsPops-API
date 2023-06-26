from service.fixtues import TestLocationFixture

from locations.models import City, Region


class TestLocations(TestLocationFixture):

    def test_region_create(self):
        region = Region.objects.create(
            name="Свердловская область"
        )
        self.assertEqual(region.name, "Свердловская область")

    def test_city_create(self):
        city = City.objects.create(
            name="Екатеринбург", region=self.region1
        )
        self.assertEqual(city.region, self.region1)
