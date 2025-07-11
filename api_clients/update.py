import time
import json
import datetime

from api_clients.weatherbit import fetch_weather
from api_clients.openmeteo import fetch_openmeteo_co2
from api_clients.google_calendar import fetch_calendar
from utils.logger import log_to_csv

def update_knowledge_base():
    print(f"\n⏳ Fetching data at {time.ctime()}")

    timestamp = time.time()
    timestamp_human = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    weather = fetch_weather()
    co2 = fetch_openmeteo_co2()
    calendar = fetch_calendar()

    knowledge = {
        "timestamp": timestamp,
        "timestamp_human": timestamp_human,
        "weather": weather,
        "co2": co2,
        "calendar": calendar
    }

    with open("knowledge_base.json", "w") as f:
        json.dump(knowledge, f, indent=4)
        print("✅ knowledge_base.json updated")

    log_to_csv(knowledge)
    print("📈 Appended to knowledge_log.csv")
