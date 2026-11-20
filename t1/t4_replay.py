#!/usr/bin/env python3
"""Replay certificate patches (provenance only), locate pole blocks in final rows.
No re-derivation: patches are the shipped row contents; we only need identity."""
import json, gzip, collections

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
with gzip.open(f"{BASE}/certificate.jsonl.gz") as f:
    events = [json.loads(l) for l in f]

rows = [ [list(t) for t in row] for row in events[0]["rows"] ]  # 4879
n_ops = 0
for ev in events[1:]:
    k = ev.get("kind")
    if k in ("weights", "final"):
        continue
    n_ops += 1
    for idx, newrow in (ev.get("patches") or []):
        rows[idx] = newrow
print(f"applied patches from {n_ops} ops; rows: {len(rows)}, empty: {sum(1 for r in rows if not r)}")

# sanity vs candidate-rows
cand = json.loads(gzip.open(f"{BASE}/candidate-rows.json.gz", "rt").read())
same = sum(1 for a, b in zip(rows, cand) if json.dumps(a) == json.dumps(b))
print(f"replay vs candidate-rows: {same}/{len(cand)} identical")

# final rows: non-empty candidates in order; final row idx -> candidate idx
final_of_cand = {}
fi = 0
for ci, r in enumerate(rows):
    if r:
        final_of_cand[ci] = fi
        fi += 1
print("final rows:", fi)

# construction map source row ownership
cm = json.load(open(f"{BASE}/construction-map.json"))
insts = cm["instantiations"]

# verify: initial rows at pole source indices match pole shapes?
SHAPES = [
    [[2,[1,2]],[-3,[2]],[1,[3]]], [[-1,[3,3]],[1,[4]]], [[-1,[0,5]],[1,[7]]],
    [[-17,[0]],[51,[5,7]],[1,[6,6]],[-34,[7]]], [[1,[4,7]],[-17,[5]],[1,[8]]],
    [[-1,[9,9]],[1,[11]]], [[-1,[0,10]],[1,[12]]],
    [[-867,[8,8]],[34,[8,11]],[-17,[10,12]],[1,[11,11]]],
]
# The initial row variables are CANDIDATE-space. Pole local final ids -> candidate ids:
active = json.load(open(f"{BASE}/variable-map.json"))
inv = {v: i for i, v in enumerate(active)}  # candidate var -> final id

def shift(row, off):
    return [[c, [v+off for v in mon]] for c, mon in row]

poles = [it for it in insts if it["module"] == "q_linearnormalpole"]
final_pole_rows = {}   # site -> list of 8 final row indices
verified_shapes = 0
for it in poles:
    fr = it["first_residual"]
    # expected final-content rows in FINAL variable space:
    exp_final = [shift(s, it["first_local"]-3) for s in SHAPES]
    cand_rows = [rows[fr+i] for i in range(8)]
    # map candidate rows to final space for comparison
    def to_final(row):
        out = []
        for c, mon in row:
            out.append([c, sorted(inv[v] for v in mon)])
        return sorted(out, key=json.dumps)
    got = sorted((to_final(r) for r in cand_rows), key=json.dumps)
    exp = sorted((sorted(r, key=json.dumps) for r in exp_final), key=json.dumps)
    ok = got == exp
    if ok:
        verified_shapes += 1
        final_pole_rows[it["path"]] = [final_of_cand[fr+i] for i in range(8)]
    else:
        print("pole row mismatch at", it["path"])
        print("  got[0]:", json.dumps(got[0])[:160])
        print("  exp[0]:", json.dumps(exp[0])[:160])

print(f"pole blocks shape-verified in final space: {verified_shapes}/37")
json.dump(final_pole_rows, open("/Users/dmitri.arkhipov/bigo-campaign/dzq-t1/final_pole_rows.json", "w"))
print("saved final_pole_rows.json")
