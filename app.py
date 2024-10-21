from flask import Flask, render_template, request
import requests
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
    "Волгоград":	(48.7086,	44.5147)
}
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])

        weather_model = WeatherModel(lat, lon)
        weather_model.get_weather()

        if weather_model.error:
            return render_template('index.html', error=weather_model.error)

        bad_weather = weather_model.check_bad_weather()
        return render_template('index.html', bad_weather=bad_weather, weather_model=weather_model)

    return render_template('index.html', bad_weather=None, weather_model=None, cities=most_populous_cities_with_coordinates)

if __name__ == '__main__':
    app.run(debug=True)
