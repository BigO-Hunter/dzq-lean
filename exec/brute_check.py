"""Rigorous independent checks for the obstruction, without the norm-group criterion.

(A) The norm form image.  For A = 5 mod 8, verify by exhaustive enumeration that
        { r^2 - A s^2  mod 2^K : r,s }  =  { x mod 2^K : v(x) even } u {0}
    (i.e. the norm group of the unramified quadratic extension is the even-valuation set).

(B) Necessary-condition search over y.  A 2-adic solution of
        delta(c^2 - A y^2) - 32 b (r^2 - A s^2) = 16
    must reduce to a solution mod 2^K for every K.  Enumerate y mod 2^K and ask whether
    g(y) mod 2^K lies in 32b * Im_K .  If no y passes for some K, no solution exists.
"""
from solve_test import classify

ODD = [5, 101, 197, 13, 3]  # representative A = 1+4a^2 values (A = 5 mod 8)


def image_set(A, K):
    m = 1 << K
    A %= m
    out = set()
    for s in range(m):
        Asq = (A * s * s) % m
        for r in range(m):
            out.add((r * r - Asq) % m)
    return out


def even_val_set(K):
    m = 1 << K
    out = {0}
    for x in range(1, m):
        v = 0
        y = x
        while y % 2 == 0:
            y //= 2
            v += 1
        if v % 2 == 0:
            out.add(x)
    return out


def check_A(K):
    print("(A) norm-form image mod 2^%d" % K)
    for A in ODD:
        img = image_set(A, K)
        ev = even_val_set(K)
        print("    A=%-4d |Im|=%3d  |even_val|=%3d  equal=%s  missing=%s" % (
            A, len(img), len(ev), img == ev, sorted(ev - img)[:5]))


def necessary_y_search(a, b, c, tau, K):
    """True if some y mod 2^K passes the mod-2^K necessary condition."""
    m = 1 << K
    A = (1 + 4 * a * a) % m
    delta = (1 - A * (tau * tau % m)) % m
    # Im of r^2 - A s^2 mod 2^K  -> after multiplying by 32b mod 2^K
    KK = K - 5
    target = set()
    if KK <= 0:
        target = {0}
    else:
        mk = 1 << KK
        An = A % mk
        img = set()
        for s in range(mk):
            Asq = (An * s * s) % mk
            for r in range(mk):
                img.add((r * r - Asq) % mk)
        bb = (32 * b) % m
        for x in img:
            target.add((bb * x) % m)
    good = []
    for y in range(m):
        gy = (delta * (c * c - A * y * y) - 16) % m
        if gy in target:
            good.append(y)
    return good


def main():
    check_A(6)
    check_A(8)
    print()
    print("(B) necessary-condition y-search (K = 10, 12) on criterion-obstructed points")
    cases = [
        ("obstructed (c0=0 cell, tau=1)", 145, 1, -208, 1),
        ("obstructed (c0=0 cell, tau=1)", -415, 1, -368, 1),
        ("obstructed (c0=6 cell, tau=5)", None, 1, None, 5),
        ("rescued  (same point, tau=3)", 145, 1, -208, 3),
        ("control  (c0=1 cell, tau=3)", 9, 1, 1, 3),
    ]
    for tag, a, b, c, tau in cases:
        if a is None:
            continue
        ok, why, det = classify(a, b, c, tau)
        print()
        print("%s  a=%d c=%d tau=%d" % (tag, a, c, tau))
        print("   criterion: solvable=%s  (%s)  %s" % (ok, why, det))
        for K in (10, 12):
            g = necessary_y_search(a, b, c, tau, K)
            print("   K=%2d: %d admissible y residues; e.g. %s" % (K, len(g), g[:6]))


if __name__ == "__main__":
    main()
