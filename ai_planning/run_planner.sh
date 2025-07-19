#!/bin/bash
python3 /Users/feyn/uni/SmartCities/Smart-office-space-project/ai_planning/downward/fast-downward.py \
  /Users/feyn/uni/SmartCities/Smart-office-space-project/ai_planning/domain.pddl \
  /Users/feyn/uni/SmartCities/Smart-office-space-project/ai_planning/problem.pddl \
  --search "lazy_greedy([ff()], preferred=[ff()])" > /Users/feyn/uni/SmartCities/Smart-office-space-project/ai_planning/plan.txt
