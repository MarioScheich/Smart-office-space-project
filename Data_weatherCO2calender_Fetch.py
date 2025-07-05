import requests
import time
import json
import csv
import os
import datetime
import schedule

# === CONFIGURATION ===
WEATHERBIT_KEY = "2b310f3fbc524315a90c3c4227b823e2"
CITY = "Stuttgart"
LAT = 48.7758
LON = 9.1829
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# === GOOGLE CALENDAR SETUP ===
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def fetch_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append({"start": start, "summary": event.get("summary", "No title")})

    return {
        "meeting": bool(event_list),
        "events": event_list
    }

# === WEATHERBIT FETCH ===
def fetch_weather():
    try:
        url = f"https://api.weatherbit.io/v2.0/current?city={CITY}&key={WEATHERBIT_KEY}"
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

# === OPEN-METEO CO₂ FETCH ===
def fetch_openmeteo_co2():
    try:
        url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={LAT}&longitude={LON}&hourly=carbon_monoxide"
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

# === CSV LOGGER ===
def log_to_csv(data):
    log_file = "knowledge_log.csv"
    headers = [
        "timestamp_utc",
        "temperature",
        "humidity",
        "weather_desc",
        "co2_ppm",
        "meeting"
    ]

    row = [
        data["timestamp_human"],
        data["weather"].get("temperature", ""),
        data["weather"].get("humidity", ""),
        data["weather"].get("description", ""),
        data["co2"].get("co2_estimated_ppm", ""),
        data["calendar"].get("meeting", "")
    ]

    file_exists = os.path.exists(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(row)

# === MAIN UPDATE FUNCTION ===
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

# === SCHEDULER ===
schedule.every(30).minutes.do(update_knowledge_base)
update_knowledge_base()

print("⏰ Scheduler started: updates every 30 minutes")
while True:
    schedule.run_pending()
    time.sleep(1)
