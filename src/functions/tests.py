import unittest
from distance_calculation import calculate_distance
from city_by_google import get_location_details


class CalculateDistanceTestCase(unittest.TestCase):
    def test_distance_in_meters(self):
        geo_1 = "43.237834, 76.945856"
        geo_2 = "43.237743, 76.945665"
        expected_result = "18 м"
        distance = calculate_distance(geo_1, geo_2)
        self.assertEqual(distance, expected_result)

    def test_distance_in_kilometers(self):
        geo_1 = "43.220012, 76.931694"
        geo_2 = "43.229381, 76.944408"
        expected_result = "1.47 км"
        distance = calculate_distance(geo_1, geo_2)
        self.assertEqual(distance, expected_result)

    def test_same_coordinates(self):
        geo_1 = "43.237837, 76.945856"
        geo_2 = "43.237837, 76.945856"
        expected_result = "Обернитесь, вы рядом!"
        distance = calculate_distance(geo_1, geo_2)
        self.assertEqual(distance, expected_result)


class CityByGoogleTestCase(unittest.TestCase):
    def test_small_city_by_google(self):
        geo_point = "54.761253411009484, 38.876861215804624"
        expected_result = "Город: Зарайск,\nУлица: Ленинская улица"
        result = get_location_details(geo_point)
        self.assertEqual(result, expected_result)

    def test_big_city_by_google_1(self):
        geo_point = "55.72259527975047, 37.6772954278016"
        expected_result = 'Город: Москва,\n' \
            'Улица: 1-я Дубровская улица,\n' \
            'Район: Юго-Восточный административный округ'
        result = get_location_details(geo_point)
        self.assertEqual(result, expected_result)

    def test_other_city_by_google_2(self):
        geo_point = "39.64889641618712, -104.78507798207592"
        expected_result = 'Город: Aurora,\nУлица: East Lehigh Place'
        result = get_location_details(geo_point)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
