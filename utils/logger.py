import csv
import os

def log_to_csv(data, filename="knowledge/knowledge_log.csv"):
    headers = [
        "timestamp_utc",
        "DHT_temperature",
        "DHT_Humidity",
        "PIR_Motion_state",
        "temperature",
        "humidity",
        "weather_desc",
        "co2_ppm",
        "meeting"

    ]

    row = [
        data["timestamp_human"],
        data["sensor_state"].get("temperature", ""),
        data["sensor_state"].get("humidity", ""),
        data["sensor_state"].get("motion_detected", ""),
        data["weather"].get("temperature", ""),
        data["weather"].get("humidity", ""),
        data["weather"].get("description", ""),
        data["co2"].get("co2_estimated_ppm", ""),
        data["calendar"].get("meeting", ""),

    ]

    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(row)
