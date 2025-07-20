# utils/notify_meeting_start.py
import json
from utils.email_sender import send_email

with open("knowledge/knowledge_base.json", "r") as f:
    kb = json.load(f)

meeting = kb.get("calendar", {}).get("meeting", False)
organizer = kb.get("calendar", {}).get("organizer", "")
attendees = kb.get("calendar", {}).get("attendees", [])
weather = kb.get("weather", {})
sensor_temp = kb.get("sensor_state", {}).get("temperature", "N/A")
city = weather.get("city", "your city")
forecast = weather.get("description", "N/A")
city_temp = weather.get("temperature", "N/A")

subject = f"📅 Meeting Started at {kb['calendar'].get('start_time', 'unknown')}"
message = f"""Hello,

A meeting has started.

🗓️ Organizer: {organizer}
🌡️ Current DHT sensor temperature: {sensor_temp}°C
🌇 Forecast at {city}: {forecast}, {city_temp}°C

Regards,
Smart Office Bot
"""

if meeting:
    recipients = [organizer] + attendees
    send_email(subject, message, recipients)
