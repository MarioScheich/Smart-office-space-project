import json
import os
from utils.email_sender import send_email

KB_PATH = "knowledge/knowledge_base.json"
FLAG_PATH = "utils/last_sent.json"

def notify_meeting_start():
    # Read knowledge base
    try:
        with open(KB_PATH, "r") as f:
            kb = json.load(f)
    except:
        print("❌ Could not read knowledge_base.json")
        return

    meeting = kb.get("calendar", {}).get("meeting", False)
    meeting_id = kb.get("calendar", {}).get("start_time")  # Use timestamp as ID
    organizer = kb.get("calendar", {}).get("organizer", "")
    attendees = kb.get("calendar", {}).get("attendees", [])
    weather = kb.get("weather", {})
    sensor_temp = kb.get("sensor_state", {}).get("temperature", "N/A")
    city = weather.get("city", "your city")
    forecast = weather.get("description", "N/A")
    city_temp = weather.get("temperature", "N/A")

    if not meeting:
        return  # No meeting now

    # Load last sent
    last_sent_id = ""
    if os.path.exists(FLAG_PATH):
        with open(FLAG_PATH, "r") as f:
            last_sent_id = json.load(f).get("last_meeting_id", "")

    if meeting_id == last_sent_id:
        return  # Email already sent for this meeting

    # Compose and send
    subject = f"📅 Meeting Started at {meeting_id}"
    message = f"""Hello,

A meeting has started.

🗓️ Organizer: {organizer}
🌡️ Current DHT sensor temperature: {sensor_temp}°C
🌇 Forecast at {city}: {forecast}, {city_temp}°C

Regards,
Smart Office Bot
"""
    recipients = [organizer] + attendees
    send_email(subject, message, recipients)

    # Save this meeting ID
    with open(FLAG_PATH, "w") as f:
        json.dump({"last_meeting_id": meeting_id}, f)

    print("✅ Meeting start email sent.")

