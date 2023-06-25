import json

import vk


class LocationParser:

    @classmethod
    def parse_cities(cls, api: vk.API, filename=None):
        cities = api.database.getCities(count=10 ** 3, need_all=1)['items']
        if filename is not None:
            with open(filename, 'w') as file:
                json.dump(cities, file)
        else:
            return cities


if __name__ == '__main__':
    api_ = vk.API(access_token="TOKEN", v=5.81)
    LocationParser.parse_cities(api_, "files/russia_cities.json")
