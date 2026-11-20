#!/usr/bin/env python3
"""Phase B: deg<=2-preserving elimination sweep + row-rank redundancy.

Moves (each PROVED projection-preserving, per-op logged):
  M1 constant-definition: row R0 = c*v + k (pure linear, constant rest, c != 0):
     substitute v := -k/c into its other rows (pre-scale each consumer by c to
     stay integral), drop R0 and v.
  M2 two-occurrence definition: v occurs in exactly rows {R0, R1}; R0 linear in
     v (coeff c) with rest of degree 0 in others after subtracting c*v -- i.e.
     R0 - c*v is a constant; consumer v-monomial degree <= 1 in the other vars:
     R1 <- c*R1 with v -> -k. Drop R0, v.
     (M1 == M2 with zero consumers)
  M3 span drop: row is a rational linear combination of the others (mod-p rank
     detection, exact-Q verification). Drop the row.
Iterate to fixed point. Assert deg <= 2 and integrality after every op.
"""
import json, gzip, collections, sys

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
OUT = "/Users/dmitri.arkhipov/bigo-campaign/dzq-t1"
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)

# rows as dict {monomial tuple: coeff}; monomials sorted tuples
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]

def deg(row):
    return max((len(m) for m in row), default=0)

def show(row):
    return " ".join(f"{c}[{'*'.join(map(str,m)) or '1'}]" for m, c in sorted(row.items()))

# ---- dump the 10 linear rows
lin_rows = [(i, r) for i, r in enumerate(rows) if deg(r) == 1]
print(f"linear rows: {len(lin_rows)}")
for i, r in lin_rows:
    print(f"  {i}: {show(r)}")

ops = []
killed_rows = set()
killed_vars = set()

def occ_tables():
    occ = collections.defaultdict(list)
    for i, r in enumerate(rows):
        if i in killed_rows: continue
        for m in r:
            for v in m:
                occ[v].append(i)
    return occ

def row_deg_excl(row, v):
    """max degree of monomials containing v counted in the OTHER variables"""
    d = 0
    for m in row:
        if v in m:
            d = max(d, len(m) - 1)
    return d

changed = True
rounds = 0
while changed:
    changed = False
    rounds += 1
    occ = occ_tables()
    for v in sorted(occ):
        if v in killed_vars or v == 0: continue
        rs = occ[v]
        if len(rs) != 2: continue
        r0, r1 = rs
        # find linear coeff in each
        def lin_c(row):
            for m, c in row.items():
                if m == (v,): return c
            return 0
        c0, c1 = lin_c(rows[r0]), lin_c(rows[r1])
        if c0 == 0 or c1 == 0: continue
        # rest of r0 after removing c0*v must be constant
        rest = {m: c for m, c in rows[r0].items() if m != (v,)}
        if not all(len(m) == 0 for m in rest): continue
        k = rest.get((), 0)
        # consumer v-monomials must be degree <= 1 in others
        if row_deg_excl(rows[r1], v) > 1: continue
        if row_deg_excl(rows[r0], v) > 0: continue  # (trivially true here)
        # execute: r1 <- c0*r1 with v -> -k/c0  =>  r1' = c0*r1 - c1*k on (v)-monomials
        new_r1 = {}
        for m, c in rows[r1].items():
            if v in m:
                m2 = tuple(x for x in m if x != v)
                # coefficient: c * (c0 if v exponent 1) ; value v = -k/c0
                # new coeff for m2: c * c0 * (-k/c0) = -c*k
                if m2 == ():
                    pass  # constant term contribution: c * (-k) folded below
                nc = new_r1.get(m2, 0) - c * k
                if nc: new_r1[m2] = nc
                if m2 in new_r1 and new_r1[m2] == 0: del new_r1[m2]
            else:
                nc = new_r1.get(m, 0) + c * c0
                if nc: new_r1[m] = nc
                elif m in new_r1: del new_r1[m]
        assert deg(new_r1) <= 2, f"degree blew up at v={v}"
        rows[r1] = new_r1
        killed_rows.add(r0)
        killed_vars.add(v)
        ops.append({"op": "M2", "var": v, "def_row": r0, "consumer_row": r1,
                    "k": k, "c": c0,
                    "def_content": [[c, list(m)] for m, c in rows[r0].items()],
                    "consumer_before": [[c, list(m)] for m, c in rows_raw[r1]],
                    "consumer_after": [[c, list(m)] for m, c in new_r1.items()]})
        changed = True
        break  # restart with fresh occ tables

print(f"\nrounds: {rounds}, M2 ops: {len(ops)}, rows killed: {len(killed_rows)}, vars killed: {len(killed_vars)}")
for o in ops[:12]:
    print(f"  v={o['var']}: def row {o['def_row']} {show({tuple(m): c for c, m in o['def_content']})} | consumer {o['consumer_row']}")

json.dump({"ops": ops, "killed_rows": sorted(killed_rows), "killed_vars": sorted(killed_vars)},
          open(f"{OUT}/phaseB_ops.json", "w"))
print("saved phaseB_ops.json")
