import vk
import json
import time


class LocationParser:

    def __init__(self, api):
        self.api = api

    def parse_regions(self) -> list[dict]:
        regions_response = self.api.database.getRegions(country_id=1, count=10**3)['items']
        regions = []
        for reg in regions_response:
            regions.append({
                "id": reg['id'],
                "name": reg['title']
            })
        return regions

    def parse_locations(self, c_filename=None, r_filename=None) -> None:
        regions = self.parse_regions()
        if r_filename is not None:
            with open(r_filename, 'w') as file:
                json.dump(regions, file)
        else:
            print(regions)

        cities = []
        for reg in regions:
            print(f"Region: {reg['name']}")
            cities_reg = self.parse_cities(reg['id'])
            cities.extend(cities_reg)
        if c_filename is not None:
            with open(c_filename, 'w') as file:
                json.dump(cities, file)
        else:
            print(cities)

    def parse_cities(self, reg_id) -> list[dict]:
        cities = []
        cities_ids = set()
        for ok in range(3):
            time.sleep(0.5)
            # print(f"Offset: {ok}")
            cities_response = self.api.database.getCities(
                count=10**3, need_all=1, region_id=reg_id, offset=ok*10**3
            )['items']
            for idx, city in enumerate(cities_response):
                id_ = city.get("id")
                if id_ not in cities_ids:
                    cities.append({
                        "id": id_,
                        "name": city['title'],
                        "region": reg_id,
                    })
                    cities_ids.add(id_)
        return cities


if __name__ == '__main__':
    TOKEN = "vk1.a.UEQ9gmOD1UklHN71ctztqP7VsGdYx1br-bXq3pUt4DAsnd_X9LvLFHrIrX5XKWqSDNXrV3Yd\
    zr8a_QkU5OuzjKx-Z0s65T4ZCBi-xYUORiymL3rD0pqjxbR__qK_CUg-BuYO7TOPeDb5R8SnNtKGtUgyNqit21y\
    XNIMhu1Pd-OHbmME4fwEy_y9wQXplEeng"
    api_ = vk.API(access_token=TOKEN, v=5.81)
    LocationParser(api_).parse_locations("files/russia_cities.json", "files/russia_regions.json")
