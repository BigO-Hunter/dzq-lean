#!/usr/bin/env python3
"""Aggregate the construction-map instantiations into a per-module ledger."""
import json, sys, collections

def load(path):
    with open(path) as f:
        return json.load(f)

def agg(m):
    out = collections.Counter()
    resid = collections.Counter()
    locs = collections.Counter()
    n = [0]
    def walk(node, depth):
        mod = node["module"]
        out[mod] += node.get("local_count", 0)
        resid[mod] += node.get("residual_count", 0)
        n[0] += 1
        for c in node.get("children", []) or []:
            walk(c, depth + 1)
    # instantiations may be nested via "children" or flat list
    def flat(nodes):
        for it in nodes:
            mod = it["module"]
            out[mod] += it.get("local_count", 0)
            resid[mod] += it.get("residual_count", 0)
            n[0] += 1
    if "instantiations" in m:
        flat(m["instantiations"])
    else:
        walk(m, 0)
    return out, resid, n[0]

if __name__ == "__main__":
    for path in sys.argv[1:]:
        m = load(path)
        out, resid, total = agg(m)
        print("=====", path, "instantiations:", total)
        print(f"{'module':30} {'locals':>8} {'residuals':>10}")
        for mod, c in out.most_common():
            print(f"{mod:30} {c:8d} {resid[mod]:10d}")
        print("TOTAL locals", sum(out.values()), "residuals", sum(resid.values()))
