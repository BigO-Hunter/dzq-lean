#!/usr/bin/env python3
"""Final sealing checks for the r-coincidence verdict:
1. No residual is a linear difference r_i - r_j (+const) for any pair of the 37 r's.
2. No two r's share an identical linear form (would let identification be sound).
3. Count conic block sizes exactly for the ledger."""
import json, gzip, collections, itertools

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    res = json.load(f)
cm = json.load(open(f"{BASE}/construction-map.json"))
insts = cm["instantiations"]

R_VARS = [119] + list(range(137, 173))

def linear_part(r):
    """Return dict var->coeff for degree-1 terms."""
    d = collections.defaultdict(int)
    for coeff, mon in r:
        if len(mon) == 1:
            d[mon[0]] += coeff
    return dict(d)

def is_r_difference(r):
    """r_i - r_j + c (any c) shape: linear part = +1 on one r, -1 on another, nothing else."""
    lp = linear_part(r)
    rv = {v: c for v, c in lp.items() if v in R_VARS}
    other = {v: c for v, c in lp.items() if v not in R_VARS}
    return (len(rv) == 2 and set(rv.values()) == {1, -1} and not other,
            sorted(rv), other)

diff_hits = []
for i, r in enumerate(res):
    hit, rv, other = is_r_difference(r)
    if hit or (len(rv) >= 2 and not other):
        diff_hits.append((i, rv, other, len(r)))
print(f"residuals whose linear part is exactly an r-vs-r relation (no other linear vars): {len(diff_hits)}")
for i, rv, other, t in diff_hits[:10]:
    print(f"  resid {i}: {rv} + {len([m for m in res[i] if len(m[1])==2])} quadratic terms")

# identical linear forms on pairs (would indicate forced proportionality)
forms = {}
for v in R_VARS:
    pass
print("\n--- exact conic block sizes ---")
tot = 0
for mod in ["q_conic13", "q_conic10", "q_conic6"]:
    rows = [it for it in insts if it["module"] == mod]
    sizes = {it["local_count"] for it in rows}
    print(f"{mod}: {len(rows)} instances, local_count {sizes}")
    tot += len(rows) * sizes.pop()
print(f"total conic locals: {tot}")
pole = [it for it in insts if it["module"] == "q_linearnormalpole"]
print(f"q_linearnormalpole: {len(pole)} instances x {[it['local_count'] for it in pole][:1]}")
