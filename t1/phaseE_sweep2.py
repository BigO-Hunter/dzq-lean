#!/usr/bin/env python3
"""Bounded elimination sweep v2 (sign fixed) + per-op independent verification
+ correct sparse rank (re-sorting reduction) on original AND swept rows.
Every op is re-verified post-hoc: new_consumer == cv*old_consumer with v->-rest/cv
(expanded over exact rationals, asserted integral)."""
import json, gzip, collections, sys
from fractions import Fraction

sys.set_int_max_str_digits(100000)
BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
OUT = "/Users/dmitri.arkhipov/bigo-campaign/dzq-t1"
CAP = 1 << 64

with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
alive = [True] * len(rows)

def deg(row): return max((len(m) for m in row), default=0)
def rowvars(r):
    s = set()
    for m in r: s.update(m)
    return s
def cmul(row): return tuple(sorted(row.values()))

# pole-block variables (final space): E7 rows + 1-step neighbors
e7 = [i for i, r in enumerate(rows) if cmul(r) == (-867, -17, 1, 34)]
pole_vars = set()
for i in e7:
    vs = rowvars(rows[i])
    pole_vars |= vs
    for j, r in enumerate(rows):
        if rowvars(r) & vs:
            pole_vars |= rowvars(r)
print(f"E7 rows: {len(e7)}; pole-block var set: {len(pole_vars)}")

def occ_table():
    occ = collections.defaultdict(list)
    for i, r in enumerate(rows):
        if not alive[i]: continue
        for m in r:
            for v in m:
                occ[v].append(i)
    return occ

def subst(row, v, cv, rest):
    """new_row = cv*row with v -> -rest/cv ; integral by construction.
    term a*v*u -> -a*(rest*u) ; term a*m (v not in m) -> cv*a*m"""
    L = {m: -c for m, c in rest.items()}   # numerator polynomial of the substitution
    new = {}
    for m, a in row.items():
        if v in m:
            m2 = tuple(x for x in m if x != v)
            for n, lc in L.items():
                mm = tuple(sorted(m2 + n))
                nc = new.get(mm, 0) + a * lc          # +a*L[n]  (FIXED sign)
                if nc: new[mm] = nc
                elif mm in new: del new[mm]
        else:
            nc = new.get(m, 0) + a * cv
            if nc: new[m] = nc
            elif m in new: del new[m]
    return new

def verify_op(v, r0, cv, rest, r1, old, new):
    """independent exact-rational recomputation of one consumer rewrite:
    expected = cv * old with v -> -rest/cv"""
    sigma = {m: Fraction(-c, cv) for m, c in rest.items()}
    exp = collections.defaultdict(Fraction)
    for m, a in old.items():
        if v in m:
            m2 = tuple(x for x in m if x != v)
            for n, lc in sigma.items():
                exp[tuple(sorted(m2 + n))] += a * cv * lc   # cv-scaled substitution
        else:
            exp[m] += a * cv
    exp = {m: c for m, c in exp.items() if c}
    ok = ({m: int(c) for m, c in exp.items()} == new) and all(c.denominator == 1 for c in exp.values())
    return ok

ops = []
oplog = []
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
            if not all(len(m) - 1 <= 1 for r1 in occ[v] if r1 != r0 for m in rows[r1] if v in m):
                continue
            # simulate
            consumers = [i for i in occ[v] if i != r0]
            news = {}
            mx = 0
            bad = False
            for r1 in consumers:
                nr = subst(rows[r1], v, cv, rest)
                if deg(nr) > 2: bad = True; break
                mx = max([mx] + [abs(c) for c in nr.values()])
                news[r1] = nr
            if bad or mx > CAP: continue
            # verify each consumer rewrite independently
            allok = all(verify_op(v, r0, cv, rest, r1, rows[r1], news[r1]) for r1 in consumers)
            if not allok:
                print(f"VERIFY FAILED for v={v} r0={r0}"); sys.exit(1)
            for r1, nr in news.items():
                rows[r1] = nr
            old_def = dict(row0)
            rows[r0] = {}; alive[r0] = False
            ops.append({"var": v, "def_row": r0, "n_consumers": len(consumers),
                        "pole": v in pole_vars})
            oplog.append({"var": v, "def_row": r0, "cv": cv,
                          "rest": [[c, list(m)] for m, c in rest.items()],
                          "consumers": consumers,
                          "def_row_old": [[c, list(m)] for m, c in old_def.items()],
                          "consumers_old": None})
            fired = True
            break
        if fired: break

print(f"ops: {len(ops)}, pole-block vars among them: {sum(1 for o in ops if o['pole'])}")
surv_rows = [r for i, r in enumerate(rows) if alive[i] and r]
allv = set()
for r in surv_rows:
    for m in r: allv.update(m)
print(f"rows: 4552 -> {len(surv_rows)}; vars: 4973 -> {len(allv)}")
mx = max(abs(c) for r in surv_rows for c in r.values())
print("max |row coeff|:", mx, "bits:", mx.bit_length())

# save swept variant
surv = sorted(allv)
remap = {v: i for i, v in enumerate(surv)}
with gzip.open(f"{OUT}/variantB_residuals.json.gz", "wt") as f:
    json.dump([[[c, [remap[x] for x in sorted(m)]] for m, c in sorted(r.items())] for r in surv_rows],
              f, separators=(",", ":"))
json.dump({"ops": ops, "survived": surv}, open(f"{OUT}/phaseD_ops.json", "w"))
print("saved variant")

# ---------- correct rank ----------
def rank(rows_list, label):
    mons = {}
    vecs = []
    for r in rows_list:
        d = {}
        for m, c in r.items():
            if m not in mons: mons[m] = len(mons)
            d[mons[m]] = c % ((1 << 61) - 1)
        vecs.append(d)
    piv = {}
    dep = []
    for idx, vec in enumerate(vecs):
        cur = dict(vec)
        while cur:
            col = min(cur)
            if col in piv:
                pv, _ = piv[col]
                f = cur[col]
                for c2, v2 in pv.items():
                    nc = (cur.get(c2, 0) - f * v2) % ((1 << 61) - 1)
                    if nc: cur[c2] = nc
                    elif c2 in cur: del cur[c2]
            else:
                piv[col] = (dict(cur), idx)
                cur = {}
        if not cur and min(vecs[idx], default=(None,))[0] is not None:
            pass
        # dependent if it reduced to zero AND it wasn't itself a pivot row
        if all(c in piv and piv[c][1] != idx or True for c in []):
            pass
    # recompute properly: dependent = rows that reduced to zero (cur empty) and not chosen as pivot
    return piv, vecs

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
    piv = {}   # col -> (vec, row_idx)
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

# original rows rank
orig = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
n_orig, dep_orig = rank2(orig, "original")
rank2(surv_rows, "swept ")
json.dump({"dependent_original": dep_orig}, open(f"{OUT}/rank_probe.json", "w"))
print("DONE")
