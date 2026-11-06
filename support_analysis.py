#!/usr/bin/env python3
"""Support analysis: which residuals contain each r_j? Are site blocks disjoint?
Also: are r_i, r_j ever linked by a residual (appearing together)?"""
import json, gzip, collections

BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"

with gzip.open(f"{BASE}/residuals.json.gz") as f:
    res = json.load(f)
print(f"residuals: {len(res)}")
# residual format sample
print("sample residual:", json.dumps(res[0])[:200])

def support(r):
    """Variables appearing in a residual: terms are [coeff, [monomial vars...]]"""
    s = set()
    for coeff, mon in r:
        s.update(mon)
    return s

R_VARS = [119] + list(range(137, 173))  # 37 candidates
print(f"\ncandidate r-vars: {R_VARS[:5]}...{R_VARS[-3:]} (n={len(R_VARS)})")

# which residuals contain each r var
per_r = collections.defaultdict(list)
for i, r in enumerate(res):
    s = support(r)
    for v in s & set(R_VARS):
        per_r[v].append(i)

print("\nr-var -> residual count + first residual idx:")
for v in R_VARS:
    lst = per_r[v]
    print(f"  r={v}: {len(lst)} residuals, idx {lst[:6]}{'...' if len(lst)>6 else ''}")

# Do any residuals contain TWO different r vars? (direct linkage)
both = []
for i, r in enumerate(res):
    s = support(r) & set(R_VARS)
    if len(s) >= 2:
        both.append((i, sorted(s)))
print(f"\nresiduals containing >=2 distinct r-vars: {len(both)}")
for i, s in both[:10]:
    print(f"  resid {i}: {s}")

# Site disjointness: compute support union per site block from construction map
cm = json.load(open(f"{BASE}/construction-map.json"))
insts = cm["instantiations"]
print("\n=== per-site variable spans (from construction-map) ===")
sites = [it for it in insts if it["module"].startswith("q_compare")]
site_spans = {}
for it in sites:
    # locals of this site's subtree = the site + conic + pole
    span = set(range(it["first_local"], it["first_local"] + it["local_count"]))
    # find conic child + pole child by path prefix
    for it2 in insts:
        if it2["path"].startswith(it["path"] + "/") and it2["module"].startswith("q_conic"):
            span |= set(range(it2["first_local"], it2["first_local"] + it2["local_count"]))
            for it3 in insts:
                if it3["path"].startswith(it2["path"] + "/"):
                    span |= set(range(it3["first_local"], it3["first_local"] + it3["local_count"]))
    site_spans[it["path"]] = span

paths = sorted(site_spans, key=lambda p: int(p.split("/")[-1]))
overlaps = []
for a in range(len(paths)):
    for b in range(a+1, len(paths)):
        ov = site_spans[paths[a]] & site_spans[paths[b]]
        if ov:
            overlaps.append((paths[a], paths[b], sorted(ov)[:8], len(ov)))
print(f"local-span overlaps between sites: {len(overlaps)}")
for a, b, ov, n in overlaps[:8]:
    print(f"  {a} ∩ {b}: {n} vars e.g. {ov}")
