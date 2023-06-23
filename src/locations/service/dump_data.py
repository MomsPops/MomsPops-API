from locations.models import City, Region
import json


def dump_regions() -> None:
    with open("locations/data/russia_regions.json") as file:
        regions = json.load(file)

    for r in regions:
        try:
            Region.objects.create(**r)
        except Exception:
            pass


def dump_cities() -> None:
    with open("locations/data/russia_cities.json") as file:
        cities = json.load(file)

    for c in cities:
        try:
            City.objects.create(id=c['id'], name=c['name'], region=Region.objects.get(id=c['region']))
        except Exception:
            pass


def dump_locations() -> None:
    dump_regions()
    dump_cities()
