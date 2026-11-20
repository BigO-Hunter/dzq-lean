#!/usr/bin/env python3
"""Ordered sparse elimination v2 — REDUCE BRANCH FIXED (skip pivot lead col).
Termination invariant: pivot rows stored with their lead entry (min col);
reduction pops the lead from cur and skips c2 == col, touching only columns
ordered after col, so min(cur) strictly increases. Controls plant dependencies
that FORCE the reduce branch, so a silent never-reduces pass cannot pass.
Outputs rank + dependent-row multiplier vectors (excluded-lead convention:
mult satisfies R_d + sum_i mult[i] * R_i == 0 mod P with mult[d] = 1)."""
import os
import json, gzip, sys, collections, time

sys.set_int_max_str_digits(200000)
P = (1 << 61) - 1
OUT = os.path.dirname(__file__)

def col_order(rows):
    coldeg = collections.Counter()
    for r in rows:
        for m in r:
            coldeg[m] += 1
    order = sorted(coldeg, key=lambda m: (coldeg[m], m))
    return {m: i for i, m in enumerate(order)}

def eliminate(rows, colid, want_mults=True):
    piv = {}            # col -> (rowdict WITH lead, mult, row idx)
    deps = []           # (row idx, mult dict)
    for idx, r in enumerate(rows):
        cur = {colid[m]: c % P for m, c in r.items()}
        mult = {idx: 1} if want_mults else None
        became = False
        while cur:
            col = min(cur)
            if col in piv:
                pv, pm, _ = piv[col]
                f = cur.pop(col)                      # remove lead
                lead = pv[col]
                factor = f * pow(lead, -1, P) % P     # lead-normalized
                for c2, v2 in pv.items():
                    if c2 == col:
                        continue
                    nc = (cur.get(c2, 0) - factor * v2) % P
                    if nc:
                        cur[c2] = nc
                    elif c2 in cur:
                        del cur[c2]
                if want_mults:
                    for r2, m2 in pm.items():
                        nm = (mult.get(r2, 0) - factor * m2) % P
                        if nm:
                            mult[r2] = nm
                        elif r2 in mult:
                            del mult[r2]
            else:
                piv[col] = (dict(cur), dict(mult) if want_mults else None, idx)
                became = True
                break
        if not became and r:
            deps.append((idx, mult))
    return piv, deps

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "variant"
    if which == "variant":
        rows = [ {tuple(sorted(m)): c for c, m in row}
                 for row in json.load(gzip.open(f"{OUT}/variantB_residuals.json.gz")) ]
    else:
        rows = [ {tuple(sorted(m)): c for c, m in row}
                 for row in json.load(gzip.open(os.path.join(os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973"), "/residuals.json.gz"))) ]
    print(f"system: {which}, rows {len(rows)}", flush=True)
    t0 = time.time()
    colid = col_order(rows)
    piv, deps = eliminate(rows, colid, want_mults=(which == "variant"))
    print(f"rank {len(piv)}, dependent {len(deps)}  [{time.time()-t0:.1f}s]", flush=True)
    for i, m in deps[:10]:
        print(f"  dep row {i}: support {sorted(m)[:12]}", flush=True)
    json.dump({"which": which, "rank": len(piv),
               "deps": [(i, {str(k): v for k, v in m.items()}) for i, m in deps]},
              open(f"{OUT}/elim2_{which}.json", "w"))
    print("saved", flush=True)

if __name__ == "__main__":
    main()
