import time
from api_clients.weatherbit import fetch_weather
from api_clients.openmeteo import fetch_openmeteo_co2
from api_clients.google_calendar import fetch_calendar
#from sensors.dht_sensor import read_dht_sensor
#from messaging.publisher import publish_message

# === Fetch and publish everything ===
def main():
    print("🚀 Starting data collection...")

    # Read from DHT sensor
    # dht_data = read_dht_sensor()
    # if "error" not in dht_data:
    #     msg = f"{dht_data['timestamp']} | DHT Temp = {dht_data['temperature']}°C, Humidity = {dht_data['humidity']}%"
    #     publish_message("sensor.dht.environment", msg)

    # Fetch Weatherbit data
    weather = fetch_weather()
    if "error" not in weather:
        msg = f"Weather: {weather['temperature']}°C, {weather['description']}, Humidity: {weather['humidity']}%"
        print(msg)
        #publish_message("sensor.weatherbit.environment", msg)

    # Fetch CO2 from Open-Meteo
    co2 = fetch_openmeteo_co2()
    if "error" not in co2:
        msg = f"CO₂ ~ {co2['co2_estimated_ppm']} ppm (CO: {co2['carbon_monoxide_ugm3']} µg/m³)"
        print(msg)
        #publish_message("sensor.openmeteo.co2", msg)

    # Fetch Calendar
    calendar = fetch_calendar()
    if "events" in calendar:
        count = len(calendar["events"])
        msg = f"{count} upcoming events | Meeting now: {calendar['meeting']}"
        print(msg)
        #publish_message("google.calendar.events", msg)

    print("✅ All data published.")

if __name__ == "__main__":
    main()
