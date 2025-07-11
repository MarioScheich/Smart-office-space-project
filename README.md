# Smart Office Space Project

## Overview

An intelligent building management system designed to improve comfort, energy efficiency, security, and productivity in modern office environments. It uses sensor data and API integrations to automate lighting, air quality, security alerts, and meeting logistics.

---

## Features

### Monitoring

- **Environmental:** Tracks humidity and CO2 levels for air quality and comfort.
- **Occupancy Detection:** Uses PIR sensors to identify room usage.
- **Security:** Detects unusual activities by combining motion sensor data with calendar schedules.

### Automation

- **Lighting & Window Shutters:** Adjusted automatically using environmental sensor data.
- **Smart Device Control:** Controls lights, fans, projectors, and computers based on occupancy and meetings.
- **Meeting Management:** Integrates with Google Calendar API to manage schedules and generate Meet links.
- **Notifications:** Alerts employees on excessive screen time and informs security of anomalies.
- **Conference Room Automation:** Shuts down PCs after meetings.

---

## Folder Structure

```
project/
├── main.py                     # Entry point of the application
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
├── sensors/
│   └── dht_sensor.py           # Humidity and temperature sensor interface
├── api_clients/
│   ├── weatherbit.py           # External weather API client
│   ├── openmeteo.py            # Another weather API client
│   ├── google_calendar.py      # Google Calendar API integration
│   └── update.py               # Updates sensor or calendar data
├── messaging/
│   └── publisher.py            # Notification and alert system
└── utils/
    └── logger.py              # Logging utilities
```

---

## Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/MarioScheich/Smart-office-space-project.git
cd Smart-office-space-project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root directory with necessary API keys and settings:

```
GOOGLE_API_KEY=your_key
WEATHERBIT_API_KEY=your_key
OPENMETEO_API_KEY=your_key
NOTIFICATION_EMAIL=your_email@example.com
```

### 4. Run the main application

```bash
python main.py
```

---

## Future Enhancements

- Predictive HVAC control with analytics.
- Integration with Microsoft Teams, Slack, etc.
- AI-based optimization for energy and security.

---

## Contributors

- *Aashik Muringathery Shoby*
- *Aishwarya Krishnamurthy Rao*
- *Mario Scheich*

---


