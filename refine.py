"""How fine must the decomposition be?  Scan (cell modulus, tau) pairs for zero-failure covers.

The criterion (verified against exhaustive mod-2^K search) is:
    Psi_tau(a,b,c) solvable in Q_2  <=>  NOT( v(w) even and w/2^v(w) = 5 mod 8 ),
    w = (c^2 - 16/delta_tau)/A,  A = 1+4a^2,  delta_tau = 1 - A tau^2.
b and the pi-part do not enter once b is a unit.
"""
import random

from solve_test import classify

A0S = (1, 3, 5, 7)


def failures(a_res, c_res, modulus, tau, n=24, rng=None):
    """count obstructed sample points in the class (a = a_res, c = c_res mod 2^modulus)."""
    rng = rng or random.Random(11)
    bad = 0
    for _ in range(n):
        a = a_res + modulus * rng.randrange(-8, 8)
        c = c_res + modulus * rng.randrange(-8, 8)
        ok, _why, _det = classify(a, 1, c, tau)
        if not ok:
            bad += 1
    return bad


def scan(modulus, taus, n=20, label=""):
    """for each class mod `modulus` (odd residues) find taus with zero failures."""
    print("=== modulus 2^%d : cells = odd a-residues x c-residues %s" % (modulus, label))
    odd = [r for r in range(modulus) if r % 2 == 1]
    covered = 0
    total = 0
    per_cell_best = {}
    for a_res in odd:
        for c_res in range(modulus):
            total += 1
            good = []
            for tau in taus:
                f = failures(a_res, c_res, modulus, tau, n=n)
                if f == 0:
                    good.append(tau)
            per_cell_best[(a_res, c_res)] = good
            if good:
                covered += 1
            else:
                print("   NO tau works for a=%d c=%d mod %d" % (a_res, c_res, modulus))
    print("   cells: %d   coverable by a single tau: %d" % (total, covered))
    # minimal tau set covering all cells greedily
    remaining = {k: set(v) for k, v in per_cell_best.items() if v}
    chosen = []
    while remaining:
        # pick tau covering most cells
        cand = {}
        for cell, taus_ok in remaining.items():
            for t in taus_ok:
                cand[t] = cand.get(t, 0) + 1
        best = max(cand.items(), key=lambda kv: kv[1])
        chosen.append(best)
        for cell in [c for c, ts in remaining.items() if best[0] in ts]:
            del remaining[cell]
    print("   greedy tau cover: %d taus -> %s" % (len(chosen), [c[0] for c in chosen]))
    return per_cell_best


def main():
    for modulus in (8, 16, 32):
        # tau mod 2^m as integers; the residue class matters, so scan residues with small reps
        taus = list(range(1, 2 * modulus, 2))
        scan(modulus, taus, n=12)


if __name__ == "__main__":
    main()
