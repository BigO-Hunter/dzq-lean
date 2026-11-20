#!/usr/bin/env python3
"""Parse construction-map.json: extract every instantiation, module, args.
Goal: find the conic instances (q_conic13/10/6) and what r-variable each takes."""
import os
import json, sys, collections

BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")

cm = json.load(open(f"{BASE}/construction-map.json"))
vm = json.load(open(f"{BASE}/variable-map.json"))

print("=== construction-map top-level keys:", list(cm.keys()))
insts = cm["instantiations"]
print(f"instantiations: {len(insts)}")

# Module histogram with arg counts and local counts
mods = collections.Counter()
for it in insts:
    mods[it["module"]] += 1
print("\nmodule histogram:")
for m, c in mods.most_common():
    print(f"  {m}: {c}")

# Conic instances: module, path, first argument (the r input), locals
print("\n=== conic + pole + compare instances (per contact site) ===")
conic_rows = []
for it in insts:
    if it["module"].startswith("q_conic") or it["module"] == "q_linearnormalpole" or it["module"].startswith("q_compare"):
        conic_rows.append(it)

# Print each site group: path parent
bypath = collections.defaultdict(list)
for it in conic_rows:
    parent = "/".join(it["path"].split("/")[:-1])
    bypath[parent].append(it)

def pathkey(p):
    return tuple(p.split("/"))
for parent in sorted(bypath, key=pathkey):
    rows = bypath[parent]
    site_desc = []
    for it in rows:
        args = it["arguments"]
        site_desc.append(f'{it["module"]}(first_arg={args[0]}, nargs={len(args)}, first_local={it["first_local"]}, lc={it["local_count"]})')
    print(f"{parent}: " + " | ".join(site_desc))
