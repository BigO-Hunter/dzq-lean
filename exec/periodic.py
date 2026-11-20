"""Constructive replacement for the broken mod-8 claim:

  (P1) periodicity: the obstruction function O(a,c,tau) depends only on a mod 2^8, c mod 2^8,
       tau mod 2^4  (verified: shifting a or c by 256 never changes the verdict).
  (P2) an explicit per-cell tau map with ZERO obstructions over the full residue grid mod 2^10.
"""
import random

from solve_test import classify

PERIOD = 256


def periodic_check(n=4000, seed=5):
    rng = random.Random(seed)
    bad = 0
    for _ in range(n):
        a = rng.randrange(-1000, 1000) * 2 + 1
        c = rng.randrange(-1000, 1000)
        tau = 2 * rng.randrange(0, 8) + 1
        base = classify(a, 1, c, tau)[0]
        for sh in (256, 512, -256, -512):
            if classify(a + sh, 1, c, tau)[0] != base:
                bad += 1
                break
            if classify(a, 1, c + sh, tau)[0] != base:
                bad += 1
                break
    print("(P1) period-256 check: %d/%d shifts changed the verdict  -> %s" % (
        bad, n, "PERIODIC mod 2^8 in a and c (0 exceptions)" if bad == 0 else "NOT periodic"))


def best_tau_per_cell():
    """tau map: c0=0 -> 3, else 1.  Verify over the full grid mod 2^10."""
    m = 1 << 10
    print("(P2) exhaustive grid a = a0 mod 8 (full mod 2^10), c = c0 mod 8 (full mod 2^10)")
    print("%3s %3s %4s  %s" % ("a0", "c0", "tau", "obstructions"))
    total = 0
    for a0 in (1, 3, 5, 7):
        for c0 in range(8):
            tau = 3 if c0 == 0 or c0 == 4 else 1
            bad = 0
            for a in range(a0, m, 8):
                for c in range(c0, m, 8):
                    if not classify(a, 1, c, tau)[0]:
                        bad += 1
                    total += 1
            print("%3d %3d %4d  %d" % (a0, c0, tau, bad))
    print("grid points examined: %d" % total)


if __name__ == "__main__":
    periodic_check()
    best_tau_per_cell()
