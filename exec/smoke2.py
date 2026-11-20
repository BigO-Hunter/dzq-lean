"""SMOKE2: the corrected patch semantics, all nine per-prime formulas, and the freezing layer.

The patch polynomial is  F_p = pi_p G_p(y,r,s) - p^2 X^2  and it must be locally soluble over Q_p
EXACTLY when X is NOT p-integral (v_p(X) <= -1), because the polynomial defines
Q \\ Z = {X : 1/X in U_w m_w} through Sun's duality (1.1).

Each case is checked two ways:
  * the square-class criterion (Prop 3.3: over a local field a quaternion algebra splits over every
    quadratic extension), and
  * an independent brute-force representation search for the ternary form <D,B,-BD>.
"""
from fractions import Fraction as Fr

import hilbert as H
from F_eval import E_EXC, PATCH
from localtest import brute_represent


def Rprime(x_or_X, d, pi, p, dual=True):
    """the value the ternary form must represent.

    dual=True  (this lane's polynomial): equation pi*G = p^2 X^2  ->  form = d/4 - p^2 X^2/pi
    dual=False (the earlier draft):       equation pi X^2 G = 1   ->  form = d/4 - 1/(pi X^2)
    """
    X = Fr(x_or_X)
    if dual:
        return Fr(d, 4) - Fr(p * p) * X * X / Fr(pi)
    return Fr(d, 4) - Fr(1) / (Fr(pi) * X * X)


def main():
    print("(1) F_p locally soluble  <=>  v_p(X) <= -1   (i.e. X not in Z_(p))")
    print("%4s | %s" % ("p", "X: v_p(X) : criterion / brute"))
    allok = True
    for consts in PATCH:
        p, pi_p, A_p, B_p, a_p = consts
        e = None
        import json
        with open("perprime.json") as f:
            e = json.load(f)[str(p)]
        D = 1 + 4 * A_p
        d = e["d"]
        cells = []
        for X in (1, 2, 3, 5, Fr(1, p), Fr(1, p * p), Fr(2, p), Fr(1, 1), Fr(p, 1)):
            X = Fr(X)
            vX = H_vp(X, p)
            R = Rprime(X, d, pi_p, p, dual=True)
            crit = (not H.is_square_at(R, p)) if R != 0 else False
            rep = brute_represent(p, D, B_p, R)
            agree = (crit == (rep is not None))
            # expected: soluble iff v_p(X) <= -1
            expect = (vX <= -1)
            ok = agree and (crit == expect)
            allok = allok and ok
            cells.append("%s:%2d:%s/%s%s" % (X, vX, "Y" if crit else "n", "Y" if rep else "n",
                                             "" if ok else "!"))
        print("%4d | %s" % (p, "  ".join(cells)))
    print("    all cells as expected:", allok)

    print()
    print("(2) integers must be rejected by every patch factor (no integer is in any m_p)")
    bad = []
    for X in range(1, 31):
        for consts in PATCH:
            p, pi_p, A_p, B_p, a_p = consts
            import json
            with open("perprime.json") as f:
                d = json.load(f)[str(p)]["d"]
            R = Rprime(X, d, pi_p, p)
            if R != 0 and not H.is_square_at(R, p):
                bad.append((X, p))
    print("    integers 1..30 with a soluble patch factor:", bad if bad else "none")

    print()
    print("(3) non-integers: exactly the primes in their denominator make a factor soluble")
    import json
    with open("perprime.json") as f:
        pp = json.load(f)
    for X in (Fr(1, 3), Fr(1, 5), Fr(1, 7), Fr(2, 9), Fr(3, 10), Fr(1, 23)):
        sol = []
        for consts in PATCH:
            p, pi_p, A_p, B_p, a_p = consts
            d = pp[str(p)]["d"]
            R = Rprime(X, d, pi_p, p)
            if R != 0 and not H.is_square_at(R, p):
                sol.append(p)
        dens = sorted({int(p) for p in pp if Fr(X).denominator % int(p) == 0})
        print("    X=%-5s denominator primes %-12s patch factors soluble: %s" % (X, dens, sol))
        assert sol == dens, (X, sol, dens)

    print()
    print("(4) freezing layer: the 8 parameters serve their classes (exhaustive, a mod 2^7)")
    from solve_test import classify
    A_SET, B_SET = set(range(1, 8)), {0, 4}
    for tau, cset, tag in ([(t, A_SET, "A") for t in (1, 17, 33, 49)]
                           + [(t, B_SET, "B") for t in (3, 11, 19, 27)]):
        bad = tot = 0
        for a in range(1, 128, 2):
            for c in range(0, 128):
                if c % 8 not in cset:
                    continue
                tot += 1
                if not classify(a, 1, c, tau)[0]:
                    bad += 1
        print("    class %s tau=%-3d obstructed %d/%d" % (tag, tau, bad, tot))
        assert bad == 0


def H_vp(x, p):
    x = Fr(x)
    def v(n):
        k = 0
        while n % p == 0:
            n //= p
            k += 1
        return k
    return v(abs(x.numerator)) - v(x.denominator)


if __name__ == "__main__":
    main()
