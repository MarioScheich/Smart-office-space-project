import requests
import datetime
from config.settings import LAT, LON
use_api=False
def fetch_openmeteo_co2():
    if not use_api:
        # Return dummy data
        return {
            "carbon_monoxide_ugm3": 120.0,
            "co2_estimated_ppm": 150,
            "source": "Dummy"
        }

    try:
        url = (
            "https://air-quality-api.open-meteo.com/v1/air-quality?"
            "latitude={}&longitude={}&hourly=carbon_monoxide".format(LAT, LON)
        )
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError if status is 4xx or 5xx
        data = response.json()

        current_hour = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:00')
        timestamps = data['hourly']['time']

        if current_hour not in timestamps:
            raise ValueError(f"No data for current hour: {current_hour}")

        index = timestamps.index(current_hour)

        co_ugm3 = data['hourly']['carbon_monoxide'][index]
        co2_ppm = round(co_ugm3 / 1.145, 2)

        return {
            "carbon_monoxide_ugm3": co_ugm3,
            "co2_estimated_ppm": co2_ppm,
            "source": "Open-Meteo"
        }
    except Exception as e:
        return {"error": str(e), "source": "Open-Meteo"}

