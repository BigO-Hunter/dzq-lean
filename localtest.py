"""Local behaviour of each per-prime patch polynomial F_p over Q_p.

F_p(X, s1, s2, s3) = pi X^2 G_p - p^2   must vanish for some (s1,s2,s3) in Q_p^3 exactly when
X in m_p (v_p(X) >= 1).  Substituting u = s1 - 1/2, v = s2 + s3/2, w = s3/2 and clearing, the
equation is equivalent to

        D U^2 + B V^2 - B D W^2 = c'(x),      c'(x) = d - 4/(pi x^2),   x = X/p,

with D = 1+4A, and (U,V,W) ranging over Q_p^3.  Prop 3.3 (a quaternion algebra splits over every
quadratic extension of a LOCAL field) turns solvability into the square-class test

        solvable over Q_p  <=>  c'(x) is a NON-square in Q_p          (x != 0),

because for c' a square the splitting field is Q_p itself and Q_p is a division algebra at p.
This file checks that equivalence two ways:
  (i)  the square-class criterion, exactly, from the constants;
  (ii) a brute-force representation search for the ternary form, which never uses the criterion.
"""
import json
from fractions import Fraction as Fr

import hilbert as H


def cprime(x, d, pi):
    return Fr(d) - Fr(4) / (Fr(pi) * Fr(x) * Fr(x))


def _vq(x, p):
    """p-adic valuation of a non-zero rational."""
    x = Fr(x)
    def vp(n):
        v = 0
        while n % p == 0:
            n //= p
            v += 1
        return v
    return vp(abs(x.numerator)) - vp(x.denominator)


def brute_represent(p, D, B, c, N=40):
    """Represent c by <D,B,-BD> over Q_p.

    Every value on an INTEGRAL triple is integral, and scaling (U,V,W) by p^m scales the value by
    p^{2m}; so c is represented iff c/p^{2m} is represented by an integral triple, with
    2m = 2*floor(v(c)/2) the largest even integer below v(c).  Then the target has valuation 0 or
    1 and a bounded box search is meaningful.
    """
    if c == 0:
        return None
    v = _vq(c, p)
    m = v // 2
    t = c / Fr(p) ** (2 * m)
    for V in range(-N, N + 1):
        BV2 = B * V * V
        for W in range(-N, N + 1):
            rest = t - BV2 + B * D * W * W
            U2 = rest / D
            if U2 == 0:
                continue
            if H.is_square_at(U2, p):
                return (U2, V, W)
    return None


def main():
    with open("perprime.json") as f:
        pp = json.load(f)
    out = {}
    print("%3s  %-28s %-28s %s" % ("p", "x in m_p (criterion/brute)", "x not in m_p (crit/brute)", "agree?"))
    for pkey in sorted(pp, key=int):
        p = int(pkey)
        e = pp[pkey]
        A, B, a, pi, d = e["A"], e["B"], e["a"], e["pi"], e["d"]
        D = 1 + 4 * A
        rows = []
        agree = True
        for u in (1, 2, 3):                 # X = p*u  in m_p  (p may divide u -- still in m_p)
            x = u                            # x = X/p has v_p(x) >= 0
            c = cprime(x, d, pi)
            crit = not H.is_square_at(c, p)
            rep = brute_represent(p, D, B, c)
            agree = agree and (crit == (rep is not None))
            rows.append(("in", u, crit, rep is not None))
        for U in (1, 2, 3, 5):             # X coprime to p  ->  NOT in m_p
            if U % p == 0:
                continue
            xq = Fr(U, p)                   # x = X/p has v_p(x) = -1
            c = cprime(xq, d, pi)
            crit = not H.is_square_at(c, p)
            rep = brute_represent(p, D, B, c)
            agree = agree and (crit == (rep is not None))
            rows.append(("out", U, crit, rep is not None))
        print("%3d  %-28s %-28s %s" % (
            p,
            " ".join("%d:%s/%s" % (x, "Y" if c else "n", "Y" if r else "n") for k, x, c, r in rows if k == "in"),
            " ".join("%d:%s/%s" % (x, "Y" if c else "n", "Y" if r else "n") for k, x, c, r in rows if k == "out"),
            "YES" if agree else "NO  <-- investigate"))
        out[p] = {"agree": agree,
                  "rows": [{"side": k, "x": str(x), "criterion_solvable": c, "brute_found": r}
                           for k, x, c, r in rows]}
    with open("localtest.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print()
    print("legend: <x>:<criterion solvable?>/<brute witness found?>")


if __name__ == "__main__":
    main()
