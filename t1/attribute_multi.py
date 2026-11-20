#!/usr/bin/env python3
"""Attribute multi-r residuals to construction modules; dump them."""
import os
import json, gzip, collections

BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    res = json.load(f)
cm = json.load(open(f"{BASE}/construction-map.json"))
insts = cm["instantiations"]

R_VARS = set([119] + list(range(137, 173)))

def support(r):
    s = set()
    for coeff, mon in r:
        s.update(mon)
    return s

# attribute each residual index to module path
attr = {}
for it in sorted(insts, key=lambda x: x["first_residual"], reverse=True):
    for i in range(it["first_residual"], it["first_residual"] + it["residual_count"]):
        attr[i] = it["path"] + ":" + it["module"]

# all residuals with >=2 r-vars, grouped by module
groups = collections.defaultdict(list)
for i, r in enumerate(res):
    s = support(r) & R_VARS
    if len(s) >= 2:
        groups[attr[i]].append((i, sorted(s)))

print("=== multi-r residuals by module ===")
for mod, lst in sorted(groups.items()):
    print(f"{mod}: {len(lst)} residuals")
    for i, s in lst[:6]:
        print(f"   resid {i}: r-vars {s}")
    if len(lst) > 6:
        print(f"   ... +{len(lst)-6} more")

# dump one representative from each interesting group
print("\n=== residual contents ===")
seen = set()
for i, r in enumerate(res):
    s = support(r) & R_VARS
    if len(s) >= 2:
        mod = attr[i]
        key = (mod, tuple(sorted(s)))
        if key in seen:
            continue
        seen.add(key)
        print(f"resid {i} @ {mod}, r-vars {sorted(s)}:")
        print("   " + json.dumps(r)[:400])
