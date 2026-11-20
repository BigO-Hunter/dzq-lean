#!/usr/bin/env python3
"""Close the hash loop: re-extract the term arrays emitted into LEAVES.lean and
verify each against the sha-pinned entry in F_recipe.json (and, transitively, the
source .terms.txt files)."""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXEC = os.environ.get("DZQ_EXEC", os.path.join(os.path.dirname(__file__), "dzq-exec"))
LEAVES = os.path.join(HERE, "LEAVES.lean")

recipe = json.load(open(os.path.join(EXEC, "F_recipe.json")))
objs = recipe["term_counts_measured"]["objects"]

src = open(LEAVES).read()

# Match: def <name>_T (v : Fin 12 -> Z) : Z := ( ... )
pat = re.compile(
    r"def (\w+)_T \(v : Fin 12 → ℤ\) : ℤ :=\s*\((.*?)\)\n\n",
    re.S,
)
found = {}
for m in pat.finditer(src):
    name, body = m.group(1), m.group(2)
    terms = []
    for part in body.split(" + "):
        part = part.strip()
        if not part:
            continue
        toks = part.split("*")
        coeff = int(toks[0].strip().strip("()"))
        mons = []
        for t in toks[1:]:
            t = t.strip()
            if "^" in t:
                vr, ex = t.split("^")
                mons.append((int(vr.split()[-1]), int(ex)))
            else:
                mons.append((int(t.split()[-1]), 1))
        mons.sort()
        terms.append((coeff, tuple(mons)))
    found[name] = terms

print(f"extracted {len(found)} term arrays from LEAVES.lean")
bad = 0
for name, o in sorted(objs.items()):
    if name not in found:
        print(f"MISSING in LEAVES.lean: {name}")
        bad += 1
        continue
    # canonical serialization: coeff, then var:exp pairs sorted by var
    lines = []
    for coeff, mons in sorted(found[name]):
        s = f"{coeff}"
        for var, exp in mons:
            s += f" {var}:{exp}"
        lines.append(s)
    # canonical hash over term content (not byte layout)
    canon = "\n".join(lines) + "\n"
    # compare against the canonical serialization of the SOURCE file
    src_terms = []
    for line in open(os.path.join(EXEC, o["file"])):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        coeff = int(parts[0])
        mons = tuple(sorted((int(t.split(":")[0]), int(t.split(":")[1])) for t in parts[1:]))
        src_terms.append((coeff, mons))
    src_lines = []
    for coeff, mons in sorted(src_terms):
        s = f"{coeff}"
        for var, exp in mons:
            s += f" {var}:{exp}"
        src_lines.append(s)
    if lines != src_lines:
        print(f"MISMATCH {name}: extracted != source term list")
        bad += 1
    if hashlib.sha256(open(os.path.join(EXEC, o["file"]), "rb").read()).hexdigest() != o["sha256"]:
        print(f"HASH FAIL {name} (source file vs F_recipe.json)")
        bad += 1

n = len(objs)
if bad == 0 and len(found) == n:
    print(f"HASH LOOP CLOSED: {n}/{n} leaves, extracted arrays == sha-pinned sources")
    sys.exit(0)
print(f"FAILURES: {bad}")
sys.exit(1)
