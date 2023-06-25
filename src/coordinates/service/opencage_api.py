from opencage.geocoder import OpenCageGeocode
import os


def get_location_details(geo_point: str) -> str:
    lat, lon = geo_point.split(', ')

    geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KET"))
    results = geocoder.reverse_geocode(float(lat), float(lon), language='ru')

    if results:
        location = results[0]
        components = location['components']

        city = components.get('city', '')
        road = components.get('road', '')

        return f"Город: {city}, Улица: {road}"

    return "Местоположение не найдено"
