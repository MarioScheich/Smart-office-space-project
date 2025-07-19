import json
import os
# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build full path for problem.pddl in the same folder
problem_path = os.path.join(script_dir, "problem.pddl")
with open("knowledge/knowledge_base.json", "r") as f:
    data = json.load(f)

init = []

# Check for calendar meeting
if  data['calendar'].get('meeting'):
    init.append("(meeting-scheduled)")

# Check for motion (from sensor_state)
if  data['sensor_state'].get('motion_detected'):
    init.append("(occupied)")

# Check for high CO2 level (use estimated ppm)
if data['co2'].get('co2_estimated_ppm', 0) > 100:
    init.append("(high-co2)")

# Check for high humidity (from sensor_state)
if data['sensor_state'].get('humidity', 0) > 50:
    init.append("(high-humidity)")

# Check for cold temperature (from sensor_state)
if data['sensor_state'].get('temperature', 1000) < 10:
    init.append("(too-cold)")

# Since weather has an error, skip checking bad forecast

goal = "(and (ventilated) (alert-sent) (email-sent))"

init_block = "\n    ".join(init)

problem_content = f"""(define (problem smart-building-situation)
  (:domain smart-office)

  (:init
    {init_block}
  )

  (:goal
    {goal}
  )
)"""

with open(problem_path, "w") as f:
    f.write(problem_content)
