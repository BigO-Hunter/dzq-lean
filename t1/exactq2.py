#!/usr/bin/env python3
"""Exact-Q verification of row-span dependencies on a residual list.
Usage: exactq2.py <residuals.json.gz> <out.json>
For each row dependent under prime 1: build candidate via CRT with primes 2..k
(lazy), rationally reconstruct, PROVE by exact Fraction expansion.
Convention from elimination: sum_i mult[i] * R_i == 0 (mod p), mult[d] = 1.
"""
import json, gzip, sys, collections
from fractions import Fraction

sys.set_int_max_str_digits(200000)
PRIMES = [(1 << 61) - 1, (1 << 62) - 57, (1 << 63) - 25]

def elim(rows_list, P):
    mons = {}
    vecs = []
    for r in rows_list:
        d = {}
        for m, c in r.items():
            if m not in mons: mons[m] = len(mons)
            d[mons[m]] = c % P
        vecs.append(d)
    piv = {}
    deps = {}
    for idx, vec in enumerate(vecs):
        cur = dict(vec)
        mult = {idx: 1}
        is_dep = True
        while cur:
            col = min(cur)
            if col in piv:
                pv, pm, _ = piv[col]
                f = cur[col]
                for c2, v2 in pv.items():
                    nc = (cur.get(c2, 0) - f * v2) % P
                    if nc: cur[c2] = nc
                    elif c2 in cur: del cur[c2]
                for r2, m2 in pm.items():
                    nm = (mult.get(r2, 0) - f * m2) % P
                    if nm: mult[r2] = nm
                    elif r2 in mult: del mult[r2]
            else:
                piv[col] = (dict(cur), dict(mult), idx)
                is_dep = False
                break
        if is_dep and vec:
            deps[idx] = dict(mult)
    return len(piv), deps

def crt_pair(a1, m1, a2, m2):
    inv = pow(m1, -1, m2)
    k = (a2 - a1) * inv % m2
    return (a1 + m1 * k) % (m1 * m2), m1 * m2

def rat_recon(y, M):
    if y == 0:
        return Fraction(0)
    B = int((M / 2) ** 0.5)
    s1, s2 = M, y % M
    t1, t2 = 0, 1
    while s2 > B:
        q = s1 // s2
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2
    if s2 == 0 or t2 == 0 or abs(s2) > B or abs(t2) > B:
        return None
    n, d = s2, t2
    if d < 0:
        n, d = -n, -d
    if (y * d - n) % M != 0:
        return None
    return Fraction(n, d)

def prove(rows, d, xs):
    exp = collections.defaultdict(Fraction)
    for i, x in xs.items():
        if x:
            for m, c in rows[i].items():
                exp[m] += x * c
    return all(c == 0 for c in exp.values())

def main():
    path, outp = sys.argv[1], sys.argv[2]
    rows = [ {tuple(sorted(m)): c for c, m in row} for row in json.load(gzip.open(path)) ]
    print(f"rows: {len(rows)}", flush=True)
    results = {}   # dep -> (nprimes_used, status)
    active = list(range(len(rows)))
    deps_all = []
    for pi, P in enumerate(PRIMES):
        n, deps = elim(rows, P)
        print(f"P#{pi}: rank {n}, dependent {len(deps)}", flush=True)
        deps_all.append(deps)
        if pi == 0:
            candidates = set(deps)
        else:
            candidates &= set(deps)
        # attempt lift for all current candidates
        proved = []
        for d in sorted(candidates):
            xs = try_lift(rows, [deps for deps in deps_all], d)
            if xs is not None:
                proved.append((d, xs))
        print(f"  after {pi+1} prime(s): {len(proved)} proved", flush=True)
    # final: use all primes
    proved = []
    unverified = []
    for d in sorted(candidates):
        xs = try_lift(rows, deps_all, d)
        if xs is not None:
            proved.append((d, xs))
        else:
            unverified.append(d)
    print(f"PROVED span-dependencies: {len(proved)}; UNVERIFIED: {len(unverified)}", flush=True)
    json.dump({"proved": [[d, {str(i): str(x) for i, x in xs.items()}] for d, xs in proved],
               "unverified": unverified},
              open(outp, "w"))
    for d, xs in proved[:6]:
        print(f"  row {d}: {len(xs)}-term combo, sample {[(i, str(x)) for i, x in list(xs.items())[:4]]}", flush=True)

def try_lift(rows, deps_list, d):
    ms = [(deps.get(d), P) for deps, P in zip(deps_list, PRIMES[:len(deps_list)])]
    if any(m is None for m, _ in ms):
        return None
    ref = None
    for m, _ in ms:
        if ref is None:
            ref = max((k for k in m if k != d), key=lambda k: m[k], default=None)
    if ref is None:
        return None
    acc = {}
    for m, P in ms:
        yref = m.get(ref)
        if not yref:
            return None
        new_acc = {}
        for i in set(m) | {d}:
            yi = m.get(i, 1 if i == d else 0)
            ri = yi * pow(yref, -1, P) % P
            if i in acc:
                v, M2 = acc[i]
                nv, NM = crt_pair(v, M2, ri, P)
                new_acc[i] = (nv, NM)
            else:
                new_acc[i] = (ri, P)
        acc = new_acc
    xs = {}
    for i, (v, M2) in acc.items():
        if v > M2 // 2:
            v -= M2
        r = rat_recon(v % M2, M2)
        if r is None:
            return None
        xs[i] = r
    if prove(rows, d, xs):
        return xs
    return None

if __name__ == "__main__":
    main()
