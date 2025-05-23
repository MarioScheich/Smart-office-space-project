# Smart Office Space Project


## Overview

This project focuses on developing an intelligent building management system to enhance comfort, energy efficiency, security, and productivity in smart buildings. The system monitors environmental conditions and occupancy, automates key building functions, and integrates with scheduling and communication tools to streamline meeting management and workplace safety.

---

## Key Features

### Monitoring

- **Environmental Monitoring:** Tracks humidity and CO2 levels inside the building to maintain air quality and comfort.
- **Occupancy Detection:** Uses PIR sensors to detect movement and occupancy in various areas.
- **Security Monitoring:** Monitors for unusual activities via PIR sensors integrated with calendar data.

### Automation

- **Lighting and Window Shutters:** Automatically controls window shutters and lights based on humidity and CO2 sensor data.
- **Meeting Management:**
  - Automates reminders for meeting timings via Calendar API.
  - Generates Google Meet links and shares them with participants.
- **Notifications and Alerts:**
  - Sends alerts to employees if they exceed allotted screen time or meeting durations.
  - Notifies building security of suspicious activity detected by sensors.
- **Smart Device Control:** Automatically switches lights, fans, projectors, cameras, and other appliances on/off based on room occupancy and meeting schedules.
- **Conference Room Automation:** Includes automatic shutdown of PCs in the conference room after meetings.

---

## Domain Components

The system focuses on automating and integrating the following core building components:

- **Lighting:** Smart control of lights based on environmental and occupancy data.
- **Heating, Ventilation, and Air Conditioning (HVAC):** Monitoring and adjusting air quality and temperature.
- **Videoconferencing:** Scheduling, meeting link generation, and room device control.
- **Appliances:** Automated control of devices such as fans, projectors, and computers.
- **Security and Alarms:** Intrusion detection and alerts for unusual activity within the building.

---

## System Architecture

The system integrates multiple sensors, APIs, and control units to monitor conditions, automate device control, and manage notifications. The interactions between environmental sensors, occupancy sensors, Calendar API, and communication modules form a comprehensive smart building ecosystem.

---

## How to Use

1. **Set up sensors** for humidity, CO2, PIR motion detection, etc., in the building.
2. **Connect the system to the building’s lighting, HVAC, and appliance control units.**
3. **Integrate with the Calendar API** for meeting schedules and reminders.
4. **Configure notification preferences** for employees and building security.
5. **Deploy the control software** to enable automated device management and alerting.

---

## Future Enhancements

- Expand automation to include advanced HVAC controls based on predictive analytics.
- Integrate with additional communication platforms beyond Google Meet.
- Implement machine learning to optimize energy usage and enhance security alerts.

---

## Contributors

- [Your Team Member Names]

---

## Contact

For questions or feedback, please contact: [Your Contact Information]
