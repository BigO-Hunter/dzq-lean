"""Checks 2.0: controls and the algebra identity, for the per-prime constants.

(a) the derivation lane's documented p = 2 constants pass the same hypothesis checker;
(b) Prop 3.6(iii) with c = 1 simplifies, for EVERY (A,B), to the bracket this lane emits
    (symbolic identity, sympy);
(c) the criterion <-> brute-force agreement over a wider random sweep, including v_p(X) >= 2
    and non-integral X.
"""
import json
import random
from fractions import Fraction as Fr

import hilbert as H
from localtest import brute_represent, cprime
from perprime import check_all


def part_a():
    print("(a) the documented p=2 constants (A=1,B=2,a=8,pi=10) under the same checker:")
    chk = check_all(2, 1, 2, 8)
    for k, v in chk.items():
        if isinstance(v, bool):
            print("    %-34s %s" % (k, "PASS" if v else "FAIL"))
    return all(v for k, v in chk.items() if isinstance(v, bool))


def part_b():
    import sympy as sp

    print()
    print("(b) symbolic identity: Prop 3.6(iii) with c=1 equals the emitted bracket")
    A, B, x1, x2, x3 = sp.symbols("A B x1 x2 x3")
    lhs = x1**2 + x1 * (1 - 2 * x1) - A * (1 - 2 * x1) ** 2 - B * (x2**2 + x2 * x3 - A * x3**2)
    phi = x2**2 + x2 * x3 - A * x3**2
    bracket = (1 + 4 * A) * (x1 - x1**2) - A - B * phi
    diff = sp.simplify(lhs - bracket)
    print("    LHS(c=1) - [(1+4A)(x1-x1^2) - A - B phi] =", diff)
    ok = sp.simplify(diff) == 0
    print("    identity holds:", ok)
    # so  LHS = d  <=>  (1+4A)(x1-x1^2) + (a - A) - B phi = 1/(pi x^2)
    return ok


def part_c():
    with open("perprime.json") as f:
        pp = json.load(f)
    print()
    print("(c) criterion <-> brute force on a wider random sweep")
    rng = random.Random(17)
    total = bad = 0
    for pkey in sorted(pp, key=int):
        p = int(pkey)
        e = pp[pkey]
        D = 1 + 4 * e["A"]
        B, pi, d = e["B"], e["pi"], e["d"]
        # X with a spread of valuations; x = X/p
        xs = []
        for k in range(1, 5):
            for _ in range(3):
                u = rng.randrange(1, 60)
                xs.append(Fr(u * p ** k, p))       # v_p(x) = k-1 >= 0   (X in m_p)
                if u % p:
                    xs.append(Fr(u, p * p))        # v_p(x) = -2         (X not in m_p)
        for x in xs:
            c = cprime(x, d, pi)
            crit = not H.is_square_at(c, p) if c != 0 else False
            rep = brute_represent(p, D, B, c)
            total += 1
            if crit != (rep is not None):
                bad += 1
                print("    mismatch p=%d x=%s c=%s crit=%s brute=%s" % (p, x, c, crit, rep))
    print("    %d/%d points agree" % (total - bad, total))
    return bad == 0


def part_d():
    """the emitted F_p really is pi*X^2*bracket - p^2 (numeric spot check against the formula)."""
    with open("perprime.json") as f:
        pp = json.load(f)
    print()
    print("(d) emitted coefficient dictionary reproduces pi*X^2*G - p^2 for random inputs")
    ok = True
    rng = random.Random(5)
    for pkey in sorted(pp, key=int):
        p = int(pkey)
        e = pp[pkey]
        A, B, a, pi = e["A"], e["B"], e["a"], e["pi"]
        terms = {tuple(int(t) for t in k.split(",")): v for k, v in e["F_p"].items()}
        for _ in range(5):
            X = Fr(rng.randrange(-6, 7), rng.randrange(1, 5))
            s1, s2, s3 = (Fr(rng.randrange(-5, 6), rng.randrange(1, 4)) for _ in range(3))
            vals = [X, s1, s2, s3]
            v1 = sum(c * (vals[0] ** k[0]) * (vals[1] ** k[1]) * (vals[2] ** k[2]) * (vals[3] ** k[3])
                     for k, c in terms.items())
            br = (1 + 4 * A) * (s1 - s1**2) + (a - A) - B * (s2**2 + s2 * s3 - A * s3**2)
            v2 = pi * X * X * br - p * p
            if v1 != v2:
                ok = False
                print("    MISMATCH p=%d X=%s s=%s/%s/%s : %s vs %s" % (p, X, s1, s2, s3, v1, v2))
    print("    all 9 primes match:", ok)
    return ok


if __name__ == "__main__":
    a = part_a()
    b = part_b()
    c = part_c()
    d = part_d()
    print()
    print("SUMMARY:", {"documented p=2 constants valid": a, "algebra identity": b,
                       "criterion==brute": c, "coefficient dict == formula": d})
