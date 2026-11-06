"""Per-prime Prop 4.2 constants: for each p in E_exc find (A_p, B_p, a_p, pi_p) satisfying the
checked hypotheses of Daans Lemma 4.1, and emit the resulting single polynomial F_p.

Lemma 4.1 (Daans), K = Q, S = {p}: with a nonreal quaternion Q = [A,B), S <= Delta(Q), and
pi, a in Q^:
   (h1) for all v in Delta(Q):  v(pi) = 1
   (h2) for all v in Delta(Q):  v(a) >= 0  and  v(1+4a) = 0
   (h3) X^2 - X - a has a root over Q_v  <=>  v in S
then  cap_{v in S} O_v = {0} u {x : Q splits over K_(a - (pi x^2)^-1)}.

Prop 3.6(iii) with c = 1, d = -a' (a' = a - (pi x^2)^-1) gives the exists-3 formula

   F_p(X, s1, s2, s3) = pi * X^2 * G_p(s1,s2,s3) - 1 ,     with x = X/pi^0 = X

after clearing the denominator of x = X/p for the maximal ideal m_p (x := X/p, so the cleared
form has constant term p^2):

   F_p = pi_p * X^2 * [ (1+4A_p)(s1 - s1^2) + (a_p - A_p) - B_p (s2^2 + s2 s3 - A_p s3^2) ] - p^2

and  X in m_p  <=>  F_p = 0 has a solution (x = 0 branch absorbed: 0 is in every m_p).
"""
import json
from fractions import Fraction as Fr

import hilbert as H

PREC = 64


def delta_of(A, B):
    """Delta of the quaternion [A,B) = (1+4A, B) in char != 2."""
    return H.ramified_primes(1 + 4 * A, B)


def find_quaternion(p, amax=30, bmax=30):
    """smallest (|A|+|B| first) pair with Delta(1+4A,B) = {p,q}, q != p, nonreal."""
    best = None
    for A in range(-amax, amax + 1):
        if A == 0 or 1 + 4 * A == 0:
            continue
        for B in range(-bmax, bmax + 1):
            if B == 0:
                continue
            dl = delta_of(A, B)
            if p not in dl or "inf" in dl or len(dl) != 2:
                continue
            q = next(iter(dl - {p}))
            key = (abs(A) + abs(B), abs(A), abs(B))
            if best is None or key < best[0]:
                best = (key, A, B, q)
    return None if best is None else (best[1], best[2], best[3])


def find_a(p, q, amax=400):
    """smallest a >= 0 with d = 1+4a coprime to pq, square at p, nonsquare at q, and pq*d not a
    perfect square (kills the degenerate stratum)."""
    for a in range(0, amax):
        d = 1 + 4 * a
        if d % p == 0 or d % q == 0:
            continue
        if not H.is_square_at(d, p):
            continue
        if H.is_square_at(d, q):
            continue
        if H.squarefree_part(p * q * d) == 1:
            continue
        return a, d
    return None


def check_all(p, A, B, a, verbose=False):
    """verify (h1)-(h3) and the degenerate-stratum condition; return dict of booleans."""
    D = 1 + 4 * A
    dl = delta_of(A, B)
    q = next(iter(dl - {p})) if p in dl and len(dl) == 2 else None
    pi = p * q if q else None
    d = 1 + 4 * a
    out = {"Delta": sorted(dl, key=str), "q": q, "pi": pi, "d": d}
    out["(h0) p in Delta and |Delta| = 2"] = (p in dl and len(dl) == 2)
    out["(h0b) nonreal"] = ("inf" not in dl)
    out["(h1) v_pi = 1 on Delta"] = all(
        (lambda v: (pi % v == 0 and (pi // v) % v != 0) if v != "inf" else True)(v) for v in dl)
    out["(h2a) v(a) >= 0 on Delta"] = all(a % v == 0 or a != 0 for v in dl if v != "inf") and a >= 0
    out["(h2b) v(1+4a) = 0 on Delta"] = all(d % v != 0 for v in dl if v != "inf")
    out["(h3a) disc square at p"] = H.is_square_at(d, p)
    out["(h3b) disc nonsquare at q"] = (q is not None) and (not H.is_square_at(d, q))
    out["degenerate stratum empty"] = H.squarefree_part(pi * d) != 1 if pi else False
    # x = 0 branch: x = 0 means X = 0, and 0 is in every m_p -- nothing to check.
    return out


def F_p(A, B, a, pi, p):
    """the emitted polynomial as a coefficient dictionary over (X, s1, s2, s3) exponents."""
    D = 1 + 4 * A
    # bracket = D*(s1 - s1^2) + (a - A) - B*(s2^2 + s2*s3 - A*s3^2)
    terms = {}
    terms[(0, 1, 0, 0)] = D
    terms[(0, 2, 0, 0)] = -D
    terms[(0, 0, 0, 0)] = a - A
    terms[(0, 0, 2, 0)] = -B
    terms[(0, 0, 1, 1)] = -B
    terms[(0, 0, 0, 2)] = B * A
    out = {}
    for k, c in terms.items():
        out[(2 + k[0], k[1], k[2], k[3])] = c * pi
    out[(0, 0, 0, 0)] = out.get((0, 0, 0, 0), 0) - p * p
    return {k: v for k, v in out.items() if v}


def main():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    res = {}
    print("%3s %5s %4s %4s %4s %5s  %s" % ("p", "A", "B", "q", "a", "pi", "checks"))
    for p in primes:
        found = find_quaternion(p)
        if not found:
            print("%3d  NO QUATERNION FOUND" % p)
            continue
        A, B, q = found
        fa = find_a(p, q)
        if not fa:
            print("%3d  A=%d B=%d q=%d  NO a FOUND" % (p, A, B, q))
            continue
        a, d = fa
        chk = check_all(p, A, B, a)
        bad = [k for k, v in chk.items() if isinstance(v, bool) and not v]
        print("%3d %5d %4d %4d %4d %5d  %s" % (
            p, A, B, q, a, p * q, "ALL PASS" if not bad else "FAIL: %s" % bad))
        res[p] = {"A": A, "B": B, "q": q, "a": a, "d": d, "pi": p * q,
                  "Delta": chk["Delta"], "checks": {k: v for k, v in chk.items() if isinstance(v, bool)},
                  "F_p": {"%d,%d,%d,%d" % k: v for k, v in F_p(A, B, a, p * q, p).items()}}
    with open("perprime.json", "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print()
    print("wrote perprime.json with %d primes" % len(res))


if __name__ == "__main__":
    main()
