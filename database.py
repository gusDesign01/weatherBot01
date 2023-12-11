import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_database.db'
db = SQLAlchemy(app)


# Define the WeatherData model
class WeatherData(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(100))
	description = db.Column(db.String(200))
	temperature = db.Column(db.Float)
	dt_txt = db.Column(db.String(100))


# Delete existing data from the WeatherData table
db.session.query(WeatherData).delete()
db.session.commit()


# # Load weather data into DataFrame
# df = pd.read_csv("weather_data.csv")

# Read weather data from the CSV file
with open('weather_data.csv', 'r') as file:
	reader = csv.DictReader(file)

	# Create a set to store unique data
	unique_data = set()

	for row in reader:
		city = row['city']
		data = row['data']
		print(data)

		# Check if the data is already processed
		if data in unique_data:
			continue

		unique_data.add(data)

		decode_data = json.loads(data)
		print(decode_data)

		# Process the weather data
		if 'data' in decode_data and len(decode_data['data']) > 0:
			for entry in decode_data['data']:
				temp = entry['main']['temp']
				description = entry['weather'][0]['description']
				timestamp = entry['dt_txt']

				# Create a WeatherData object and add to the session
				weather = WeatherData(city=city, temperature=temp, description=description, dt_txt=timestamp)

				db.session.add(weather)

			else:
				print(f"No weather data found for {city}")

	# Commit the changes to the database
	db.session.commit()

	# Retrieve and print the committed weather data
	committed_weather_data = WeatherData.query.all()

	for weather_data in committed_weather_data:
		print(f"City: {weather_data.city}")
		print(f"Temperature: {weather_data.temperature}")
		print(f"Description: {weather_data.description}")
		print(f"Timestamp: {weather_data.dt_txt}")
		print()



