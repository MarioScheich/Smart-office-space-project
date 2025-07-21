import os
import requests
from dotenv import load_dotenv
from config.settings import WEATHERBIT_KEY, CITY
load_dotenv()
is_test_str = os.getenv("IS_API_TEST", "False")  # Default to "False" if not set
is_api_test = is_test_str.lower() in ("true", "1", "yes")
def fetch_weather():
    if is_api_test:
        print("❌Running in test mode, returning dummy weather data.")
        return {
            "temperature": 22,
            "description": "Broken clouds",
            "humidity": 145,
    }
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
