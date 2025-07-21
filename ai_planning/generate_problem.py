import json
import os
import csv
from dotenv import load_dotenv
script_dir = os.path.dirname(os.path.abspath(__file__))
problem_path = os.path.join(script_dir, "problem.pddl")

with open("knowledge/knowledge_base.json", "r") as f:
    data = json.load(f)
load_dotenv()

is_test_str = os.getenv("IS_TEST", "False")  # Default to "False" if not set
is_test = is_test_str.lower() in ("true", "1", "yes")
init = []
goal = []
#TEST 
if is_test:
    humidity = 35
    humidity_threshold = 40
    temperature = 22
    temperature_threshold = 20
    co2_ppm={
            "carbon_monoxide_ugm3": 120.0,
            "co2_estimated_ppm": 135,
            "source": "Dummy"
        }
    co2_threshold = 140  
    #init.append("(rain-expected)")  
    motion_detected = False
    meeting_scheduled = True
    #init.append("(occupied)")
    print("❌Running in test mode with dummy data.")
else:   
    humidity = data.get('sensor_state', {}).get('humidity', 0)
    temperature = data.get('sensor_state', {}).get('temperature', 0)
    co2_ppm = data.get('co2', {}).get('co2_estimated_ppm', 0)
    description = data.get("weather", {}).get("description", "").lower()
    rain_keywords = ["Heavy rain", "Shower", "Thunderstorm", "Storm", "Moderate rain"]
    if any(keyword in description for keyword in rain_keywords):
        init.append("(rain-expected)")
    humidity_threshold = 40
    temperature_threshold = 20
    co2_threshold = 140

    motion_detected = data.get('sensor_state', {}).get('motion_detected', False)
    meeting_scheduled = data.get('calendar', {}).get('meeting', False)

if co2_ppm["co2_estimated_ppm"] > co2_threshold:
    print("⚠️ High CO₂ detected:", co2_ppm)
    init.append("(high-co2)")
    goal += ["(ventilated)", "(buzzer-on)"] 

if humidity > humidity_threshold:
    print("⚠️ High humidity detected:", humidity)
    init.append("(high-humidity)")
    goal.append("(ventilated)")
if temperature < temperature_threshold:
    print("⚠️ Low temperature detected:", temperature)
    init.append("(too-cold)")
    init.append("(window-opened)")
    goal.append("(not (window-opened))")

if motion_detected:
    print("⚠️ Motion detected")
    init.append("(occupied)")
    goal.append("(light-on)")

if meeting_scheduled:
    print("⚠️ Meeting scheduled")
    init.append("(meeting-scheduled)")
    goal.append("(send-meeting-scheduled)")


# Weather Change via CSV Comparison
try:
    with open("knowledge/knowledge_log.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        if len(rows) >= 2:
            last = json.loads(rows[-1]["weather"])
            prev = json.loads(rows[-2]["weather"])
            if last != prev:
                init.append("(forecast-bad)")
                goal.append("(email-sent)")  
except Exception as e:
    print("⚠️ Could not compare weather from CSV:", e)
#to remove duplicates from goal    
goal = list(dict.fromkeys(goal))
print("✅ init state:", init)
print("✅ goal state:", goal)

init_block = "\n    ".join(init)
if goal:
    goal_block = "(and " + " ".join(set(goal)) + ")"
else:
    # fallback so planner doesn't crash
    goal_block = "(and (light-on))"

problem_content = f"""(define (problem smart-building-situation)
  (:domain smart-office)

  (:init
    {init_block}
  )

  (:goal
    {goal_block}
  )
)"""

with open(problem_path, "w") as f:
    f.write(problem_content)

