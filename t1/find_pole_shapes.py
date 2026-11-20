#!/usr/bin/env python3
"""Find the pole blocks in FINAL space by their distinctive coefficient shapes.
Module shapes (module-local; coeffs are what matter):
  E0: 2*th*l - 3*th + c          -> row with coeffs {2,-3,1}, two LINEAR -3? no: -3 on theta (shared with 2*th*l)
  E3: -17*r + 51*e*c + p^2 - 34*c -> linear -17, linear -34, quad 51, square +1
  E7: -867*w^2 + 34*w*j - 17*q*k + j^2 -> coeffs {34, -17, -867}
Search final rows for coeff multisets matching each shape."""
import json, gzip, collections

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(m): c for c, m in row} for row in rows_raw ]

def cmul(row):  # coefficient multiset
    return tuple(sorted(c for c in row.values()))

E0 = (1, -3, 2)
E1 = (-1, 1)
E2 = (-1, 1)
E3 = (-34, -17, 1, 51)
E4 = (-17, 1, 1)
E5 = (-1, 1)
E6 = (-1, 1)
E7 = (-867, -17, 1, 34)

hist = collections.Counter(cmul(r) for r in rows)
for name, cmu in [("E0", E0), ("E3", E3), ("E7", E7)]:
    print(name, cmu, "final rows with this coeff multiset:", hist.get(cmu, 0))

# locate E7 rows (most distinctive)
e7_rows = [i for i, r in enumerate(rows) if cmul(r) == E7]
print("\nE7-shaped rows:", len(e7_rows), e7_rows[:10])

# locate E3 rows
e3_rows = [i for i, r in enumerate(rows) if cmul(r) == E3]
print("E3-shaped rows:", len(e3_rows), e3_rows[:10])

# E0: 1,-3,2
e0_rows = [i for i, r in enumerate(rows) if cmul(r) == E0]
print("E0-shaped rows:", len(e0_rows), e0_rows[:10])

# For a found E7 row, dump neighbors: rows sharing variables (its block)
if e7_rows:
    i = e7_rows[0]
    vs = set()
    for m in rows[i]: vs.update(m)
    near = [j for j, r in enumerate(rows) if set().union(*[set(m) for m in r]) & vs]
    print(f"\nrow {i} vars {sorted(vs)}; rows sharing vars: {near}")
    for j in near:
        print(f"  {j}: " + "  ".join(f"{c}[{'*'.join(map(str,m)) or '1'}]" for m, c in sorted(rows[j].items()))[:200])
