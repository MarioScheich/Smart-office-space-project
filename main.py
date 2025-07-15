from api_clients.update import update_knowledge_base
from api_clients.weatherbit import fetch_weather
from api_clients.openmeteo import fetch_openmeteo_co2
from api_clients.google_calendar import fetch_calendar
from messaging.subscriber import start_subscriber

import json

# === Global combined sensor data holder ===
sensor_state = {}

def handle_environment_data(ch, method, body):
    global sensor_state
    try:
        print("Handling environment data:", body.decode())
        sensor_state = json.loads(body.decode())

        if sensor_state.get("motion_detected"):
            print("Motion is detected")
        else:
            print("No motion detected")

        print("Temperature:", sensor_state.get("temperature"))
        print("Humidity:", sensor_state.get("humidity"))
        print("Buzzer activated:", sensor_state.get("buzzer_activated"))

        update_knowledge()
    except json.JSONDecodeError:
        print("Invalid environment data received:", body.decode())

def update_knowledge():
    if not sensor_state:
        print("Sensor state is empty, skipping update.")
        return

    print("Fetching external data sources and updating knowledge base...")
    weather = fetch_weather()
    co2 = fetch_openmeteo_co2()
    calendar = fetch_calendar()

    update_knowledge_base(weather, co2, calendar, sensor_state)
    print("Knowledge base updated.")

def main():
    print("Starting environment data collection...")
    start_subscriber("sensor.environment", handle_environment_data)

if __name__ == "__main__":
    main()
