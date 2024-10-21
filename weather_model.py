import requests

class WeatherModel:
    def __init__(self, lat: float, lon: float,
                 min_comfortable_temperature: float = 10, max_comfortable_temperature: float = 30,
                 min_comfortable_humidity: float = 30, max_comfortable_humidity: float = 70,
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

        self.weather_data = None
        self.error = None


    def get_weather(self):
        # Make a request to the Open-Meteo API
        base_url = "https://api.open-meteo.com/v1/forecast"
        request_query = f'?latitude={self.lat}&longitude={self.lon}&current=temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m'
        response = requests.get(base_url + request_query)

        if response.status_code == 200:
            self.weather_data = response.json()
            self.store_current_weather(self.weather_data)
        else:
            self.error = 'Could not retrieve data'


    def store_current_weather(self, weather_data) -> None:
        self.current_temperature = weather_data['current']['temperature_2m']
        self.current_humidity = weather_data['current']['relative_humidity_2m']
        self.current_wind_speed = weather_data['current']['wind_speed_10m']
        self.current_precipitation_probability = weather_data['current']['precipitation_probability']


    def print_weather_data(self) -> None:
        print(f"Current temperature: {self.current_temperature} °C")
        print(f"Current humidity: {self.current_humidity} %")
        print(f"Current wind speed: {self.current_wind_speed} m/s")
        print(f"Current precipitation probability: {self.current_precipitation_probability} %")

    def check_bad_weather(self) -> bool:
        if (self.current_temperature < self.min_comfortable_temperature or
                self.current_temperature > self.max_comfortable_temperature or
                self.current_humidity < self.min_comfortable_humidity or
                self.current_humidity > self.max_comfortable_humidity or
                self.current_wind_speed > self.max_wind_speed or
                self.current_precipitation_probability > self.max_precipitation_probability):

            return True
        return False


def main():
    weather_model = WeatherModel(55.768740, 37.588835)
    weather_model.get_weather()
    weather_model.print_weather_data()
    weather_model.current_humidity = 100
    print("Weather is shit:", weather_model.check_bad_weather())



if __name__ == '__main__':
    main()