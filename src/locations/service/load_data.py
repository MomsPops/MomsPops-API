from locations.models import City, Region
import json


def load_regions() -> None:
    with open("locations/data/russia_regions.json") as file:
        regions = json.load(file)

    for r in regions:
        try:
            Region.objects.create(**r)
        except Exception:
            pass


def load_cities() -> None:
    with open("locations/data/russia_cities.json") as file:
        cities = json.load(file)

    for c in cities:
        try:
            City.objects.create(
                id=c['id'], name=c['name'],
                region_id=c['region']
            )
            print(c)
        except Exception:
            pass


def load_locations() -> None:
    load_regions()
    load_cities()
