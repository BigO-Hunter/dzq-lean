#!/usr/bin/env python3
"""Ordered sparse elimination probe on the swept variant (variantB).
Column order: ascending initial column degree (static min-degree approximation).
Reports rank + dependent rows with multiplier vectors; then exact-Q lifts.
Writes ordered_deps.json."""
import json, gzip, sys, collections, time
from fractions import Fraction

sys.set_int_max_str_digits(200000)
OUT = "/Users/dmitri.arkhipov/bigo-campaign/dzq-t1"
P = (1 << 61) - 1

rows = [ {tuple(sorted(m)): c for c, m in row} for row in json.load(gzip.open(f"{OUT}/variantB_residuals.json.gz")) ]
print(f"rows: {len(rows)}", flush=True)
t0 = time.time()

coldeg = collections.Counter()
for r in rows:
    for m in r:
        coldeg[m] += 1
order = sorted(coldeg, key=lambda m: (coldeg[m], m))
colid = {m: i for i, m in enumerate(order)}

vecs = []
for r in rows:
    d = {}
    for m, c in r.items():
        d[colid[m]] = c % P
    vecs.append(d)

piv = {}
dep = []
for idx, vec in enumerate(vecs):
    cur = dict(vec)
    mult = {idx: 1}
    became_pivot = False
    while cur:
        col = min(cur)
        if col in piv:
            pv, pm, _ = piv[col]
            f = cur.pop(col)
            for c2, v2 in pv.items():
                nc = (cur.get(c2, 0) - f * v2) % P
                if nc: cur[c2] = nc
                elif c2 in cur: del cur[c2]
            for r2, m2 in pm.items():
                nm = (mult.get(r2, 0) - f * m2) % P
                if nm: mult[r2] = nm
                elif r2 in mult: del mult[r2]
        else:
            piv[col] = (dict(cur), dict(mult), idx)
            became_pivot = True
            break
    if not became_pivot and vec:
        dep.append((idx, mult))
    if (idx + 1) % 500 == 0:
        print(f"  {idx+1}/{len(vecs)} rows, pivots {len(piv)}, deps {len(dep)}  [{time.time()-t0:.0f}s]", flush=True)

print(f"rank {len(piv)}, dependent {len(dep)}  [{time.time()-t0:.0f}s]", flush=True)
json.dump({"dep": [(i, {str(k): v for k, v in m.items()}) for i, m in dep]},
          open(f"{OUT}/ordered_deps.json", "w"))
print("saved ordered_deps.json", flush=True)
