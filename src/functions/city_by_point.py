from opencage.geocoder import OpenCageGeocode


API_KEY = 'b8fcd228862e4ee9b8efd5817fac44ea'
geo_point = '55.694170717163146, 37.8804331967079'


def get_location_details(geo_point, API_KEY):
    lat, lon = geo_point.split(', ')

    geocoder = OpenCageGeocode(API_KEY)
    results = geocoder.reverse_geocode(float(lat), float(lon), language='ru')

    if results:
        location = results[0]
        components = location['components']

        city = components.get('city', '')
        road = components.get('road', '')

        return f"Город: {city}, Улица: {road}"

    return "Местоположение не найдено"


print(get_location_details(geo_point, API_KEY))
