#!/usr/bin/env python3
"""Full elimination sweep (generalized M2) + cascade.

Sound per op (PROVED): v has a row R0 in which v is linear (coeff c != 0) and
every OTHER monomial of R0 has degree <= 1; every monomial containing v in
v's other rows has degree <= 1 in the non-v variables. Then v is definable:
v := -rest/c, and substituting (pre-scaling each consumer by c) keeps rows
integral and deg <= 2. Zero-set projection argument identical to the
release's own 'eliminate' certificate op. Weights stay 1 (row scaling only
changes R_i, not the zero set of Sum R_i^2).
"""
import json, gzip, collections

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
OUT = "/Users/dmitri.arkhipov/bigo-campaign/dzq-t1"
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
alive = [True] * len(rows)

def deg(row): return max((len(m) for m in row), default=0)
def show(row): return " ".join(f"{c}[{'*'.join(map(str,m)) or '1'}]" for m, c in sorted(row.items()))

def occ_table():
    occ = collections.defaultdict(list)
    for i, r in enumerate(rows):
        if not alive[i]: continue
        for m in r:
            for v in m:
                occ[v].append(i)
    return occ

def find_op(occ):
    for v in sorted(occ):
        if v == 0: continue
        rs = occ[v]
        if not rs: continue
        # pick a def row: v linear there, other monomials deg <= 1
        for r0 in rs:
            row0 = rows[r0]
            cv = row0.get((v,), 0)
            if cv == 0: continue
            rest = {m: c for m, c in row0.items() if m != (v,)}
            if any(len(m) > 1 for m in rest): continue
            # consumers: all other rows containing v; v-monomials deg<=1 in others
            ok = True
            for r1 in rs:
                if r1 == r0: continue
                for m in rows[r1]:
                    if v in m and len(m) - 1 > 1:
                        ok = False; break
                if not ok: break
            if not ok: continue
            return v, r0, cv, rest
    return None

ops = []
free_vars = set()
while True:
    occ = occ_table()
    hit = find_op(occ)
    if not hit: break
    v, r0, cv, rest = hit
    L = {m: -c for m, c in rest.items()}          # v -> L/cv, L = -rest
    consumers = [i for i in occ[v] if i != r0]
    for r1 in consumers:
        newrow = {}
        for m, a in rows[r1].items():
            if v in m:
                m2 = tuple(x for x in m if x != v)
                for n, lc in L.items():
                    mm = tuple(sorted(m2 + n))
                    newrow[mm] = newrow.get(mm, 0) - a * lc
            else:
                newrow[m] = newrow.get(m, 0) + a * cv
        newrow = {m: c for m, c in newrow.items() if c}
        assert deg(newrow) <= 2, f"deg blowup v={v} row={r1}"
        assert all(isinstance(c, int) for c in newrow.values())
        rows[r1] = newrow
    alive[r0] = False
    ops.append({"var": v, "def_row": r0, "n_consumers": len(consumers),
                "def_row_content": [[c, list(m)] for m, c in rows[r0].items()]})
    rows[r0] = {}

print(f"ops: {len(ops)}")
for o in ops[:20]:
    rr = {tuple(m): c for c, m in o["def_row_content"]}
    print(f"  v={o['var']} defrow {o['def_row']} (consumers={o['n_consumers']}): {show(rr)[:130]}")

# finalize: surviving rows and vars
surv_rows = [r for i, r in enumerate(rows) if alive[i] and r]
allv = set()
for r in surv_rows:
    for m in r: allv.update(m)
# variables that vanished (had rows, all killed): vars in 0..4972 minus allv
nv = 4973
free_vars = sorted(set(range(nv)) - allv)
print(f"\nsurviving rows: {len(surv_rows)}; variables used: {len(allv)}; vanished vars: {len(free_vars)}")
print(f"total var delta: {nv} -> {len(allv)}  (-{nv - len(allv)})")
print(f"row delta: 4552 -> {len(surv_rows)}  (-{4552 - len(surv_rows)})")

# sanity: any empty surviving row? no (filtered). degree histogram:
dh = collections.Counter(deg(r) for r in surv_rows)
print("degree histogram:", dict(sorted(dh.items())))
mx = max(abs(c) for r in surv_rows for c in r.values())
print("max |row coeff|:", mx, "(bit length", mx.bit_length(), ")")

# compact reindex
surv = sorted(allv)
remap = {v: i for i, v in enumerate(surv)}
new_rows = [[[c, [remap[x] for x in sorted(m)]] for m, c in sorted(r.items())] for r in surv_rows]
with gzip.open(f"{OUT}/variantB_residuals.json.gz", "wt") as f:
    json.dump(new_rows, f, separators=(",", ":"))
json.dump({"ops": ops, "survived_vars": surv, "vanished": free_vars},
          open(f"{OUT}/phaseC_ops.json", "w"))
print("saved variantB_residuals.json.gz + phaseC_ops.json")
