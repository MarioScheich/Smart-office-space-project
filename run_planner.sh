#!/bin/bash
./fast-downward.py domain.pddl problem.pddl --search "lazy_greedy([ff()], preferred=[ff()])" > plan.txt
