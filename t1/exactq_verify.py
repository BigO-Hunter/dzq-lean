#!/usr/bin/env python3
"""Exact-Q verification of mod-p row dependencies (v2, clean).

For each row dependent under ALL primes: ratios mult[i]/mult[ref] are CRT-
combined across primes, rationally reconstructed (Wang), then the candidate
dependency is PROVEN by exact Fraction expansion: sum x_i R_i == 0 over Q with
x_d = 1. Rows failing reconstruction/proof stay in the system (UNVERIFIED).
"""
import os
import json, gzip, sys, collections
from fractions import Fraction

sys.set_int_max_str_digits(200000)
BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
OUT = os.path.dirname(__file__)
PRIMES = [(1 << 61) - 1, (1 << 62) - 57, (1 << 63) - 25, (1 << 31) - 1]

def load_rows():
    with gzip.open(f"{BASE}/residuals.json.gz") as f:
        rows_raw = json.load(f)
    return [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]

def elim_with_mult(rows_list, P, want_mults=True):
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
        mult = {idx: 1} if want_mults else None
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
                if want_mults:
                    for r2, m2 in pm.items():
                        nm = (mult.get(r2, 0) - f * m2) % P
                        if nm: mult[r2] = nm
                        elif r2 in mult: del mult[r2]
            else:
                piv[col] = (dict(cur), dict(mult) if want_mults else None, idx)
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
    """y mod M -> n/d with y*d == n (mod M), |n|,|d| <= sqrt(M/2); else None."""
    if y == 0:
        return Fraction(0)
    B = int((M / 2) ** 0.5)
    s1, s2 = M, y % M
    t1, t2 = 0, 1
    while s2 > B:
        q = s1 // s2
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2
    if s2 == 0 or t2 == 0:
        return None
    if abs(s2) > B or abs(t2) > B:
        return None
    n, d = s2, t2
    if d < 0:
        n, d = -n, -d
    if (y * d - n) % M != 0:
        return None
    return Fraction(n, d)

def main():
    rows = load_rows()
    alldeps = []
    for P in PRIMES:
        n, deps = elim_with_mult(rows, P)
        alldeps.append(deps)
        print(f"P={P:#x}: rank {n}, dependent {len(deps)}", flush=True)
    depset = set(alldeps[0])
    for d in alldeps[1:]:
        depset &= set(d)
    print(f"dependent under all {len(PRIMES)} primes: {len(depset)}", flush=True)

    proved, failed = [], []
    for d in sorted(depset):
        ms = [(deps.get(d), P) for deps, P in zip(alldeps, PRIMES)]
        if any(m is None for m, _ in ms):
            failed.append(d); continue
        ref = None
        for m, _ in ms:
            if ref is None:
                ref = max((k for k in m if k != d), key=lambda k: m[k], default=None)
        if ref is None:
            failed.append(d); continue
        # CRT ratios
        acc = {}
        Macc = 1
        okflag = True
        for m, P in ms:
            yref = m.get(ref)
            if not yref:
                okflag = False; break
            keys = set(m) | {d}
            new_acc = {}
            for i in keys:
                yi = m.get(i, 1 if i == d else 0)
                ri = yi * pow(yref, -1, P) % P
                if i in acc:
                    v, M2 = acc[i]
                    nv, NM = crt_pair(v, M2, ri, P)
                    new_acc[i] = (nv, NM)
                else:
                    new_acc[i] = (ri, P)
            acc = new_acc
        if not okflag:
            failed.append(d); continue
        xs = {}
        okflag = True
        for i, (v, M2) in acc.items():
            if v > M2 // 2:
                v -= M2
            r = rat_recon(v % M2, M2)
            if r is None:
                okflag = False; break
            xs[i] = r
        if not okflag:
            failed.append(d); continue
        # exact proof: sum x_i R_i == 0, with x_d forced 1? use xs as-is and check zero
        exp = collections.defaultdict(Fraction)
        for i, x in xs.items():
            if not x:
                continue
            for m, c in rows[i].items():
                exp[m] += x * c
        zero = all(c == 0 for c in exp.values()) and len(exp) == 0 or all(c == 0 for c in exp.values())
        if zero:
            proved.append((d, {i: str(x) for i, x in xs.items() if x}))
        else:
            failed.append(d)
    print(f"PROVED exact-Q: {len(proved)}; UNVERIFIED: {len(failed)}")
    json.dump({"proved": proved, "failed": failed}, open(f"{OUT}/exactq_deps.json", "w"))
    for d, xs in proved[:6]:
        print(f"  row {d}: combo of {len(xs)} rows, sample {list(xs.items())[:4]}")

if __name__ == "__main__":
    main()
