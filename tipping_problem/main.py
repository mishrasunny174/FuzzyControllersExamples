#!/usr/bin/env python3
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# antecedents and consequent objects
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# auto membership functions for quality and service
quality.automf(3)
service.automf(3)

# manual membership functions for tip
tip["poor"] = fuzz.trimf(tip.universe, [0, 0, 13])
tip["average"] = fuzz.trimf(tip.universe, [0, 13, 25])
tip["good"] = fuzz.trimf(tip.universe, [0, 25, 25])

# creating rules
rule1 = ctrl.Rule(quality["poor"] | service["poor"], tip["poor"], "quality(poor) | service (poor) -> tip (poor)")
rule2 = ctrl.Rule(quality["average"], tip["average"], "quality(average) -> tip (poor)")
rule3 = ctrl.Rule(quality["good"] | service["good"], tip["good"], "quality(good) | service (good) -> tip (good)")

# creating control system and control system simulator
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping_sim = ctrl.ControlSystemSimulation(tipping_ctrl)

# calculating tip
tipping_sim.input["quality"] = 10
tipping_sim.input["service"] = 10
tipping_sim.compute()
print(tipping_sim.output["tip"])