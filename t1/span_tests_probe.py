#!/usr/bin/env python3
"""Span-membership tests against the saved pivot basis (validates the elimination):
(a) row 0 again -> must reduce to zero (in span);
(b) 2 x row 5 -> must zero;
(c) r0 + r1 combo -> must zero;
(d) row 0 with one coefficient perturbed -> must NOT zero (negative control);
(e) 10 random sparse rows -> must NOT zero."""
import os
import json, gzip, collections, random
P = (1 << 61) - 1

orig = [ {tuple(sorted(m)): c for c, m in row}
         for row in json.load(gzip.open(os.path.join(os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973"), "/residuals.json.gz"))) ]

import time; t0 = time.time(); print("loaded", flush=True)
coldeg = collections.Counter()
for r in orig:
    for m in r:
        coldeg[m] += 1
print("coldeg", time.time()-t0, flush=True)
order = sorted(coldeg, key=lambda m: (coldeg[m], m))
colid = {m: i for i, m in enumerate(order)}

print("order done", time.time()-t0, flush=True)
piv = {}
for r in orig:
    cur = {colid[m]: c % P for m, c in r.items()}
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
            break

print("elim done", time.time()-t0, flush=True)
def in_span(row):
    cur = {colid[m]: c % P for m, c in row.items()}
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
            return False
    return True

print("a) row0 again in span:", in_span(orig[0]), "(expect True)")
print("b) 2*row5 in span:", in_span({m: 2 * c for m, c in orig[5].items()}), "(expect True)")
combo = {}
for m in set(orig[0]) | set(orig[1]):
    c = orig[0].get(m, 0) + orig[1].get(m, 0)
    if c:
        combo[m] = c
print("c) r0+r1 in span:", in_span(combo), "(expect True)")
pert = dict(orig[0])
m0 = next(iter(pert))
pert[m0] += 1
print("d) perturbed row0 in span:", in_span(pert), "(expect False)")
rng = random.Random(7)
neg = 0
for t in range(10):
    r = dict(orig[rng.randrange(len(orig))])
    mm = next(iter(r))
    r[mm] += rng.randrange(1, 97)
    if in_span(r):
        neg += 1
print(f"e) 10 perturbed rows in span: {neg} (expect 0)")
print("DONE", flush=True)
