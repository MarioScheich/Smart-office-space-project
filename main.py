import subprocess
import os
from api_clients.update import update_knowledge_base
from api_clients.weatherbit import fetch_weather
from api_clients.openmeteo import fetch_openmeteo_co2
from api_clients.google_calendar import fetch_calendar
from messaging.subscriber import start_subscriber

import json

# === Global combined sensor data holder ===
sensor_state = {}

from messaging.publisher import publish_message  # Ensure this is available on Mac too

def handle_environment_data(ch, method, body):
    global sensor_state
    try:
        print("Handling environment data:", body.decode())
        sensor_state = json.loads(body.decode())

        if sensor_state.get("motion_detected"):
            print("Motion is detected")
        else:
            print("No motion detected")

        humidity = sensor_state.get("humidity")
        print("Humidity:", humidity)

        # Publish alert if humidity > 50
        if humidity is not None and humidity > 50:
            print("High humidity detected! Sending alert to RPI.")
            publish_message("sensor.alert", {"alert": "high_humidity_alert"})

        print("Temperature:", sensor_state.get("temperature"))
        print("Buzzer activated:", sensor_state.get("buzzer_activated"))

        update_knowledge()
        print("Knowledge base updated with latest sensor data.")
        run_ai_planning()
        print("AI planning executed successfully.")
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
def run_ai_planning():
    print("🔄 Generating problem file...")
    os.system("python ai_planning/generate_problem.py")

    print("🧠 Running Fast Downward planner...")
    subprocess.run(["bash", "ai_planning/run_planner.sh"], check=False)

    print("⚙️ Executing plan...")
    os.system("python ai_planning/plan_executor.py")

def main():
    print("Starting environment data collection...")
    start_subscriber("sensor.environment", handle_environment_data)
    

if __name__ == "__main__":
    main()
