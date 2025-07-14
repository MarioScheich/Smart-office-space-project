import requests
import datetime
from config.settings import LAT, LON

def fetch_openmeteo_co2():
    try:
        url = (
            "https://air-quality-api.open-meteo.com/v1/air-quality?"
            "latitude={}&longitude={}&hourly=carbon_monoxide".format(LAT, LON)
        )
        response = requests.get(url)
        data = response.json()

        current_hour = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:00')
        timestamps = data['hourly']['time']
        index = timestamps.index(current_hour)

        co_ugm3 = data['hourly']['carbon_monoxide'][index]
        co2_ppm = round(co_ugm3 / 1.145, 2)

        return {
            "carbon_monoxide_ugm3": co_ugm3,
            "co2_estimated_ppm": co2_ppm,
            "source": "Open-Meteo"
        }
    except Exception as e:
        return {"error": str(e)}
