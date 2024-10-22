import unittest

from models.geocoder_model import get_coordinates_of_city


class TestGetCoordinatesOfCity(unittest.TestCase):

    def test_valid_city(self):
        """Test that a valid city returns correct coordinates (basic test for a known city)."""
        city = "Moscow"
        coordinates = get_coordinates_of_city(city)
        self.assertIsNotNone(coordinates)
        self.assertEqual(len(coordinates), 2)
        self.assertTrue(isinstance(coordinates[0], float))
        self.assertTrue(isinstance(coordinates[1], float))

    def test_invalid_city(self):
        """Test that an invalid city name returns None."""
        city = "InvalidCityXYZ"
        coordinates = get_coordinates_of_city(city)
        self.assertIsNone(coordinates)

    def test_empty_city_name(self):
        """Test that an empty city name returns None."""
        city = ""
        coordinates = get_coordinates_of_city(city)
        self.assertIsNone(coordinates)

    def test_non_ascii_city_name(self):
        """Test that a non-ASCII city name (in Russian) returns correct coordinates."""
        city = "Москва"  # Moscow in Russian
        coordinates = get_coordinates_of_city(city)
        self.assertIsNotNone(coordinates)
        self.assertEqual(len(coordinates), 2)
        self.assertTrue(isinstance(coordinates[0], float))
        self.assertTrue(isinstance(coordinates[1], float))

    def test_city_with_special_characters(self):
        """Test that a city name with special characters returns valid coordinates."""
        city = "São Paulo"
        coordinates = get_coordinates_of_city(city)
        self.assertIsNotNone(coordinates)
        self.assertEqual(len(coordinates), 2)
        self.assertTrue(isinstance(coordinates[0], float))
        self.assertTrue(isinstance(coordinates[1], float))


if __name__ == '__main__':
    unittest.main()
