#!/usr/bin/env python3
"""Per-site pole analysis in FINAL space: rows touching pole locals, their
shapes, linear-in-v candidates, and cross-consumption."""
import os
import json, gzip, collections

BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    res = json.load(f)
cm = json.load(open(f"{BASE}/construction-map.json"))
insts = cm["instantiations"]
poles = [it for it in insts if it["module"] == "q_linearnormalpole"]

def support(row):
    s = set()
    for c, mon in row:
        s.update(mon)
    return s

row_support = [support(r) for r in res]
row_has = [dict() for _ in res]  # not needed; compute linear coeff on demand
def lin_coeff(row, v):
    for c, mon in row:
        if mon == [v]:
            return c
    return 0

report = {}
all_touch = set()
for it in poles:
    g10 = list(range(it["first_local"], it["first_local"] + 10))
    s = set(g10)
    rows_t = [i for i, sup in enumerate(row_support) if sup & s]
    all_touch.update(rows_t)
    report[it["path"]] = {
        "locals": g10,
        "rows": rows_t,
        "n_rows": len(rows_t),
    }
print("rows touching pole locals per site: histogram",
      dict(collections.Counter(d["n_rows"] for d in report.values())))
tot = sum(d["n_rows"] for d in report.values())
print("total distinct rows touching pole locals:", len(all_touch), "(sum per-site:", tot, ")")

# Dump the smallest site in full detail
site = min(report, key=lambda k: report[k]["n_rows"])
d = report[site]
print(f"\n=== site {site}: locals {d['locals']}")
L = set(d["locals"])
for i in d["rows"]:
    row = res[i]
    print(f" row {i}: " + "  ".join(f"{c}[{'*'.join('x'+str(v) for v in mon) or '1'}]" for c, mon in row)[:250])
print("\nlinear-in analysis for this site's locals:")
for v in d["locals"]:
    rows_v = [i for i in d["rows"] if v in row_support[i]]
    lins = [(i, lin_coeff(res[i], v)) for i in rows_v]
    lin_rows = [(i, c) for i, c in lins if c != 0]
    print(f"  x{v}: in {len(rows_v)} rows; linear in {lin_rows}")

json.dump(report, open(os.path.join(os.path.dirname(__file__), "/site_pole_rows.json"), "w"))
