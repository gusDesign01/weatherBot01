from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from google_maps import GetMaps
from database import db, WeatherData
from dataExtract import GetWeather
from datetime import datetime, timedelta
from config.config import OPENWEATHER_API_KEY, GOOGLE_MAPS_API_KEY
from sqlalchemy import distinct
from sqlalchemy.sql import func
import requests
import json


class WeatherBot:
	def __init__(self, openweather_api_key, google_maps_api_key):
		self.maps = GetMaps(google_maps_api_key)
		self.weather_data = GetWeather(openweather_api_key)
		self.chatbot = ChatBot('WeatherBot')
		self.trainer = ChatterBotCorpusTrainer(self.chatbot)
		self.trainer.train('chatterbot.corpus.english.greetings', 'chatterbot.corpus.english.conversation')


	def get_weather(self, city):

		current_time = datetime.now()
		end_time = current_time + timedelta(days=5)

		weather_data = WeatherData.query.filter_by(city=city).filter(WeatherData.dt_txt >= current_time.strftime('%Y-%m-%d %H:%M:%S'), WeatherData.dt_txt <= end_time.strftime('%Y-%m-%d %H:%M:%S')).all()

		print(f"Information for {city}")
		for data in weather_data:
			print(f"Temperature: {data.temperature}")
			print(f"Description: {data.description}")
			print(f"Timestamp: {data.dt_txt}")
			print()

		if weather_data:
			lines = [f"Weather forecast for the next 5 days in {city}:"]

			for data in weather_data:
				timestamp = data.dt_txt
				if timestamp:
					temperature = data.temperature
					description = data.description

					formatted_timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
					formatted_timestamp = formatted_timestamp.strftime('%A %dth of %B')

					line = f"{formatted_timestamp}: {description}, Temperature: {temperature} degrees Celsius"
					lines.append(line)
				else:
					lines.append("No timestamp available")

			if len(lines) > 1:
				return lines

			return f"No weather data found for {city}"

	def get_map(self, city):
		location_data = self.maps.get_geolocation(city)
		print(city)

		if location_data:
			latitude = location_data['latitude']
			longitude = location_data['longitude']
			map_url = self.maps.display_map(latitude, longitude)
			if map_url:
				return map_url
				print(f"Get Map URL: {map_url}")
			else:
				print("Error occurred while retrieving map")
		else:
			print(f"No geolocation found for {city}")

	def extract_city_from_input(self, user_input):
		city = None

		for city_name in self.weather_data.city_dict.values():
			if city_name.lower() in user_input.lower():
				city = city_name
				break

		if city is None:
			# Generate small talk response
			response = self.chatbot.get_response(user_input)
			return str(response)

		return city

	def chatbotTrain(self):
		self.trainer = ChatterBotCorpusTrainer(self.chatbot)
		self.trainer.train('chatterbot.corpus.english.greetings', 'chatterbot.corpus.english.conversation')

	def process_input(self, user_input):

		city = self.extract_city_from_input(user_input)

		if city is None:
			print(f"No city extracted form input: {city}")
			return None

		if city:
			print(f"Finding weather info for: {city}")
			weather_response = self.get_weather(city)
			map_response = self.get_map(city)

			return f"{weather_response}\n{map_response}"

		return "Sorry, I couldn't determine the location from your input"


chatbot = WeatherBot(OPENWEATHER_API_KEY, GOOGLE_MAPS_API_KEY)

# user_input = input("Enter your request:...")
# response = chatbot.process_input(user_input)
# print(response)











