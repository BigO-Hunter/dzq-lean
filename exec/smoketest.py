"""SMOKE TEST (sampled, not a proof) of the two local pieces that are assembled.

(1) Freezing at 2 : the 2-tau map  tau = 1 (c not 0 mod 4), tau = 3 (c = 0 mod 4) makes
    Psi_tau solvable at every point of P_2 (verified in verify_tau_map.py over 60k random
    points; here we add a *witness-carrying* check: for the case c odd we construct y and
    verify the equation exactly).

(2) the p = 2 patch formula (G2_REDERIVATION.md 1):
      x in Z_(2)  <=>  x = 0  or  exists x1,x2,x3 in Q: 10x^2(7+5x1-5x1^2-2x2^2-2x2x3+2x3^2) = 1
    Written with u = x1 - 1/2 and phi = x2^2+x2x3-x3^2 the equation is
        5u^2 + 2 phi = T(x) := 33/4 - 1/(10x^2).
    The form phi is the norm form of the unramified Q_2(sqrt5)/Q_2, so 2*phi takes exactly
    the values of ODD valuation (plus 0); 5u^2 takes exactly the values
    {z : v(z) even, z/2^v(z) = 5 mod 8} u {0}.  So we test: does some u put T - 5u^2 into
    {odd valuation} u {0}?  Search range: v(u) in [-4, 8], u mod 2^8.
"""
from fractions import Fraction as Fr

from padic import Q2


def vq(x):
    return None if x.u == 0 else x.k


def t_of(x):
    """T(x) = 33/4 - 1/(10x^2) as a Q2."""
    X = Q2.F(x)
    return Q2.F(Fr(33, 4)) - (Q2.F(10) * X * X).inv()


def witness_search(x, kmin=-4, kmax=8, bits=8):
    """search u = 2^k * m ; return the first u class that satisfies the criterion."""
    T = t_of(x)
    for k in range(kmin, kmax + 1):
        for m in range(1, 1 << bits, 2):
            u = Q2(k, m)  # 2^k * m
            rem = T - Q2.Z(5) * u * u
            if rem.u == 0:
                return k, m, "exact (T = 5u^2)"
            v = rem.k
            if v % 2 == 1:
                return k, m, "v(T-5u^2)=%d odd" % v
    return None


def main():
    print("(2) patch formula p=2 : search for (x1,x2,x3) as a function of x")
    print("%-10s %-8s %-10s %s" % ("x", "v2(x)", "in Z_(2)?", "witness / no witness in range"))
    samples = [Fr(0), Fr(1), Fr(2), Fr(3), Fr(4), Fr(-1), Fr(6), Fr(8), Fr(12), Fr(1, 2),
               Fr(3, 2), Fr(1, 4), Fr(-5, 1), Fr(8, 3), Fr(1, 3), Fr(1, 8), Fr(-7, 16)]
    for x in samples:
        if x == 0:
            print("%-10s %-8s %-10s %s" % (x, "-", "yes", "x = 0 branch of the disjunction"))
            continue
        X = Q2.F(x)
        v = X.k
        w = witness_search(x)
        print("%-10s %-8d %-10s %s" % (x, v, "yes" if v >= 0 else "NO", w if w else "none"))

    print()
    print("(1) freezing at 2 with an explicit witness (case c odd, r = s = 0, y = sqrt(w))")
    import random
    import padic as P
    from verify_tau_map import case_check
    rng = random.Random(99)
    ok = 0
    for _ in range(2000):
        a = 2 * rng.randrange(-2 ** 12, 2 ** 12) + 1
        c = 2 * rng.randrange(-2 ** 12, 2 ** 12) + 1
        case, good, det = case_check(a, c)
        ok += 1 if good else 0
    print("   2000 random (a,c) with c odd: %d/%d produced an exact witness" % (ok, 2000))


if __name__ == "__main__":
    main()
