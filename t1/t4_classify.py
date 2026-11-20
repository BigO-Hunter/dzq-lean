#!/usr/bin/env python3
"""T4 probe: for each pole-block variable, classify eliminability.
Classes:
  ELIM  - would be eliminated by the bounded sweep (def row linear, all
          consumer v-monomials deg<=1 in others, coeff cap OK)
  DEG   - every candidate def row has a deg>=2 rest (substitution -> deg>2)
  CONS  - some consumer has a v-monomial of deg>=2 in others (substitution -> deg>2)
  COEFF - substitution legal but worst new coefficient > 2^64
  MULTI - v occurs in >=3 rows and none qualifies as def row (most common:
          v is linear in several rows / only in non-linear monomials)
"""
import json, gzip, collections

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
CAP = 1 << 64

def rowvars(r):
    s = set()
    for m in r: s.update(m)
    return s
def cmul(row): return tuple(sorted(row.values()))

e7 = [i for i, r in enumerate(rows) if cmul(r) == (-867, -17, 1, 34)]
pole_vars = set()
for i in e7:
    vs = rowvars(rows[i])
    pole_vars |= vs
    for j, r in enumerate(rows):
        if rowvars(r) & vs:
            pole_vars |= rowvars(r)

occ = collections.defaultdict(list)
for i, r in enumerate(rows):
    for m in r:
        for v in m:
            occ[v].append(i)

def deg(row): return max((len(m) for m in row), default=0)

cls = collections.Counter()
elim = []
for v in sorted(pole_vars):
    rs = occ.get(v, [])
    if not rs:
        cls["NOCC"] += 1
        continue
    reasons = []
    for r0 in rs:
        row0 = rows[r0]
        cv = row0.get((v,), 0)
        if cv == 0:
            continue
        rest = {m: c for m, c in row0.items() if m != (v,)}
        if any(len(m) > 1 for m in rest):
            reasons.append("DEG")
            continue
        consumers = [i for i in rs if i != r0]
        if any(len(m) - 1 > 1 for r1 in consumers for m in rows[r1] if v in m):
            reasons.append("CONS")
            continue
        # coeff simulation
        L = {m: -c for m, c in rest.items()}
        mx = 0
        for r1 in consumers:
            for m, a in rows[r1].items():
                if v in m:
                    m2 = tuple(x for x in m if x != v)
                    for n, lc in L.items():
                        mm = tuple(sorted(m2 + n))
                        base = next((c for m3, c in rows[r1].items() if m3 == mm), 0)
                        mx = max(mx, abs(base * CAP))  # placeholder; do real sim below
        # real per-consumer sim
        mx = 0
        for r1 in consumers:
            new = {}
            for m, a in rows[r1].items():
                if v in m:
                    m2 = tuple(x for x in m if x != v)
                    for n, lc in L.items():
                        mm = tuple(sorted(m2 + n))
                        nc = new.get(mm, 0) + a * lc
                        if nc: new[mm] = nc
                        elif mm in new: del new[mm]
                else:
                    nc = new.get(m, 0) + a * cv
                    if nc: new[m] = nc
                    elif m in new: del new[m]
            mx = max([mx] + [abs(c) for c in new.values()] or [0])
        if mx > CAP:
            reasons.append("COEFF")
            continue
        reasons.append("ELIM")
    if "ELIM" in reasons:
        cls["ELIM"] += 1
        elim.append(v)
    elif "DEG" in reasons:
        cls["DEG"] += 1
    elif "CONS" in reasons:
        cls["CONS"] += 1
    elif "COEFF" in reasons:
        cls["COEFF"] += 1
    else:
        cls["MULTI/NOLIN"] += 1

print(f"pole-block variables: {len(pole_vars)}")
print("eliminability classification:", dict(cls))
print("ELIM vars:", elim[:20])
