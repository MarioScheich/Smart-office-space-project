def publish_all_data(dht_data, weather, co2, calendar):
    # --- DHT Sensor Data ---
    print("DHT data fetched:", dht_data)
    if "error" not in dht_data:
        msg = (
            f"{dht_data['timestamp']} | "
            f"DHT Temp = {dht_data['temperature']}°C, "
            f"Humidity = {dht_data['humidity']}%"
        )
        publish_message("sensor.dht.environment", msg)
    else:
        print("❌ DHT sensor error:", dht_data["error"])

    # --- Weatherbit Data ---
    print("Weather data fetched:", weather)
    if "error" not in weather:
        msg = (
            f"Weather: {weather['temperature']}°C, "
            f"{weather['description']}, "
            f"Humidity: {weather['humidity']}%"
        )
        publish_message("sensor.weatherbit.environment", msg)
    else:
        print("❌ Weather error:", weather["error"])

    # --- OpenMeteo CO₂ Data ---
    print("CO₂ data fetched:", co2)
    if "error" not in co2:
        msg = (
            f"CO₂ ~ {co2['co2_estimated_ppm']} ppm "
            f"(CO: {co2['carbon_monoxide_ugm3']} µg/m³)"
        )
        publish_message("sensor.openmeteo.co2", msg)
    else:
        print("❌ CO₂ data error:", co2["error"])

    # --- Google Calendar Data ---
    print("Calendar data fetched:", calendar)
    if "events" in calendar:
        count = len(calendar["events"])
        msg = f"{count} upcoming events | Meeting now: {calendar['meeting']}"
        publish_message("google.calendar.events", msg)
    else:
        print("❌ Calendar fetch failed or returned no events.")
