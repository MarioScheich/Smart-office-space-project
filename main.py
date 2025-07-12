import time
from api_clients.update import update_knowledge_base
from api_clients.weatherbit import fetch_weather
from api_clients.openmeteo import fetch_openmeteo_co2
from api_clients.google_calendar import fetch_calendar
from messaging.publish_all_data import publish_all_data
from sensors.dht_sensor import read_dht_sensor


# === Fetch and publish everything ===
def main():
    print("Starting data collection...")
    # Read from DHT sensor
    dht_data = read_dht_sensor()    
    weather = fetch_weather()
    co2 = fetch_openmeteo_co2()
    calendar = fetch_calendar()
    update_knowledge_base(weather, co2, calendar, dht_data)
    publish_all_data(dht_data, weather, co2, calendar)
    print("All data published.")
if __name__ == "__main__":
    main()
