#!/usr/bin/env python3
"""Extract Z_definition construction_log entries around each site instantiation,
to see what each site's r input is named (root role vs fresh variable)."""
import json

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
m = json.load(open(f"{BASE}/source/modules/Z_definition.json"))
print("keys:", list(m.keys()))
log = m.get("construction_log", [])
print("log entries:", len(log))

# Print entries mentioning 'root' or 'call' or 'conic' or site paths
for i, e in enumerate(log):
    s = json.dumps(e)
    low = s.lower()
    if any(t in low for t in ["root", "call", "conic", "r.", "site"]):
        print(i, s[:220])
