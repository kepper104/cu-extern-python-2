from flask import Flask, render_template, request
from weather_model import WeatherModel

most_populous_cities_with_coordinates = {
    "Москва":	(55.7558,	37.6172),
    "Санкт Петербург":	(59.9342,	30.3350),
    "Новосибирск":	(55.0500,	82.9500),
    "Екатеринбург":	(56.8356,	60.6128),
    "Казань":	(55.7964,	49.1089),
    "Нижний Новгород":	(56.3294,	43.3917),
    "Челябинск":	(55.1547,	61.3758),
    "Омск":	(54.9833,	73.3667),
    "Самара":	(53.2028,	50.1408),
    "Ростов":	(47.2225,	39.7100),
    "Уфа":	(54.7261,	55.9475),
    "Красноярск":	(56.0089,	92.8719),
    "Воронеж":	(51.6717,	39.2106),
    "Пермь":	(58.0000,	56.3167),
    "Волгоград":	(48.7086,	44.5147),
    "Другая локация":	(0.0,	0.0),
}
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)

        orig_city = request.form.get('orig-city')
        orig_latitude = request.form.get('orig-latitude')
        orig_longitude = request.form.get('orig-longitude')
        dest_city = request.form.get('dest-city')
        dest_latitude = request.form.get('dest-latitude')
        dest_longitude = request.form.get('dest-longitude')

        return_form_data = {"orig_city": orig_city, "orig_latitude": orig_latitude, "orig_longitude": orig_longitude,
                            "dest_city": dest_city, "dest_latitude": dest_latitude, "dest_longitude": dest_longitude}



        weather_model_origin = WeatherModel(float(orig_latitude), float(orig_longitude))
        try:
            weather_model_origin.get_weather()
        except Exception as e:
            print("Error!", e)


        weather_model_destination = WeatherModel(float(dest_latitude), float(dest_longitude))
        try:
            weather_model_destination.get_weather()
        except Exception as e:
            print("Error!", e)

        return render_template('index.html',
                               cities=most_populous_cities_with_coordinates,
                               form_data=return_form_data, destination_weather = weather_model_destination.weather_data_parsed, origin_weather = weather_model_origin.weather_data_parsed, origin_weather_error=weather_model_origin.error, destination_weather_error=weather_model_destination.error)

    elif request.method == "GET":
        return render_template('index.html', cities=most_populous_cities_with_coordinates, form_data="undefined")


if __name__ == '__main__':
    app.run(debug=True)
