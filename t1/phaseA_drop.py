#!/usr/bin/env python3
"""Phase A: projection-preserving drop sweep.

Rule (PROVED per op): variable v occurs in exactly one row R and R is linear
in v (coeff c != 0). Drop R and v. Any other variable whose ONLY occurrence
was R becomes unconstrained and leaves the system. Both directions of the iff:
  - full solution restricts to reduced solution (trivial);
  - reduced solution extends: v := -rest/c (rational), freed vars arbitrary.
Consistent with the release's "rational zero projection exactly Z".
"""
import os
import json, gzip, collections

BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
OUT = os.path.dirname(__file__)
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(mon): c for c, mon in row} for row in rows_raw ]

cm = json.load(open(f"{BASE}/construction-map.json"))
poles = [it for it in cm["instantiations"] if it["module"] == "q_linearnormalpole"]
pole_locals = set()
for it in poles:
    pole_locals.update(range(it["first_local"], it["first_local"] + 10))

# occurrence table
occ = collections.defaultdict(list)      # var -> [row idx]
lin = collections.defaultdict(list)      # var -> [(row idx, coeff)]
for i, r in enumerate(rows):
    for m, c in r.items():
        if len(m) == 1:
            occ[m[0]].append(i)
            lin[m[0]].append((i, c))
        else:
            for v in m:
                occ[v].append(i)

INPUT = 0
assert len(occ[INPUT]) > 1, "input must not be droppable"

dropped_rows = set()
dropped_vars = set()
ops = []
candidates = [v for v in sorted(occ) if len(occ[v]) == 1 and v != INPUT
              and any(ri == occ[v][0] and c != 0 for ri, c in lin[v])]
print(f"initial drop candidates: {len(candidates)}")
for v in candidates:
    if v in dropped_vars:
        continue
    R = occ[v][0]
    if R in dropped_rows:
        continue
    c = next((c for ri, c in lin[v] if ri == R), 0)
    if c == 0:
        continue
    # execute drop
    involved = set()
    for m in rows[R]:
        involved.update(m)
    dropped_rows.add(R)
    dropped_vars.add(v)
    freed = [u for u in sorted(involved) if u != v and all(ri == R for ri in occ[u])]
    dropped_vars.update(freed)
    ops.append({"row": R, "pivot": v, "coeff": c, "freed": freed,
                "row_content": rows_raw[R]})
    # keep occ coherent for remaining candidates (rows don't change; occ only matters
    # for vars not yet processed; their occ lists still point at dropped rows -> guarded above)

print(f"ops: {len(ops)}, rows dropped: {len(dropped_rows)}, vars dropped: {len(dropped_vars)}")
pole_rows_dropped = sum(1 for o in ops if set().union(*[set(m) for m in o["row_content"]]) & pole_locals)
pole_vars_dropped = sorted(dropped_vars & pole_locals)
print(f"ops whose row touches a pole local: {pole_rows_dropped}")
print(f"pole locals among dropped vars: {len(pole_vars_dropped)} -> {pole_vars_dropped[:20]}")

surv_rows = [r for i, r in enumerate(rows) if i not in dropped_rows]
surv_vars = sorted(set(occ) - dropped_vars)
print(f"surviving rows: {len(surv_rows)}, surviving vars: {len(surv_vars)} (min {surv_vars[0]}, max {surv_vars[-1]})")

# re-index compactly: old -> new
remap = {v: i for i, v in enumerate(surv_vars)}
new_rows = [ [ [c, [remap[v] for v in sorted(m)]] for m, c in sorted(r.items()) ] for r in surv_rows ]

json.dump({
    "ops": ops,
    "dropped_rows": sorted(dropped_rows),
    "dropped_vars": sorted(dropped_vars),
    "pole_vars_dropped": pole_vars_dropped,
    "surv_vars": surv_vars,
}, open(f"{OUT}/phaseA_ops.json", "w"))
with gzip.open(f"{OUT}/variantA_residuals.json.gz", "wt") as f:
    json.dump(new_rows, f, separators=(",", ":"))
print("saved phaseA_ops.json + variantA_residuals.json.gz")
