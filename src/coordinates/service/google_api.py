import os
import googlemaps


def get_location_details(lat: float, lon: float) -> str:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(api_key)
    geo_point = f"{lat}, {lon}"
    reverse_geocode_result = gmaps.reverse_geocode(geo_point, language='ru')

    city = ''
    street = ''
    district = ''

    for component in reverse_geocode_result[0]['address_components']:
        types = component['types']
        if 'locality' in types:
            city = component['long_name']
        if 'route' in types:
            street = component['long_name']
        if 'sublocality' in types:
            district = component['long_name']

    result_parts = []
    if city:
        result_parts.append(f"Город: {city}")
    if street:
        result_parts.append(f"Улица: {street}")
    if district:
        result_parts.append(f"Район: {district}")

    result = ",\n".join(result_parts)

    return result
