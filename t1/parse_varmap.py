#!/usr/bin/env python3
"""What are the r-variables? Map variable indices -> names/roles from variable-map.json."""
import json, collections

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
vm = json.load(open(f"{BASE}/variable-map.json"))
print("type:", type(vm).__name__, "len:", len(vm))
print("sample entries:", json.dumps(vm[:3], indent=1)[:600])
# Index by 'variable' field if present
byidx = {}
for e in vm:
    byidx[e.get("variable", e.get("index"))] = e
print("\nr-variables of the 37 sites:")
for idx in [119, 137, 138, 139, 140, 141, 150, 151, 155, 157, 163, 165, 171, 172]:
    print(f"  var {idx}: {json.dumps(byidx.get(idx))}")
# How many distinct variables total
print("\ntotal entries:", len(byidx))
