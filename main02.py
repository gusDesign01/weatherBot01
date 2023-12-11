from flask import Flask, render_template, request
from database import db
from config.config import OPENWEATHER_API_KEY, GOOGLE_MAPS_API_KEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_database.db'
db.init_app(app)

google_maps = None
weatherBot = None


@app.route('/', methods=['GET', 'POST'])
def index():
	from google_maps import GetMaps
	from weatherBot import WeatherBot

	global google_maps
	global weatherBot
	if request.method == 'POST':
		# Get user input from the form
		user_input = request.form['user_input']
		city = weatherBot.extract_city_from_input(user_input)
		# Get the weather data and map URL
		weather_data = weatherBot.get_weather(city)
		map_url = weatherBot.get_map(city)
		# Render the weatherBot.html template with the data
		return render_template('weatherBot.html', weather_data=weather_data, map_url=map_url)

	if google_maps is None:
		google_maps = GetMaps(GOOGLE_MAPS_API_KEY)

	if weatherBot is None:
		weatherBot = WeatherBot(OPENWEATHER_API_KEY, GOOGLE_MAPS_API_KEY)

	return render_template('weatherBot.html')


@app.route('/weather', methods=['POST'])
def render_weather():
	from weatherBot import WeatherBot

	user_input = request.form['user_input']
	city = weatherBot.extract_city_from_input(user_input)
	weather_data = weatherBot.get_weather(city)
	# Render the weatherBot.html template with the weather data
	return render_template('weatherBot.html', weather_data=weather_data)

@app.route('/maps', methods=['POST'])
def render_maps():
	from google_maps import GetMaps

	user_input = request.form['user_input']
	city = weatherBot.extract_city_from_input(user_input)
	map_url = weatherBot.get_map(city)

	if map_url:
		# If a map URL is retrieved, render the weatherBot.html template with the map URL
		return render_template('weatherBot.html', map_url=map_url)
	else:
		print("Error occurred while retrieving map")


if __name__ == '__main__':
	app.run()




