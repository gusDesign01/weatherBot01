import aiohttp
import requests
import json


class GetMaps:
	def __init__(self, api_key):
		# Initialize the GetMaps class with the provided API key
		self.api_key = api_key
		self.geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'
		self.static_maps_url = 'https://maps.googleapis.com/maps/api/staticmap'

	def get_geolocation(self, location):
		# Get the geolocation data for the given location
		params = {
			'address': location,
			'key': self.api_key
		}

		print(f"Fetching geolocation data for l{location}...")
		print(f"Geocode url: {self.geocoding_url}")
		print(f"Static URL: {self.static_maps_url}")
		print(f"Parameters: {params}")

		# Sends a get request to the geocoding API
		response = requests.get(self.geocoding_url, params=params)
		print(f"Geolocation Request URL:{response.url}")
		print(f"Geolocation Response status code: {response.status_code}")
		print(f"Geolocation Response text: {response.text}")

		try:
			# Parse the data response as JSON
			data = json.loads(response.text)
		except json.JSONDecoder as e:
			print(f"Error while decoding JSON response: {e}")
			return None

		if data['status'] == 'OK' and data['results']:
			# Extract the relevant location data from the response
			result = data['results'][0]
			location_data = {
				'formatted_address': result['formatted_address'],
				'latitude': result['geometry']['location']['lat'],
				'longitude': result['geometry']['location']['lng']
			}
			return location_data
		else:
			print(f"No location data retrieved for: {location}")
			return None

	def display_map(self, latitude, longitude, zoom=12, size=(600,400)):

		# Display a map based on the provided latitude and longitude
		params = {
			'center': f'{latitude},{longitude}',
			'zoom': zoom,
			'size': f'{size[0]}x{size[1]}',
			'key': self.api_key
		}

		# Send a GET request to the static maps API
		response = requests.get(self.static_maps_url, params=params)
		print(f"Maps Request URL:{response.url}")
		print(f"Maps Response status code: {response.status_code}")

		if response.status_code == 200:
			# If the request was successful, return the map URL
			map_url = response.url
			print(f"Display Map URL: {map_url}")
			return map_url
		else:
			print('Error occurred while retrieving map')
			return None
