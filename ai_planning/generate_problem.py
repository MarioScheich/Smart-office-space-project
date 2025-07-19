import json

with open("knowledge_base.json", "r") as f:
    data = json.load(f)

init = []

if data['calendar']['meeting']:
    init.append("(meeting-scheduled)")
if data['motion']:
    init.append("(occupied)")
if data['co2_signal']['carbonIntensity'] > 400:
    init.append("(high-co2)")
if data['weather']['humidity'] > 80:
    init.append("(high-humidity)")
if data['weather']['temperature'] < 10:
    init.append("(too-cold)")
if data['weather']['condition'].lower() in ['rain', 'storm', 'snow']:
    init.append("(forecast-bad)")

goal = "(and (ventilated) (alert-sent) (email-sent))"

init_block = "\\n    ".join(init)

problem_content = f"""(define (problem smart-building-situation)
  (:domain smart-office)

  (:init
    {init_block}
  )

  (:goal
    {goal}
  )
)"""

with open("problem.pddl", "w") as f:
    f.write(problem_content)
