import json
import os
from datetime import datetime, timezone
from utils.email_sender import send_email

KB_PATH = "knowledge/knowledge_base.json"
FLAG_PATH = "utils/last_sent.json"

def notify_meeting_start():
    # Load knowledge base
    try:
        with open(KB_PATH, "r") as f:
            kb = json.load(f)
            print("✅ Knowledge base loaded successfully.")
    except:
        print("❌ Could not read knowledge_base.json")
        return

    events = kb.get("calendar", {}).get("events", [])
    if not events:
        print("ℹ️ No upcoming meetings.")
        return

    now_utc = datetime.now(timezone.utc)

    # Find meetings within the next 2 days
    upcoming_meetings = []
    for event in events:
        start_str = event.get("start")
        if not start_str:
            continue
        try:
            start_time = datetime.fromisoformat(start_str)
        except ValueError:
            print(f"⚠️ Invalid date format: {start_str}")
            continue

        delta = start_time - now_utc
        if 0 <= delta.total_seconds() <= 2 * 24 * 3600:
            upcoming_meetings.append((start_time, event))

    if not upcoming_meetings:
        print("ℹ️ No meetings scheduled in the next 2 days.")
        return

    # Pick the earliest upcoming meeting
    upcoming_meetings.sort(key=lambda x: x[0])
    next_meeting = upcoming_meetings[0][1]

    meeting_id = next_meeting["start"]
    organizer = next_meeting.get("creator_email", "")
    attendees = next_meeting.get("attendees", [])

    # Check if email already sent for this meeting
    last_sent_id = ""
    if os.path.exists(FLAG_PATH):
        with open(FLAG_PATH, "r") as f:
            last_sent_id = json.load(f).get("last_meeting_id", "")

    if meeting_id == last_sent_id:
        print("ℹ️ Email already sent for this meeting.")
        return

    # Gather sensor and weather data
    weather = kb.get("weather", {})
    sensor_temp = kb.get("sensor_state", {}).get("temperature", "N/A")
    city = weather.get("city", "your city")
    forecast = weather.get("description", "N/A")
    city_temp = weather.get("temperature", "N/A")

    # Compose and send the email
    subject = f"📅 Meeting Started: {next_meeting.get('summary', 'No Title')}"
    message = f"""Hello,

A meeting has been scheduled.

🗓️ Summary: {next_meeting.get('summary')}
👤 Organizer: {organizer}
🕒 Start Time: {meeting_id}
🌡️ Sensor Temperature: {sensor_temp}°C
🌇 Weather Forecast: {forecast}, {city_temp}°C

Regards,  
Smart Office Bot
"""
    recipients = [organizer] + attendees
    send_email(subject, message, recipients)

    # Save last sent meeting ID
    with open(FLAG_PATH, "w") as f:
        json.dump({"last_meeting_id": meeting_id}, f)

    print("✅ Meeting notification email sent.")
