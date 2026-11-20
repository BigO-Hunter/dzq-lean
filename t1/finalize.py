#!/usr/bin/env python3
"""Finalize: expand Sum R'^2 exactly, write canonical term list + variant package.
Usage: finalize.py <residuals.json.gz> <variant_dir_name> [vars.json]
"""
import os
import json, gzip, sys, collections, hashlib, subprocess
from pathlib import Path

SRC = os.path.dirname(__file__)
res_path = sys.argv[1]
name = sys.argv[2]
vars_path = sys.argv[3] if len(sys.argv) > 3 else None

rows = json.load(gzip.open(res_path))
print(f"rows: {len(rows)}")

# expand sum of squares over Z
acc = collections.defaultdict(int)
maxrow = 0
degmax = 0
for row in rows:
    items = [(tuple(m), c) for c, m in row]
    degmax = max(degmax, max(len(m) for m, _ in items))
    for m1, c1 in items:
        for m2, c2 in items:
            mm = tuple(sorted(m1 + m2))
            acc[mm] += c1 * c2
    maxrow = max(maxrow, max(abs(c) for _, c in items))
acc = {m: c for m, c in acc.items() if c}
terms = sorted(acc.items(), key=lambda kv: kv[0])
allv = sorted({v for m in acc for v in m})
print(f"monomials: {len(acc)}, degree: {degmax}, max |Phi coeff|: {abs(max(acc.values(), key=abs)).bit_length()} bits, max |row coeff|: {maxrow.bit_length()} bits")
print(f"distinct vars in Phi: {len(allv)}, max idx: {allv[-1]}, contiguous 0..{len(allv)-1}: {allv == list(range(len(allv)))}")

outdir = Path(SRC) / name
outdir.mkdir(exist_ok=True)
# term list (canonical form)
tl = outdir / "phi_variant.canonical.txt"
with tl.open("w") as f:
    f.write("# canonical Phi variant term list: '<coeff> <var>:<exp> ...' sorted by sparse monomial key\n")
    for m, c in terms:
        f.write(f"{c} " + " ".join(f"{v}:{m.count(v)}" for v in sorted(set(m))) + "\n")
subprocess.run(["gzip", "-n", "-kf", str(tl)], check=True)
sha = hashlib.sha256(tl.read_bytes()).hexdigest()
print(f"term list: {tl} ({tl.stat().st_size} bytes); sha256 {sha}")

# variant package (residuals already compact ids; variable-map identity)
pkg = outdir / "package"
pkg.mkdir(exist_ok=True)
subprocess.run(["cp", res_path, str(pkg / "residuals.json.gz")], check=True)
n = len(rows)
(pkg / "weights.json").write_text(json.dumps([1] * n))
(pkg / "variable-map.json").write_text(json.dumps(list(range(max(allv) + 1))))
print(f"variant package at {pkg} (rows={n}, varmap identity up to {max(allv)})")
print("checker cmd: python3 ../artifact/checker.py --package " + str(pkg) + " --termlist " + str(tl) + ".gz")
