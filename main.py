
from api_clients.update import update_knowledge_base
from api_clients.weatherbit import fetch_weather
from api_clients.openmeteo import fetch_openmeteo_co2
from api_clients.google_calendar import fetch_calendar
from messaging.subscriber import start_subscriber

def handle_dht_data(ch, method, body):
    print("Handling DHT data:", body.decode())

# === Fetch and publish everything ===
def main():
    print("Starting data collection...")  
    # dht_subscriber.py
    # Routing key should match the one used in the publisher, e.g., "sensor.dht"
    start_subscriber("sensor.dht.environment", handle_dht_data)
    # weather = fetch_weather()
    # co2 = fetch_openmeteo_co2()
    # calendar = fetch_calendar()
    # update_knowledge_base(weather, co2, calendar, dht_data)
    # print("All data published.")

if __name__ == "__main__":
    main()
