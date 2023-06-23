import os
import googlemaps
from dotenv import load_dotenv


load_dotenv()


def get_location_details(geo_point):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(api_key)
    reverse_geocode_result = gmaps.reverse_geocode(geo_point, language='ru')

    address_components = reverse_geocode_result[0]['address_components']

    city = ''
    street = ''
    district = ''

    for component in address_components:
        types = component['types']
        if 'locality' in types:
            city = component['long_name']
        if 'route' in types:
            street = component['long_name']
        if 'sublocality' in types:
            district = component['long_name']

    result = "Город: " + city
    if street:
        result += ",\nУлица: " + street
    if district:
        result += ",\nРайон: " + district

    return result
