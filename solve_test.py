"""Direct solvability test for Psi_tau at a point (a,b,c,tau) of P_2, F = Q_2.

Psi_tau(a,b,c) :  delta_tau != 0  and  delta_tau(c^2 - A y^2) - 16*B*(r^2 - A s^2) = 16
with A = 1+4a^2, B = b*pi = 2b.

Rearrange:  32b * (r^2 - A s^2) = g(y) := delta(c^2 - A y^2) - 16 = -delta*A*(y^2 - w),
            w := (c^2 - 16/delta)/A.

A is a unit with A = 5 mod 8, so E = Q_2(sqrt A) is the unramified quadratic extension and the
norm form r^2 - A s^2 has image {x in Q_2 : v(x) even} u {0}   (Serre, Local Fields V.2).

Hence a solution exists iff  v(g) is odd for some y, or g = 0 for some y, i.e. iff
   v(w) odd,  or  w is a square,  or  w/2^{2m} = 3,7 mod 8   (m = v(w)/2).
The single failing residue class is  v(w) = 2m  and  w/2^{2m} = 5 mod 8.
"""
import random
from fractions import Fraction as Fr

from cells import build_cell, A0S, C0S
from padic import Q2


def classify(a, b, c, tau):
    """Return (solvable, verdict, detail) for the point (a,b,c) and parameter tau."""
    A = Q2.Z(1 + 4 * a * a)
    delta = Q2.Z(1) - A * Q2.Z(tau * tau)
    if delta.u == 0:
        return None, "delta=0", ""
    c2 = Q2.Z(c * c)
    w = (c2 - Q2.Z(16) * delta.inv()) * A.inv()
    if w.u == 0:
        return True, "w=0 (g=0 for y=0)", "v=inf"
    v = w.val()
    if v % 2 == 1:
        return True, "v(w) odd -> v(g) odd", "v(w)=%d" % v
    m = v // 2
    u = w.u % 8
    if u == 1:
        return True, "w is a square -> g=0", "v(w)=%d,u=1" % v
    if u == 3 or u == 7:
        return True, "u=3,7 mod 8 -> v(g) odd", "v(w)=%d,u=%d" % (v, u)
    return False, "OBSTRUCTION: v(w) even, u=5 mod 8", "v(w)=%d,u=%d" % (v, u)


def main():
    cells = [build_cell(a0, c0) for a0 in A0S for c0 in C0S]
    rng = random.Random(7)
    obst = []
    tot = 0
    print("--- Psi_tau solvability, cell tau, random points of each cell (a=a0 mod 8, c=c0 mod 8) ---")
    for cell in cells:
        a0, c0, tau = cell["a0"], cell["c0"], cell["tau"]
        cnt = {"ok": 0, "bad": 0, "why": {}}
        for _ in range(24):
            a = a0 + 8 * rng.randrange(-64, 64)
            c = c0 + 8 * rng.randrange(-64, 64)
            b = 2 * rng.randrange(-32, 32) + 1
            ok, why, det = classify(a, b, c, tau)
            tot += 1
            if ok:
                cnt["ok"] += 1
            else:
                cnt["bad"] += 1
                obst.append((a0, c0, tau, a, c, det))
            cnt["why"][why] = cnt["why"].get(why, 0) + 1
        print("a0=%d c0=%d tau=%d : ok=%2d bad=%2d   %s" % (
            a0, c0, tau, cnt["ok"], cnt["bad"],
            ", ".join("%s x%d" % (k, v) for k, v in sorted(cnt["why"].items()))))
    print()
    print("total points: %d   obstructions: %d" % (tot, len(obst)))
    if obst:
        print("first five obstructions (a0,c0,tau,a,c):")
        for o in obst[:5]:
            print("  cell(%d,%d) tau=%d  a=%d c=%d  %s" % o)

    # does some other tau rescue an obstructed point?
    print()
    print("--- can another tau rescue an obstructed point? ---")
    for o in obst[:6]:
        a0, c0, tau, a, c, det = o
        sols = [t for t in range(1, 64, 2) if classify(a, 1, c, t)[0]]
        print("  cell(%d,%d) a=%d c=%d : tau working in 1..63 odd: %s" % (a0, c0, a, c, sols[:12]))


if __name__ == "__main__":
    main()
