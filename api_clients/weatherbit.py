import requests
from config.settings import WEATHERBIT_KEY, CITY

def fetch_weather():
    try:
        url = "https://api.weatherbit.io/v2.0/current?city={}&key={}".format(CITY, WEATHERBIT_KEY)
        response = requests.get(url)
        data = response.json()
        weather_info = data['data'][0]
        return {
            "temperature": weather_info["temp"],
            "description": weather_info["weather"]["description"],
            "humidity": weather_info["rh"]
        }
    except Exception as e:
        return {"error": str(e)}
