import unittest
from unittest.mock import patch
from coordinates.service.calculations import calculate_distance_2, distance_formatter, calculate_distance_1
from coordinates.service.google_api import get_location_details


class GetLocationDetailsTestCase(unittest.TestCase):
    @patch('coordinates.service.google_api.googlemaps.Client')
    def test_small_city_by_google(self, mock_client):
        mock_geocode_result = [
            {
                'address_components': [
                    {'long_name': 'Зарайск', 'types': ['locality']},
                    {'long_name': 'Ленинская улица', 'types': ['route']},
                ]
            }
        ]
        mock_client.return_value.reverse_geocode.return_value = mock_geocode_result
        latitude = 54.761253411009484
        longitude = 38.876861215804624
        expected_result = "Город: Зарайск,\nУлица: Ленинская улица"
        result = get_location_details(latitude, longitude)
        self.assertEqual(result, expected_result)

    @patch('coordinates.service.google_api.googlemaps.Client')
    def test_big_city_by_google_1(self, mock_client):
        mock_geocode_result = [
            {
                'address_components': [
                    {'long_name': 'Москва', 'types': ['locality']},
                    {'long_name': '1-я Дубровская улица', 'types': ['route']},
                    {'long_name': 'Юго-Восточный административный округ', 'types': ['sublocality']},
                ]
            }
        ]
        mock_client.return_value.reverse_geocode.return_value = mock_geocode_result
        latitude = 55.72259527975047
        longitude = 37.6772954278016
        expected_result = 'Город: Москва,\nУлица: 1-я Дубровская улица,\nРайон: Юго-Восточный административный округ'
        result = get_location_details(latitude, longitude)
        self.assertEqual(result, expected_result)

    @patch('coordinates.service.google_api.googlemaps.Client')
    def test_other_city_by_google_2(self, mock_client):
        mock_geocode_result = [
            {
                'address_components': [
                    {'long_name': 'Aurora', 'types': ['locality']},
                    {'long_name': 'East Lehigh Place', 'types': ['route']},
                ]
            }
        ]
        mock_client.return_value.reverse_geocode.return_value = mock_geocode_result
        latitude = 39.64889641618712
        longitude = -104.78507798207592
        expected_result = 'Город: Aurora,\nУлица: East Lehigh Place'
        result = get_location_details(latitude, longitude)
        self.assertEqual(result, expected_result)


class CalculateDistanceTestCase(unittest.TestCase):
    meters_delta: int = 100
    kilometers_delta: int = 8 * 1000

    def test_calculate_distance_2(self):
        lat = 43.237834
        lon = 76.945856
        expected_result = "Обернитесь, вы рядом!"
        distance = distance_formatter(calculate_distance_2)(lat, lon, lat, lon)
        self.assertEqual(distance, expected_result)

        lat1 = 43.237834
        lon1 = 76.945856
        lat2 = 43.237743
        lon2 = 76.945665
        expected_result = "18 м"
        distance = distance_formatter(calculate_distance_2)(lat1, lon1, lat2, lon2)
        self.assertEqual(distance, expected_result)

        lat1 = 43.237834
        lon1 = 76.945856
        lat2 = 43.237743
        lon2 = 76.945665
        distance1 = calculate_distance_2(lat1, lon1, lat2, lon2)
        distance2 = calculate_distance_2(lat2, lon2, lat1, lon1)
        self.assertEqual(distance1, distance2)

    def test_distance_in_kilometers(self):
        lat1 = 43.220012
        lon1 = 76.931694
        lat2 = 43.229381
        lon2 = 76.944408
        expected_result = "1.47 км"
        distance = distance_formatter(calculate_distance_2)(lat1, lon1, lat2, lon2)
        self.assertEqual(distance, expected_result)

    def test_distance_2_places(self):
        lat1 = 43.220012
        lon1 = 76.931694
        lat2 = 43.229381
        lon2 = 76.944408

        distance1 = calculate_distance_1(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)
        distance2 = calculate_distance_1(lat1=lat2, lat2=lat1, lon1=lon2, lon2=lon1)
        self.assertEqual(distance1, distance2)

    def test_distance_2_expect(self):
        lat1 = 43.220012
        lon1 = 76.931694
        lat2 = 43.229381
        lon2 = 76.944408
        expected_distance = 1465.102054360464
        distance = calculate_distance_1(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)
        self.assertAlmostEquals(distance, expected_distance, delta=self.meters_delta)

    def test_distance_tura_newyork(self):
        lat1 = 64.28
        lon1 = 100.22
        lat2 = 40.71
        lon2 = -74.01
        expected_distance = 8_335_000
        distance = calculate_distance_1(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)
        self.assertAlmostEquals(distance, expected_distance, delta=self.kilometers_delta)

    def test_distance_tura_sidney(self):
        lat1 = 64.28
        lon1 = 100.22
        lat2 = -33.874
        lon2 = 151.213
        expected_distance = 11_780_000
        distance = calculate_distance_1(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)
        self.assertAlmostEquals(distance, expected_distance, delta=self.kilometers_delta)
