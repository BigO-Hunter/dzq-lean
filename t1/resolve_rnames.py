#!/usr/bin/env python3
"""Resolve the 37 conic r-variables to Z_definition log names."""
import json

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
m = json.load(open(f"{BASE}/source/modules/Z_definition.json"))
log = m["construction_log"]
FIRST_LOCAL = 27

names = {}
for e in log:
    if e[0] == "variable":
        names[e[1]] = e[2]

rvars = [119] + list(range(137, 173))
print("conic r-variable -> Z_definition log name:")
for g in rvars:
    loc = g - FIRST_LOCAL
    print(f"  global {g} (local {loc}): {names.get(loc, '???')}")

# also the sites' own locals referenced: e.g. 278, 291-294 (r_error?)
extra = [278, 279, 291, 292, 293, 294]
print("\nextra vars in multi-r residuals:")
for g in extra:
    loc = g - FIRST_LOCAL
    print(f"  global {g} (local {loc}): {names.get(loc, '???')}")
