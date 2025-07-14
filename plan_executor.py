def send_email(subject, message):
    print(f"📧 Email sent: {subject} - {message}")

def control_servo(open=True):
    print("🪟 Window action:", "Open" if open else "Close")

def turn_on_led():
    print("💡 Light turned ON")

def turn_off_led():
    print("💡 Light turned OFF")

def activate_buzzer():
    print("🔔 Buzzer activated")

def execute_plan(plan_file):
    with open(plan_file, "r") as f:
        plan = f.readlines()

    for line in plan:
        action = line.strip().split(":")[-1].strip().lower()
        if "send-alert" in action:
            send_email("CO₂ Alert", "Please ventilate the room!")
        elif "open-window" in action:
            control_servo(open=True)
        elif "close-window" in action:
            control_servo(open=False)
        elif "turn-on-light" in action:
            turn_on_led()
        elif "turn-off-light" in action:
            turn_off_led()
        elif "activate-buzzer" in action:
            activate_buzzer()

# Example usage
# execute_plan("plan.txt")
