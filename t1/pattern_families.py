#!/usr/bin/env python3
"""Pattern-family analysis of the final residual system (A3 hypothesis check).
Signature = (sorted coeffs, multiset of monomial degrees). Same signature on
DIFFERENT variable sets = same shape, different constraints (NOT redundant).
Also: exact duplicate rows (same monomials+coeffs) and scalar duplicates."""
import os
import json, gzip, collections

BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]

def sig(r):
    return (tuple(sorted(r.values())), tuple(sorted(len(m) for m in r)))

fams = collections.defaultdict(list)
for i, r in enumerate(rows):
    fams[sig(r)].append(i)

sizes = collections.Counter(len(v) for v in fams.values())
print(f"rows: {len(rows)}; distinct shape-signatures: {len(fams)}")
print("family-size histogram (n rows sharing a shape):", dict(sorted(sizes.items())))
big = sorted(fams.items(), key=lambda kv: -len(kv[1]))[:8]
for s, idxs in big:
    print(f"  family size {len(idxs)}: sig coeffs {s[0][:6]}.. degs {s[1]}")

# same shape AND same variable-overlap pattern? check top family: do rows share variables?
s, idxs = big[0]
vs0 = set()
for m in rows[idxs[0]]: vs0.update(m)
overlap = 0
for j in idxs[1:]:
    vs = set()
    for m in rows[j]: vs.update(m)
    if vs & vs0: overlap += 1
print(f"top family: {len(idxs)} rows; rows sharing vars with row {idxs[0]}: {overlap}")

# exact duplicates (up to sign)
seen = {}
dups = 0
scalars = 0
for i, r in enumerate(rows):
    key = tuple(sorted((m, c) for m, c in r.items()))
    key2 = tuple(sorted((m, -c) for m, c in r.items()))
    if key in seen or key2 in seen:
        dups += 1
    seen[key] = i
# scalar duplicates: r_j = c * r_i for integer c != +-1: normalize by gcd
def norm(r):
    g = 0
    for c in r.values(): g = gcd0(g, abs(c))
    return tuple(sorted((m, c // g) for m, c in r.items())) if g else None
from math import gcd as gcd0
seen2 = {}
for i, r in enumerate(rows):
    g = 0
    for c in r.values(): g = gcd0(g, abs(c))
    if g == 0: continue
    key = tuple(sorted((m, c // g) for m, c in r.items()))
    if key in seen2 and seen2[key] != (i, g):
        scalars += 1
    else:
        seen2[key] = (i, g)
print(f"exact/sign duplicates: {dups}; scalar-multiple collisions: {scalars}")
