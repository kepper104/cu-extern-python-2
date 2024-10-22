import requests


def get_coordinates_of_city(city_name):
    base_url = "https://geocoding-api.open-meteo.com/v1/search"
    request_query = f'?name={city_name}&count=5&language=ru&format=json'

    try:
        response = requests.get(base_url + request_query)
        if response.status_code != 200:
            return None
        else:
            response_json = response.json()
            if response_json['results'][0]:
                lat, lon = response_json['results'][0]['latitude'], response_json['results'][0]['longitude']
                return lat, lon
            else:
                return None
    except Exception as e:
        print("Exception! Error: " + str(e))
        return None





