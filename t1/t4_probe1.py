#!/usr/bin/env python3
"""T4 probe step 1: locate each site's pole rows in the final residuals,
verify module-local->global mapping, build the pole-local occurrence table."""
import os
import json, gzip, collections

BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    res = json.load(f)
cm = json.load(open(f"{BASE}/construction-map.json"))
insts = cm["instantiations"]

poles = [it for it in insts if it["module"] == "q_linearnormalpole"]
print(f"pole instances: {len(poles)}")

# Expected module row shapes (local indices, free=0:r,1:theta,2:W; locals 3..12)
SHAPES = [
    [[2,[1,2]],[-3,[2]],[1,[3]]],
    [[-1,[3,3]],[1,[4]]],
    [[-1,[0,5]],[1,[7]]],
    [[-17,[0]],[51,[5,7]],[1,[6,6]],[-34,[7]]],
    [[1,[4,7]],[-17,[5]],[1,[8]]],
    [[-1,[9,9]],[1,[11]]],
    [[-1,[0,10]],[1,[12]]],
    [[-867,[8,8]],[34,[8,11]],[-17,[10,12]],[1,[11,11]]],
]

def shift(row, off):
    return [[c, [v+off for v in mon]] for c, mon in row]

verified = 0
pole_globals = []  # list of (site_path, first_local, [10 globals], [8 row indices])
for it in poles:
    fr, n = it["first_residual"], it["residual_count"]
    rows = res[fr:fr+n]
    assert len(rows) == 8, (it["path"], len(rows))
    # mapping: module local m (3..12) -> global first_local + (m-3)
    ok = all(sorted(map(json.dumps, rows)) == sorted(map(json.dumps, [shift(s, it["first_local"]-3) for s in SHAPES])) for _ in [0])
    if ok:
        verified += 1
    else:
        print("MISMATCH at", it["path"])
        for r in rows[:2]: print("  got", json.dumps(r)[:150])
        for r in SHAPES[:2]: print("  exp", json.dumps(shift(r, it["first_local"]-3))[:150])
    pole_globals.append((it["path"], it["first_local"], list(range(it["first_local"], it["first_local"]+10)), list(range(fr, fr+8))))

print(f"shape-verified pole blocks: {verified}/{len(poles)}")

# occurrence table: pole local -> residual indices (search ALL residuals)
occ = collections.defaultdict(list)
pset = set()
for _, _, g10, _ in pole_globals:
    pset.update(g10)
for i, row in enumerate(res):
    s = set()
    for c, mon in row:
        s.update(mon)
    for v in s & pset:
        occ[v].append(i)

print(f"\ndistinct pole locals seen in residuals: {len(occ)} (of {len(pset)})")
cnt = collections.Counter(len(v) for v in occ.values())
print("occurrence-count histogram (num residuals containing the local):", dict(sorted(cnt.items())))

# linear-in-v occurrences: coefficient of [v] alone
def lin_coeff(row, v):
    for c, mon in row:
        if mon == [v]:
            return c
    return None

single_lin = []
for v in sorted(pset):
    rows_here = occ.get(v, [])
    if len(rows_here) == 1:
        c = lin_coeff(res[rows_here[0]], v)
        single_lin.append((v, rows_here[0], c))
print(f"\nsingle-occurrence pole locals: {len(single_lin)}")
by_c = collections.Counter(c for _, _, c in single_lin)
print("their linear coefficients:", dict(by_c))

# Do pole locals leak outside their own site's 8 pole rows?
leak = {}
for path, fl, g10, ridx in pole_globals:
    outside = set()
    for v in g10:
        for i in occ.get(v, []):
            if i not in ridx:
                outside.add(i)
    if outside:
        leak[path] = sorted(outside)
print(f"\nsites whose pole locals appear outside their own 8 pole rows: {len(leak)}")
for k, v in list(leak.items())[:5]:
    print("  ", k, "->", v[:6])

json.dump({"pole_blocks": [[p, fl, g10, ridx] for p, fl, g10, ridx in pole_globals],
           "occ": {str(k): v for k, v in occ.items()}},
          open(os.path.join(os.path.dirname(__file__), "/pole_occ.json"), "w"))
print("\nsaved pole_occ.json")
