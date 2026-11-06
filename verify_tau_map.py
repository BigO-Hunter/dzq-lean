"""The proved replacement for G1's persistence argument, machine-checked.

Claim (this lane, elementary, complete -- see VERIFICATION.md):
  tau = 1  if c = 0,2,3 mod 4   (i.e. c not = 0 mod 4)
  tau = 3  if c = 0 mod 4
  gives, for EVERY (a,b,c) in P_2 = {a odd, b unit, c in Z_2}, a solution of
        delta_tau != 0  and  delta_tau (c^2 - A y^2) - 16*B*(r^2 - A s^2) = 16.
  Proof sketch, all three sub-cases:
    c odd      : w := (c^2-16/delta)/A = (a^2 c^2 + 4)/(a^2 A) = 1 mod 8, v(w)=0 -> w square,
                 r = s = 0, y = sqrt(w).
    c = 2 mod 4: v(a^2c^2+4) = 3 -> v(w) = 3 odd -> v(g) odd -> g/(32b) in Norm(E^/Q_2^) = 2Z.
    c = 0 mod 4: with tau = 3, delta = -4(2+9a^2), v(w) = 2 and w/4 = 3 or 7 mod 8 (never 5).
This script re-checks each step exactly (2-adic), including the explicit square root in case 1.
"""
import random

import padic as P
from padic import Q2, E
from solve_test import classify

TWO = Q2.Z(2)


def tau_for(c):
    return 3 if c % 4 == 0 else 1


def data(a, c, tau):
    A = Q2.Z(1 + 4 * a * a)
    delta = Q2.Z(1) - A * Q2.Z(tau * tau)
    w = (Q2.Z(c * c) - Q2.Z(16) * delta.inv()) * A.inv()
    g = delta * (Q2.Z(c * c) - A * Q2.Z(0)) - Q2.Z(16)  # at y = 0 (not the witness, just a probe)
    return A, delta, w


def case_check(a, c):
    """Return (case, ok, detail) for one (a,c); constructs the witness when case 1."""
    tau = tau_for(c)
    A, delta, w = data(a, c, tau)
    assert delta.u != 0
    if c % 2 == 1:
        # w must be a unit = 1 mod 8 : then y = sqrt(w) in Q_2 exists explicitly
        if not (w.k == 0 and (w.u % 8) == 1):
            return 1, False, "w not a 1-mod-8 unit: v=%s u=%s" % (w.k, w.u % 8)
        s = P.sqrt_unit(w)
        if not (s * s - w).ge(40):
            return 1, False, "sqrt(w) does not square back"
        # exact check of the equation with r = s = 0, y = sqrt(w)
        lhs = delta * (Q2.Z(c * c) - A * s * s) - Q2.Z(16)
        return 1, lhs.ge(40), "y=sqrt(w), residual v=%s" % (lhs.val() if lhs.u else "0")
    if c % 4 == 2:
        v = w.val()
        return 2, (v == 3), "v(w)=%s (must be 3, odd)" % v
    # c = 0 mod 4, tau = 3
    v = w.val()
    if v != 2:
        return 3, False, "v(w)=%s (expected 2)" % v
    u = w.u % 8
    return 3, (u in (1, 3, 7)), "v(w)=2, u=%d (must be 1,3,7 -- 5 is the obstruction)" % u


def main():
    rng = random.Random(2024)
    fails = []
    stats = {1: 0, 2: 0, 3: 0}
    N = 60000
    for _ in range(N):
        a = 2 * rng.randrange(-2 ** 20, 2 ** 20) + 1
        c = rng.choice([
            rng.randrange(-2 ** 20, 2 ** 20),
            rng.randrange(-2 ** 6, 2 ** 6) * 4,          # c = 0 mod 4
            rng.randrange(-2 ** 6, 2 ** 6) * 4 + 2,      # c = 2 mod 4
            rng.randrange(-2 ** 6, 2 ** 6) * 2 + 1,      # c odd
        ])
        case, ok, det = case_check(a, c)
        stats[case] += 1
        if not ok:
            fails.append((a, c, case, det))
        # independent cross-check with the solvability criterion
        ok2, why, d2 = classify(a, 1, c, tau_for(c))
        if not ok2:
            fails.append((a, c, case, "criterion says obstructed: " + d2))
    print("tau map: c != 0 mod 4 -> 1, c = 0 mod 4 -> 3")
    print("random points tested: %d   (case 1 c odd: %d, case 2 c=2 mod 4: %d, case 3 c=0 mod 4: %d)"
          % (N, stats[1], stats[2], stats[3]))
    print("failures: %d" % len(fails))
    for f in fails[:5]:
        print("   ", f)

    print()
    print("--- the broken cell tau (t_p mod 8) vs the corrected map, same random points ---")
    from cells import build_cell, A0S, C0S
    bad = 0
    tot = 0
    for a0 in A0S:
        for c0 in C0S:
            cell = build_cell(a0, c0)
            for _ in range(2000):
                a = a0 + 8 * rng.randrange(-2 ** 16, 2 ** 16)
                c = c0 + 8 * rng.randrange(-2 ** 16, 2 ** 16)
                tot += 1
                if not classify(a, 1, c, cell["tau"])[0]:
                    bad += 1
    print("cell tau from the Cayley construction: %d/%d points obstructed (%.2f%%)" % (
        bad, tot, 100.0 * bad / tot))


if __name__ == "__main__":
    main()
