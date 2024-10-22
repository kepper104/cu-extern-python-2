import unittest

from weather_model import WeatherModel


class TestCheckBadWeather(unittest.TestCase):

    def setUp(self):
        self.weather_model = WeatherModel(0, 0)

    def test_good_weather(self):
        """Test when all weather conditions are within the comfortable range."""
        self.weather_model.current_temperature = 20
        self.weather_model.current_humidity = 50
        self.weather_model.current_wind_speed = 10
        self.weather_model.current_precipitation_probability = 10

        self.assertFalse(self.weather_model.check_bad_weather())

    def test_temperature_too_low(self):
        """Test when temperature is below the minimum comfortable range."""
        self.weather_model.current_temperature = 5
        self.weather_model.current_humidity = 50
        self.weather_model.current_wind_speed = 10
        self.weather_model.current_precipitation_probability = 10

        self.assertTrue(self.weather_model.check_bad_weather())

    def test_temperature_too_high(self):
        """Test when temperature is above the maximum comfortable range."""
        self.weather_model.current_temperature = 35
        self.weather_model.current_humidity = 50
        self.weather_model.current_wind_speed = 10
        self.weather_model.current_precipitation_probability = 10

        self.assertTrue(self.weather_model.check_bad_weather())

    def test_humidity_too_low(self):
        """Test when humidity is below the minimum comfortable range."""
        self.weather_model.current_temperature = 20
        self.weather_model.current_humidity = 10
        self.weather_model.current_wind_speed = 10
        self.weather_model.current_precipitation_probability = 10

        self.assertTrue(self.weather_model.check_bad_weather())

    def test_humidity_too_high(self):
        """Test when humidity is above the maximum comfortable range."""
        self.weather_model.current_temperature = 20
        self.weather_model.current_humidity = 80
        self.weather_model.current_wind_speed = 10
        self.weather_model.current_precipitation_probability = 10

        self.assertTrue(self.weather_model.check_bad_weather())

    def test_wind_speed_too_high(self):
        """Test when wind speed exceeds the maximum comfortable range."""
        self.weather_model.current_temperature = 20
        self.weather_model.current_humidity = 50
        self.weather_model.current_wind_speed = 45
        self.weather_model.current_precipitation_probability = 10

        self.assertTrue(self.weather_model.check_bad_weather())

    def test_precipitation_probability_too_high(self):
        """Test when precipitation probability exceeds the maximum comfortable range."""
        self.weather_model.current_temperature = 20
        self.weather_model.current_humidity = 50
        self.weather_model.current_wind_speed = 10
        self.weather_model.current_precipitation_probability = 60

        self.assertTrue(self.weather_model.check_bad_weather())

    def test_multiple_bad_conditions(self):
        """Test when multiple conditions are outside the comfortable range."""
        self.weather_model.current_temperature = 5
        self.weather_model.current_humidity = 80
        self.weather_model.current_wind_speed = 50
        self.weather_model.current_precipitation_probability = 70

        self.assertTrue(self.weather_model.check_bad_weather())


if __name__ == '__main__':
    unittest.main()
