
import os
from messaging.publisher import publish_message
from utils.notify_meeting_start import notify_meeting_start

script_dir = os.path.dirname(os.path.abspath(__file__))
plan_path = os.path.join(script_dir, "plan.txt")
  
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
    # print("\n====  Plan.txt ====\n")
    # for idx, line in enumerate(plan, start=1):
    #     clean_line = line.strip()
    #     if clean_line:
    #         print(f"{idx:>2}. {clean_line}")
    # print("\n===================\n")
    for line in plan:
        action = line.strip().split(":")[-1].strip().lower()
        if "send-alert" in action:
            beep_buzzer()
        elif "ventilated" in action:
            print("Ventilating room...")
            control_servo(open=True)
        elif "buzzer-on" in action:
            print("Executing action:", action)
            beep_buzzer()
        elif "open-window" in action:
            print("Executing action:", action)
            control_servo(open=True)
        elif "close-window" in action:
            control_servo(open=False)
        elif "turn-on-light"   in action:
            print("Executing action: LIGHT ON")
            turn_on_led()
        elif "turn-off-light" in action:
            turn_off_led()
        elif "activate-buzzer" in action:
            #activate_buzzer()
            beep_buzzer()
        elif "send-meeting-scheduled" in action:
            notify_meeting_start()
            print("📧 Email sent: ")

            