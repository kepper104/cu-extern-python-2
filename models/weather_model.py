import requests


def ping_internet():
    """
    Ping the internet to check if it is available.
    :return: True if the internet is available, False otherwise.
    """

    base_url = "https://1.1.1.1"
    response = requests.get(base_url)

    if response.status_code == 200:
        return True
    else:
        return False


def ping_weather_api():
    """
    Ping the weather API to check if it is available.
    :return: True if the weather API is available, False otherwise.
    """

    base_url = "https://api.open-meteo.com/v1/forecast?latitude=10&longitude=10"
    response = requests.get(base_url)
    if response.status_code == 200:
        return True
    else:
        return False


class WeatherModel:
    """
    Class for weather information retrieval and processing model.
    """

    def __init__(self, lat: float, lon: float,
                 min_comfortable_temperature: float = 8, max_comfortable_temperature: float = 30,
                 min_comfortable_humidity: float = 30, max_comfortable_humidity: float = 80,
                 max_wind_speed: float = 40, max_precipitation_probability: float = 50):

        self.lat = lat
        self.lon = lon

        self.min_comfortable_temperature = min_comfortable_temperature
        self.max_comfortable_temperature = max_comfortable_temperature
        self.min_comfortable_humidity = min_comfortable_humidity
        self.max_comfortable_humidity = max_comfortable_humidity
        self.max_wind_speed = max_wind_speed
        self.max_precipitation_probability = max_precipitation_probability

        self.current_temperature: float = 0.0
        self.current_humidity: float = 0.0
        self.current_wind_speed: float = 0.0
        self.current_precipitation_probability: float = 0.0

        self.weather_data_parsed = {}

        self.weather_data = None
        self.error = None

    def get_weather(self):
        """
        Retrieve weather information from the weather API.
        :return: None
        """
        base_url = "https://api.open-meteo.com/v1/forecast"
        request_query = f'?latitude={self.lat}&longitude={self.lon}&current=temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m'

        try:
            response = requests.get(base_url + request_query)

            if response.status_code == 200:
                self.weather_data = response.json()
                self.store_current_weather(self.weather_data)
            else:
                self.error = 'Произошла ошибка при запросе данных о погоде: ' + str(response.text)

        except Exception as e:
            print("Exception! Error: " + str(e))
            self.error = 'Произошла ошибка при запросе данных о погоде: ' + str(e)

    def store_current_weather(self, weather_data) -> None:
        """
        Store the current weather information in the model.
        :param weather_data: weather data retrieved from the weather API
        :return: None
        """

        self.current_temperature = weather_data['current']['temperature_2m']
        self.current_humidity = weather_data['current']['relative_humidity_2m']
        self.current_wind_speed = weather_data['current']['wind_speed_10m']
        self.current_precipitation_probability = weather_data['current']['precipitation_probability']

        is_bad_weather = self.check_bad_weather()

        self.weather_data_parsed = {"temperature": self.current_temperature, "humidity": self.current_humidity,
                                    "wind_speed": self.current_wind_speed,
                                    "precipitation_probability": self.current_precipitation_probability,
                                    "is_bad_weather": is_bad_weather}

    def print_weather_data(self):
        """
        Print the current weather information.
        :return: None
        """

        print(f"Current temperature: {self.current_temperature} °C")
        print(f"Current humidity: {self.current_humidity} %")
        print(f"Current wind speed: {self.current_wind_speed} m/s")
        print(f"Current precipitation probability: {self.current_precipitation_probability} %")

    def check_bad_weather(self):
        """
        Check if the current weather conditions are bad.
        :return: True if the weather conditions are bad, False otherwise.
        """

        if (self.current_temperature < self.min_comfortable_temperature or
                self.current_temperature > self.max_comfortable_temperature or
                self.current_humidity < self.min_comfortable_humidity or
                self.current_humidity > self.max_comfortable_humidity or
                self.current_wind_speed > self.max_wind_speed or
                self.current_precipitation_probability > self.max_precipitation_probability):
            return True
        return False
