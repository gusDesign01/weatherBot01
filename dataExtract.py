import csv
import json

import aiohttp
import asyncio
import urllib.parse
import pandas as pd
from config.config import OPENWEATHER_API_KEY
from sqlalchemy import create_engine


class GetWeather:
	def __init__(self, api_key):
		self.api_key = api_key
		self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

		self.city_dict = {
			"Corfe Castle": "Corfe Castle",
			"The Cotswolds": "The Cotswolds",
			"Cambridge": "Cambridge",
			"Bristol": "Bristol",
			"Oxford": "Oxford",
			"Norwich": "Norwich",
			"Stonehenge": "Stonehenge",
			"Watergate Bay": "Watergate Bay",
			"Birmingham": "Birmingham"
		}

	async def get_weather(self, city):
		# Encode the city name for URL compatability
		encoded_city = urllib.parse.quote(city)
		# Construct the API url with the encoded city name and API key
		endpoint = f"{self.base_url}?q={encoded_city}&appid={self.api_key}"
		print(f"Fetching weather data for {city}...")
		print(f"Endpoint: {endpoint}")
		# Create an asynchronous HTTP client session using aiohttp
		async with aiohttp.ClientSession() as session:
			# Send an HTTP Get request to the API url
			async with session.get(endpoint) as response:
				try:
					# Attempt to parse the response as JSON data
					data = await response.json()
					# Extract the 'list' field from the response data, which contains all the weather data
					weather_list = data.get('list', [])

					# If the 'list' field returns empty return a dummy response
					if not weather_list:
						return [{'cod': '404'}]

					return weather_list
				except KeyError:
					print(f"Error retrieving weather data for {city}. Response: {data}")
					return []

	async def process_weather(self):
		async with aiohttp.ClientSession() as session:
			with open('weather_data.csv', 'w', newline='') as csvfile:
				# Define the fieldnames for the CSV file
				fieldnames = ['city', 'data']
				# Create a csv writer
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				# Write the CSV header row
				writer.writeheader()

				# Create a list to store the asynchronous tasks
				tasks = []
				# Iterate over the cities in city_dict
				for city in self.city_dict.values():
					# Create an asynchronous task to retrieve weather data
					task = asyncio.ensure_future(self.get_weather(city))
					# Add the task to the tasks list
					tasks.append(task)

				# Gather the results of all tasks
				weather_data_list = await asyncio.gather(*tasks)

				# Create a set to keep track of processed cities
				processed_cities = set()

				# Iterate over the city_dict values and the weather sata
				for city, weather_data in zip(self.city_dict.values(), weather_data_list):

					if city not in processed_cities:
						processed_cities.add(city)

						print(weather_data)

						# Check if the weather data in not empty and doesn't indicate error
						if weather_data and 'cod' not in weather_data[0]:
							city_info = city
							data = {'city': city, 'data':[]}

							existing_data = next((d for d in weather_data_list if d[0].get('city') == city_info), None)
							if existing_data:
								data = existing_data[0]

							weather_data_by_date = {}

							# Iterate over the weather data entries
							for entry in weather_data:
								# Extract the date from the dt_txt field
								date = entry['dt_txt'].split()[0]
								# Store the weather entry in the weather_data_by_date dict
								if date not in weather_data_by_date:
									weather_data_by_date[date] = entry

								# Check if the entry matches 12:00
								if entry['dt_txt'].split()[1] == '12:00:00':
									# Create a weather_entry dictionary with selected fields
									weather_entry = {
										'dt': entry['dt'],
										'main': entry['main'],
										'weather': entry['weather'],
										'clouds': entry['clouds'],
										'wind': entry['wind'],
										'visibility': entry['visibility'],
										'pop': entry['pop'],
										'sys': entry['sys'],
										'dt_txt': entry['dt_txt']
									}
									# Append the weather_entry to the data dictionary
									data['data'].append(weather_entry)

						# Convert the data dictionary to JSON data
						weather_data_json = json.dumps(data)

						writer.writerow({'city': city, 'data': weather_data_json})

						print(f"Data written for {city}")

	def import_csv_as_dataframe(self, csv_file):
		df = pd.read_csv(csv_file)
		print("CSV file imported into DataFrame")
		return df

	# def import_csv_to_sql(self, csv_file, table_name, db_uri):
	# 	df = pd.read_csv(csv_file)
	#
	# 	try:
	# 		engine = create_engine(db_uri)
	# 		engine.connect()
	# 		df.to_sql(table_name, engine, if_exists='replace', index= False)
	# 		print("Data exported to SQL database successfully")
	# 	except Exception as e:
	# 		print("Error exporting data to SQL database:", str(e))


# Create an instance of GetWeather
weather_fetcher = GetWeather(OPENWEATHER_API_KEY)

# Run the process_weather method
asyncio.run(weather_fetcher.process_weather())

df = weather_fetcher.import_csv_as_dataframe("weather_data.csv")

print("Dataframe table: ", df)

# csv_file = "weather_data.csv"
# table_name = 'weather_table'
# db_uri = 'sqlite:///weather.db'
#
# weather_fetcher.import_csv_to_sql(csv_file, table_name, db_uri)



