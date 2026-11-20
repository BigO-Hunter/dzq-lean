#!/usr/bin/env python3
"""Bounded elimination sweep: only ops whose worst new coefficient stays < 2^64.
Tracks pole-block variables (final space, E7-connected) separately for T4.
Also runs mod-p rank on the swept system for span-redundancy drops."""
import os
import json, gzip, collections, sys

sys.set_int_max_str_digits(100000)
BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
OUT = os.path.dirname(__file__)
CAP = 1 << 64

with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
alive = [True] * len(rows)

# ---- final-space pole block identification: E7 rows + 1-step neighbors
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
print(f"E7 rows: {len(e7)}; pole-block variable set (final space, E7+1step): {len(pole_vars)}")

def deg(row): return max((len(m) for m in row), default=0)
def maxcoeff(): return max((abs(c) for r in rows if r and alive_row(r) for c in r.values()), default=0)

alive_rows = lambda i: alive[i]
cur_max = 0

def occ_table():
    occ = collections.defaultdict(list)
    for i, r in enumerate(rows):
        if not alive[i]: continue
        for m in r:
            for v in m:
                occ[v].append(i)
    return occ

def try_op(v, r0, cv, rest, occ):
    """simulate; return new consumer rows or None if coeff cap violated"""
    L = {m: -c for m, c in rest.items()}
    consumers = [i for i in occ[v] if i != r0]
    news = {}
    mx = 0
    for r1 in consumers:
        newrow = {}
        for m, a in rows[r1].items():
            if v in m:
                m2 = tuple(x for x in m if x != v)
                for n, lc in L.items():
                    mm = tuple(sorted(m2 + n))
                    nc = newrow.get(mm, 0) - a * lc
                    if nc: newrow[mm] = nc
                    elif mm in newrow: del newrow[mm]
            else:
                nc = newrow.get(m, 0) + a * cv
                if nc: newrow[m] = nc
                elif m in newrow: del newrow[m]
        if deg(newrow) > 2: return None
        for c in newrow.values():
            if abs(c) > mx: mx = abs(c)
        news[r1] = newrow
    if mx > CAP: return None
    return consumers, news

ops = []
while True:
    occ = occ_table()
    fired = False
    for v in sorted(occ):
        if v == 0 or not occ[v]: continue
        for r0 in occ[v]:
            row0 = rows[r0]
            cv = row0.get((v,), 0)
            if cv == 0: continue
            rest = {m: c for m, c in row0.items() if m != (v,)}
            if any(len(m) > 1 for m in rest): continue
            ok = all(len(m) - 1 <= 1 for r1 in occ[v] if r1 != r0 for m in rows[r1] if v in m)
            if not ok: continue
            res = try_op(v, r0, cv, rest, occ)
            if res is None: continue
            consumers, news = res
            for r1, nr in news.items():
                rows[r1] = nr
            rows[r0] = {}
            alive[r0] = False
            ops.append({"var": v, "def_row": r0, "n_consumers": len(consumers),
                        "def_content": [[c, list(m)] for m, c in row0.items()],
                        "pole_block_var": v in pole_vars})
            fired = True
            break
        if fired: break
    if not fired: break

print(f"\nbounded ops: {len(ops)}")
surv_rows = [r for i, r in enumerate(rows) if alive[i] and r]
allv = set()
for r in surv_rows:
    for m in r: allv.update(m)
free = sorted(set(range(4973)) - allv)
print(f"rows: 4552 -> {len(surv_rows)}; vars: 4973 -> {len(allv)} (-{4973-len(allv)}; vanished {len(free)})")
pole_killed = [o["var"] for o in ops if o["pole_block_var"]]
print(f"pole-block vars eliminated: {len(pole_killed)} {pole_killed[:10]}")
mx = max(abs(c) for r in surv_rows for c in r.values())
print("max |row coeff| after sweep:", mx, "bit_length", mx.bit_length())
for o in ops:
    rr = {tuple(m): c for c, m in o["def_content"]}
    print(f"  v={o['var']} defrow {o['def_row']} cons={o['n_consumers']}: " +
          " ".join(f"{c}[{'*'.join(map(str,m)) or '1'}]" for m, c in sorted(rr.items()))[:120])

# ---------- rank mod p on swept rows ----------
P = (1 << 61) - 1
mons = {}
def midx(m):
    if m not in mons: mons[m] = len(mons)
    return mons[m]
vecs = []
for r in surv_rows:
    d = {}
    for m, c in r.items():
        d[midx(m)] = c % P
    vecs.append(d)

pivots = {}   # col -> (vec, row_idx)
dependent = []
for idx, vec in enumerate(vecs):
    cur = dict(vec)
    for col in sorted(cur):
        if col in pivots:
            pv, _ = pivots[col]
            f = cur[col]
            for c2, v2 in pv.items():
                nc = (cur.get(c2, 0) - f * v2) % P
                if nc: cur[c2] = nc
                elif c2 in cur: del cur[c2]
            if col in cur and cur[col] == 0: del cur[col]
    if not cur:
        dependent.append(idx)
    else:
        col = min(cur)
        pivots[col] = ({c: v for c, v in cur.items()}, idx)
print(f"\nrank mod p: {len(pivots)} / {len(vecs)} rows; dependent: {len(dependent)} -> {dependent[:10]}")

json.dump({"ops": ops, "pole_vars": sorted(pole_vars), "dependent_rows": dependent,
           "surv_rows_n": len(surv_rows), "vars_n": len(allv)},
          open(f"{OUT}/phaseD_ops.json", "w"))
with gzip.open(f"{OUT}/variantB_residuals.json.gz", "wt") as f:
    json.dump([[[c, [x for x in sorted(m)]] for m, c in sorted(r.items())] for r in surv_rows],
              f, separators=(",", ":"))
json.dump(sorted(allv), open(f"{OUT}/variantB_vars.json", "w"))
print("saved variantB_residuals.json.gz + phaseD_ops.json")
