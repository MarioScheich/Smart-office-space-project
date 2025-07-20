import json
import os
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))
problem_path = os.path.join(script_dir, "problem.pddl")
with open("knowledge/knowledge_base.json", "r") as f:
    data = json.load(f)

init = []
# if  data['calendar'].get('meeting'):
#     init.append("(meeting-scheduled)")
# if  data['sensor_state'].get('motion_detected'):
#     init.append("(occupied)")
if data['co2'].get('co2_estimated_ppm', 0) > 160:
    init.append("(high-co2)")

# if data['sensor_state'].get('humidity', 0) > 50:
#     init.append("(high-humidity)")

# if data['sensor_state'].get('temperature', 1000) < 10:
#     init.append("(too-cold)")
try:
    with open("knowledge/knowledge_log.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        if len(rows) >= 2:
            last = json.loads(rows[-1]["weather"])
            prev = json.loads(rows[-2]["weather"])
            if last != prev:
                init.append("(forecast-bad)")
except Exception as e:
    print("⚠️ Could not compare weather from CSV:", e)

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
