import os
import json
import time
import subprocess
from ai_planning.plan_executor import execute_plan
from api_clients.update import update_knowledge_base
from api_clients.weatherbit import fetch_weather
from api_clients.openmeteo import fetch_openmeteo_co2
from api_clients.google_calendar import fetch_calendar
from messaging.subscriber import start_subscriber

# Global state
sensor_state = {}

# Time control
last_planning_time = 0
PLANNING_INTERVAL_SECONDS = 600  # Default: 10 minutes

def handle_environment_data(ch, method, body):
    global sensor_state
    try:
        print("Handling environment data:", body.decode())
        sensor_state = json.loads(body.decode())
        print("Current sensor state:", sensor_state)
        update_knowledge()
        print("Knowledge base updated with latest sensor data.")
        maybe_run_ai_planning()
    except json.JSONDecodeError:
        print("Invalid environment data received:", body.decode())

def update_knowledge():
    if not sensor_state:
        print("Sensor state is empty, skipping update.")
        return
    print("Fetching external API and updating knowledge base...")
    weather = fetch_weather()
    co2 = fetch_openmeteo_co2()
    calendar = fetch_calendar()
    update_knowledge_base(weather, co2, calendar, sensor_state)

def maybe_run_ai_planning():
    global last_planning_time
    now = time.time()
    if now - last_planning_time >= PLANNING_INTERVAL_SECONDS:
        print(f"Running AI planning (last run was {(now - last_planning_time):.1f} seconds ago)...")
        run_ai_planning()
        last_planning_time = now
    else:
        print(f"Skipping AI planning: only {(now - last_planning_time):.1f} seconds since last run.")

def run_ai_planning():
    print("(1) Generating problem file...")
    os.system("python ai_planning/generate_problem.py")
    print("(2) Running Fast Downward planner...")
    subprocess.run(["bash", "ai_planning/run_planner.sh"], check=False)
    print("(3) Executing plan...")
    execute_plan()
    print("(*) Planning and execution completed successfully.")

def main():
    print("Starting environment data collection...")
    start_subscriber("sensor.environment", handle_environment_data)

if __name__ == "__main__":
    main()
