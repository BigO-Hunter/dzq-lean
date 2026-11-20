"""Extra checks backing three statements in VERIFICATION.md.

(a) I3 split by parity: v(dc^2) >= 4 for c0 odd, >= 5 for c0 even (G1 states both);
(b) b-irrelevance: the psi_tau verdict does not depend on the unit b at all;
(c) delta_tau != 0 (with v = 2) for the corrected tau map, on deep random points;
(d) the period-256 flip count cited in VERIFICATION.md 6.
"""
import random

from cells import A0S, C0S, build_cell
from padic import Q2
from periodic import periodic_check
from solve_test import classify


def main():
    cells = [build_cell(a0, c0) for a0 in A0S for c0 in C0S]
    rng = random.Random(1)
    mins = {0: 99, 1: 99}
    for c in cells:
        a0, c0 = c["a0"], c["c0"]
        for _ in range(300):
            cc = c0 + 8 * rng.randrange(-256, 256)
            d = Q2.Z(cc * cc - c0 * c0)
            if d.u:
                mins[c0 % 2] = min(mins[c0 % 2], d.k)
    print("(a) I3: min v(dc^2)  c0 odd = %d,  c0 even = %d" % (mins[1], mins[0]))

    bad = tot = 0
    for _ in range(3000):
        a = 2 * rng.randrange(-2 ** 10, 2 ** 10) + 1
        c = rng.randrange(-2 ** 10, 2 ** 10)
        tau = 3 if c % 4 == 0 else 1
        v = [classify(a, b, c, tau)[0] for b in (1, 3, 5, 7, -1, -3, 9, 15)]
        tot += 1
        if len(set(v)) != 1:
            bad += 1
    print("(b) b-irrelevance over 8 unit b values: %d/%d points disagreed" % (bad, tot))

    bad = 0
    for _ in range(20000):
        a = 2 * rng.randrange(-2 ** 20, 2 ** 20) + 1
        c = rng.randrange(-2 ** 20, 2 ** 20)
        tau = 3 if c % 4 == 0 else 1
        d = Q2.Z(1) - Q2.Z(1 + 4 * a * a) * Q2.Z(tau * tau)
        if d.u == 0 or d.k != 2:
            bad += 1
    print("(c) delta_tau != 0 with v = 2: %d violations / 20000" % bad)

    periodic_check(n=4000, seed=5)


if __name__ == "__main__":
    main()
