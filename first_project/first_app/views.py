import requests
from datetime import datetime, timedelta
import os
import json  # Ensure json module is imported
from dotenv import load_dotenv
from django.shortcuts import render

# Load environment variables from .env file
load_dotenv()
GEO_APIKEY = os.getenv("GEO_API", default="")


def get_weather_data(city_name):
    api_key = GEO_APIKEY
    city = city_name
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    print(f'Temperature in {city}: {data["main"]["temp"]}')
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    # Check if a cached file exists
    filename = f"{city_name.lower().replace(' ', '')+str(lat)+'-'+str(lon)}.txt"
    if os.path.exists(filename):
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(filename))
        if datetime.now() - file_modified_time < timedelta(minutes=180):
            with open(filename, 'r') as file:
                try:
                    return json.load(file)  # Ensure returning a dictionary
                except json.JSONDecodeError:
                    # If the cached file is corrupted or not valid JSON, delete it
                    os.remove(filename)

    # Get weather data directly using the city name
    api_key = GEO_APIKEY
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}'
    response = requests.get(url)

    if response.status_code != 200:
        return None  # Handle error if the city is not found or API fails

    data = response.json()

    # Cache the data to a file
    with open(filename, 'w') as file:
        json.dump(data, file)  # Save the weather data as a JSON file

    return data


def weather_view(request):
    weather_data = None
    if request.method == 'POST':
        city_name = request.POST['city_name']
        weather_data = get_weather_data(city_name)

        if isinstance(weather_data, dict):  # Ensure weather_data is a dictionary
            weather_data['city_name'] = city_name
        else:
            weather_data = {'error': 'City not found or data processing error'}

    return render(request, 'weather/weather.html', {'weather_data': weather_data})
