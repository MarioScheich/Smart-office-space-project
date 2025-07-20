
import os
from messaging.publisher import publish_message

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
plan_path = os.path.join(script_dir, "plan.txt")
def send_email(subject, message):
    print(f"📧 Email sent: {subject} - {message}")

def control_servo(open=True):
    if open:
        publish_message("sensor.servo", {"action": "open_window"})
    else:
        publish_message("sensor.servo", {"action": "close_window"})
    print("🪟 Window action:", "Open" if open else "Close")


def turn_on_led():
    publish_message("sensor.led", {"action": "turn_on"})
    print("💡 Light turned ON")

def turn_off_led():
    publish_message("sensor.led", {"action": "turn_off"})
    print("💡 Light turned OFF")

def activate_buzzer():
    publish_message("sensor.buzzer", {"action": "activate"})
    print("🔔 Buzzer activated")

def deactivate_buzzer():
    publish_message("sensor.buzzer", {"action": "deactivate"})
    print("🔔 Buzzer deactivated")

def beep_buzzer():
    publish_message("sensor.buzzer", {"action": "beep"})
    print("🔔 Buzzer beeped"
          )
def execute_plan(plan_file=plan_path):
    with open(plan_file, "r") as f:
        plan = f.readlines()

    for line in plan:
        action = line.strip().split(":")[-1].strip().lower()
        if "send-alert" in action:
            beep_buzzer()
        elif "open-window" in action:
            control_servo(open=True)
        elif "close-window" in action:
            control_servo(open=False)
        elif "turn-on-light" in action:
            turn_on_led()
        elif "turn-off-light" in action:
            turn_off_led()
        elif "activate-buzzer" in action:
            #activate_buzzer()
            beep_buzzer()
        elif "send-email-weather-update" in action:
            send_email("Weather Forecast + Temp", "Weather is bad. Please be prepared.")


