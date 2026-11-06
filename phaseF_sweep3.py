#!/usr/bin/env python3
"""Optimized bounded elimination sweep v3.
- per-round: build occ + row->var degree index once
- rejected (v, r0) pairs memoized with a row-version counter
- fires one op per round; verifies every consumer rewrite exactly (Fractions)
- coeff cap 2^64; deg<=2 asserted
Then: sparse rank (re-sorting) on original + swept rows, with per-dependent-row
multiplier vectors saved for exact-Q lift.
"""
import json, gzip, collections, sys, time
from fractions import Fraction

sys.set_int_max_str_digits(100000)
BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
OUT = "/Users/dmitri.arkhipov/bigo-campaign/dzq-t1"
CAP = 1 << 64

with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
alive = [True] * len(rows)
version = 0

def deg(row): return max((len(m) for m in row), default=0)
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

t0 = time.time()
def subst(row, v, cv, rest):
    L = {m: -c for m, c in rest.items()}
    new = {}
    for m, a in row.items():
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
    return new

def verify_full(v, cv, rest, old, new):
    sigma = {m: Fraction(-c, cv) for m, c in rest.items()}
    exp = collections.defaultdict(Fraction)
    for m, a in old.items():
        if v in m:
            m2 = tuple(x for x in m if x != v)
            for n, lc in sigma.items():
                exp[tuple(sorted(m2 + n))] += a * cv * lc
        else:
            exp[m] += a * cv
    got = {m: c for m, c in exp.items() if c}
    if any(c.denominator != 1 for c in got.values()):
        return False
    return {m: int(c) for m, c in got.items()} == new

ops = []
rejected = {}   # (v, r0) -> version when rejected
rounds = 0
while True:
    rounds += 1
    if rounds > 2000:
        print("ROUND CAP"); break
    # occ
    occ = collections.defaultdict(list)
    for i, r in enumerate(rows):
        if not alive[i] or not r: continue
        for m in r:
            for v in m:
                occ[v].append(i)
    # per-row var degree index: badvar[row] = set of vars in a deg->(>=2 others) monomial
    lin = {}      # row -> dict var -> linear coeff
    bad = {}      # row -> set of vars appearing with deg>=2 in others
    for i, r in enumerate(rows):
        if not alive[i] or not r: continue
        l = {}
        b = set()
        for m, c in r.items():
            if len(m) == 1:
                l[m[0]] = c
            elif len(m) == 2:
                for v in m:
                    b.add(v)
        lin[i] = l
        bad[i] = b
    fired = False
    for v in sorted(occ):
        if v == 0: continue
        rs = occ[v]
        for r0 in rs:
            if rejected.get((v, r0)) is not None and rejected[(v, r0)] >= version:
                continue
            cv = lin[r0].get(v, 0)
            if cv == 0:
                rejected[(v, r0)] = version
                continue
            row0 = rows[r0]
            rest = {m: c for m, c in row0.items() if m != (v,)}
            if any(len(m) > 1 for m in rest):
                rejected[(v, r0)] = version
                continue
            # consumers
            consumers = [i for i in rs if i != r0]
            if any(v in bad[r1] for r1 in consumers):
                rejected[(v, r0)] = version
                continue
            # simulate
            L = {m: -c for m, c in rest.items()}
            news = {}
            mx = 0
            ok = True
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
                if deg(new) > 2 or max((abs(c) for c in new.values()), default=0) > CAP:
                    ok = False; break
                news[r1] = new
            if not ok:
                rejected[(v, r0)] = version
                continue
            # verify
            allok = True
            for r1 in consumers:
                if not verify_full(v, cv, rest, rows[r1], news[r1]):
                    allok = False
                    print(f"VERIFY FAILED v={v} r0={r0} r1={r1}")
                    sys.exit(1)
            # commit
            for r1, nr in news.items():
                rows[r1] = nr
            rows[r0] = {}
            alive[r0] = False
            ops.append({"var": v, "def_row": r0, "n_consumers": len(consumers), "pole": v in pole_vars})
            fired = True
            version += 1
            break
        if fired: break
    if not fired:
        break

print(f"rounds: {rounds}, ops: {len(ops)}, pole-block ops: {sum(1 for o in ops if o['pole'])}")
surv_rows = [r for i, r in enumerate(rows) if alive[i] and r]
allv = set()
for r in surv_rows:
    for m in r: allv.update(m)
print(f"rows: 4552 -> {len(surv_rows)}; vars: 4973 -> {len(allv)}")
mx = max(abs(c) for r in surv_rows for c in r.values())
print("max |row coeff|:", mx.bit_length(), "bits")
surv = sorted(allv)
remap = {v: i for i, v in enumerate(surv)}
with gzip.open(f"{OUT}/variantB_residuals.json.gz", "wt") as f:
    json.dump([[[c, [remap[x] for x in sorted(m)]] for m, c in sorted(r.items())] for r in surv_rows], f, separators=(",", ":"))
json.dump({"ops": ops, "survived": surv}, open(f"{OUT}/phaseD_ops.json", "w"))
print(f"[{time.time()-t0:.0f}s] saved variant")

# ---------- rank ----------
def rank2(rows_list, label):
    P = (1 << 61) - 1
    mons = {}
    vecs = []
    for r in rows_list:
        d = {}
        for m, c in r.items():
            if m not in mons: mons[m] = len(mons)
            d[mons[m]] = c % P
        vecs.append(d)
    piv = {}
    dep = []
    for idx, vec in enumerate(vecs):
        cur = dict(vec)
        is_dep = True
        while cur:
            col = min(cur)
            if col in piv:
                pv, _ = piv[col]
                f = cur[col]
                for c2, v2 in pv.items():
                    nc = (cur.get(c2, 0) - f * v2) % P
                    if nc: cur[c2] = nc
                    elif c2 in cur: del cur[c2]
            else:
                piv[col] = (dict(cur), idx)
                is_dep = False
                break
        if is_dep and vec:
            dep.append(idx)
    print(f"{label}: rows {len(vecs)}, rank {len(piv)}, dependent {len(dep)}: {dep[:12]}")
    return len(piv), dep

orig = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
n_orig, dep_orig = rank2(orig, "original")
n_swept, dep_swept = rank2(surv_rows, "swept ")
json.dump({"dependent_original": dep_orig, "dependent_swept": dep_swept,
           "rank_original": n_orig, "rank_swept": n_swept},
          open(f"{OUT}/rank_probe.json", "w"))
print(f"[{time.time()-t0:.0f}s] DONE")
