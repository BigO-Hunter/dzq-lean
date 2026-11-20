#!/usr/bin/env python3
"""Control arms for the ordered elimination + rank of the original system."""
import json, gzip, collections, time
P = (1 << 61) - 1

def rank(rows, label):
    t0 = time.time()
    coldeg = collections.Counter()
    for r in rows:
        for m in r:
            coldeg[m] += 1
    order = sorted(coldeg, key=lambda m: (coldeg[m], m))
    colid = {m: i for i, m in enumerate(order)}
    piv = {}
    dep = 0
    for idx, r in enumerate(rows):
        cur = {colid[m]: c % P for m, c in r.items()}
        became = False
        while cur:
            col = min(cur)
            if col in piv:
                pv = piv[col]
                f = cur.pop(col)
                for c2, v2 in pv.items():
                    nc = (cur.get(c2, 0) - f * v2) % P
                    if nc:
                        cur[c2] = nc
                    elif c2 in cur:
                        del cur[c2]
            else:
                piv[col] = dict(cur)
                became = True
                break
        if not became:
            dep += 1
    print(f"{label}: rows {len(rows)} rank {len(piv)} dep {dep}  [{time.time()-t0:.1f}s]", flush=True)

orig = [ {tuple(sorted(m)): c for c, m in row}
         for row in json.load(gzip.open("/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973/residuals.json.gz")) ]
rank(orig, "original")
dup = orig + [dict(orig[0])]
rank(dup, "control dup-row (expect dep=1)")
half = orig + [{m: 2 * c for m, c in orig[5].items()}]
rank(half, "control 2x-row (expect dep=1)")
combo_row = {}
for m in set(orig[0]) | set(orig[1]):
    c = orig[0].get(m, 0) + orig[1].get(m, 0)
    if c:
        combo_row[m] = c
rank(orig + [combo_row], "control r0+r1 combo (expect dep=1)")
print("DONE", flush=True)
