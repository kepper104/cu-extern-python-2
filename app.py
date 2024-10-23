from flask import Flask, render_template, request, jsonify

from models.geocoder_model import get_coordinates_of_city
from models.weather_model import WeatherModel, ping_weather_api, ping_internet

most_populous_cities_with_coordinates = {
    "Москва": (55.7558, 37.6172),
    "Санкт Петербург": (59.9342, 30.3350),
    "Новосибирск": (55.0500, 82.9500),
    "Екатеринбург": (56.8356, 60.6128),
    "Казань": (55.7964, 49.1089),
    "Нижний Новгород": (56.3294, 43.3917),
    "Челябинск": (55.1547, 61.3758),
    "Омск": (54.9833, 73.3667),
    "Самара": (53.2028, 50.1408),
    "Ростов": (47.2225, 39.7100),
    "Другая локация": (0.0, 0.0),
}

app = Flask(__name__)


@app.route('/get_city_coordinates')
def get_city_coordinates():
    """
    Get coordinates of a city by its name.
    :return: coordinates of the city
    """

    city_name = request.args.get('city_name')
    coordinates = get_coordinates_of_city(city_name)
    return jsonify(coordinates)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main page of the application.
    :return:
    """

    internet_ping_successful = ping_internet()

    if not internet_ping_successful:
        return "Похоже, что вы не подключены к Интернету"

    weather_api_ping_successful = ping_weather_api()

    if not weather_api_ping_successful:
        return "Похоже, что не удалось подключиться к API погодного сервиса. Попробуйте позже."

    if request.method == "GET":
        return render_template('index.html',
                               cities=most_populous_cities_with_coordinates,
                               form_data="undefined")

    elif request.method == 'POST':
        try:
            origin_city = request.form.get('orig-city')
            origin_searched_city = request.form.get('orig-city-search-input')
            origin_latitude = request.form.get('orig-latitude')
            origin_longitude = request.form.get('orig-longitude')
            destination_city = request.form.get('dest-city')
            destination_searched_city = request.form.get('dest-city-search-input')
            destination_latitude = request.form.get('dest-latitude')
            destination_longitude = request.form.get('dest-longitude')

        except Exception as e:
            print("Error!", e)
            return "Был сделан некорректный POST запрос. \
            Попробуйте вернуться на <a href='/'> главную страницу </a> и повторите попытку."

        return_form_data = {"origin_city": origin_city, "origin_latitude": origin_latitude,
                            "origin_longitude": origin_longitude,
                            "destination_city": destination_city, "destination_latitude": destination_latitude,
                            "destination_longitude": destination_longitude,
                            "origin_searched_city": origin_searched_city,
                            "destination_searched_city": destination_searched_city}

        try:
            weather_model_origin = WeatherModel(float(origin_latitude), float(origin_longitude))
        except Exception as e:
            print("Error!", e)
            return "Произошла ошибка при запросе данных о погоде, возможно,\
                    были переданы координаты в неверном формате: " + str(e)

        try:
            weather_model_origin.get_weather()
        except Exception as e:
            print("Error!", e)

        try:
            weather_model_destination = WeatherModel(float(destination_latitude), float(destination_longitude))
        except Exception as e:
            print("Error!", e)
            return "Произошла ошибка при запросе данных о погоде, возможно,\
                    были переданы координаты в неверном формате: " + str(e)

        try:
            weather_model_destination.get_weather()
        except Exception as e:
            print("Error!", e)

        print(weather_model_destination.error, weather_model_origin.error)

        return render_template('index.html',
                               cities=most_populous_cities_with_coordinates,
                               form_data=return_form_data,
                               destination_weather=weather_model_destination.weather_data_parsed,
                               origin_weather=weather_model_origin.weather_data_parsed,
                               origin_weather_error=weather_model_origin.error,
                               destination_weather_error=weather_model_destination.error
                               )
    else:
        return "Был сделан неизвестный запрос. \
        Попробуйте вернуться на <a href='/'> главную страницу </a> и повторите попытку."


if __name__ == '__main__':
    app.run()
