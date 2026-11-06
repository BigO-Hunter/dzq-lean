#!/usr/bin/env python3
"""Exact-Q verification of mod-p row dependencies.

For each dependent row d (from rank_probe.json), lift the mod-p dependency to an
exact rational combination via multi-prime CRT + rational reconstruction of
ratios, then PROVE it by exact Fraction expansion. Rows whose reconstruction
fails are kept (not dropped) and reported UNVERIFIED.

Dependency convention: R_d = sum_{i in S} m_i * R_i  (mod p, multipliers from
the elimination). Exact target: R_d == sum x_i R_i over Q.
"""
import json, gzip, sys, collections
from fractions import Fraction
from math import gcd

sys.set_int_max_str_digits(200000)
BASE = "/Users/dmitri.arkhipov/bigo-campaign/dzq-anatomy/v4/quartics/quartic-4973"
OUT = "/Users/dmitri.arkhipov/bigo-campaign/dzq-t1"
PRIMES = [(1 << 61) - 1, (1 << 62) - 57, (1 << 63) - 25]

def load_rows():
    with gzip.open(f"{BASE}/residuals.json.gz") as f:
        rows_raw = json.load(f)
    return [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]

def elim_with_mult(rows_list, P):
    """returns (pivots, deps) where deps[d] = multiplier dict {row_idx: coeff mod P}
    meaning R_d = sum m_i R_i (mod P); pivot rows store their own multiplier vector."""
    mons = {}
    vecs = []
    for r in rows_list:
        d = {}
        for m, c in r.items():
            if m not in mons: mons[m] = len(mons)
            d[mons[m]] = c % P
        vecs.append(d)
    piv = {}   # col -> (vec, mult, row_idx)
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
    return piv, deps

def crt(a1, p1, a2, p2):
    # combine x = a1 mod p1, x = a2 mod p2
    inv = pow(p1, -1, p2)
    k = (a2 - a1) * inv % p2
    return (a1 + p1 * k) % (p1 * p2), p1 * p2

def rat_recon(y, M):
    """rational reconstruction of y mod M: find n/d with |n|,|d| <= sqrt(M/2)."""
    if y == 0:
        return Fraction(0)
    B = int((M // 2) ** 0.5) + 1
    # extended euclid bound variant: use python's standard algorithm
    a, b = M, y % M
    u0, u1 = 0, 1
    while b > B:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
    if b == 0:
        return None
    n = u1 * (1 if y % M == b else -1) if False else None
    # simpler: backtrack from (b, u1)
    num = u1
    den = b
    if num.denominator != 1:
        return None
    nn = int(num)
    if abs(nn) > B:
        return None
    return Fraction(nn, den)

def main():
    rows = load_rows()
    # dependencies per prime
    alldeps = []
    for P in PRIMES:
        piv, deps = elim_with_mult(rows, P)
        alldeps.append(deps)
        print(f"prime 2^61-1 class {P.bit_length()}b: {len(deps)} dependent rows, rank {len(piv)}")
    depset = set(alldeps[0])
    for d in alldeps[1:]:
        depset &= set(d)
    print(f"dependent under all primes: {len(depset)}")

    proved = []
    failed = []
    for d in sorted(depset):
        # CRT-combine multiplier ratios
        ref = None
        cands = []
        ok = True
        for P, deps in zip(PRIMES, alldeps):
            m = deps.get(d)
            if not m:
                ok = False; break
            if ref is None:
                ref = max(m, key=lambda k: abs(m[k]) if k != d else 0)
            cands.append((m, P))
        if not ok:
            failed.append(d); continue
        # ratios y_i / y_ref per prime, CRT, rational-reconstruct
        M = 1
        rat_crt = {}
        good = True
        for m, P in cands:
            yref = m.get(ref)
            if not yref:
                good = False; break
            for i in set(list(m.keys()) + [d]):
                yi = m.get(i, 1 if i == d else 0)
                ri = yi * pow(yref, -1, P) % P
                if i in rat_crt:
                    v, M2 = rat_crt[i]
                    nv, NM = crt(v, M2, ri, P)
                    rat_crt[i] = (nv, NM)
                else:
                    rat_crt[i] = (ri, P)
        if not good:
            failed.append(d); continue
        Ms = max(M2 for _, M2 in rat_crt.values())
        xs = {}
        good = True
        for i, (v, M2) in rat_crt.items():
            # center
            if v > M2 // 2: v -= M2
            r = rat_recon(v % M2, M2)
            if r is None:
                good = False; break
            xs[i] = r
        if not good:
            failed.append(d); continue
        # exact verification: R_d == sum xs[i] * R_i
        exp = collections.defaultdict(Fraction)
        for i, x in xs.items():
            for m, c in rows[i].items():
                exp[m] += x * c
        target = {m: Fraction(c) for m, c in rows[d].items()}
        if dict(exp) == target:
            proved.append((d, {i: str(x) for i, x in xs.items() if x}))
        else:
            failed.append(d)
    print(f"proved exact-Q dependencies: {len(proved)}; failed/unverified: {len(failed)}")
    json.dump({"proved": proved, "failed": failed}, open(f"{OUT}/exactq_deps.json", "w"))
    for d, xs in proved[:5]:
        print(f"  row {d} = combination of {len(xs)} rows; sample coeffs {list(xs.items())[:4]}")

if __name__ == "__main__":
    main()
