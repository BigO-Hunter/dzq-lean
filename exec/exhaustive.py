"""Exhaustive (not sampled) obstruction scan.

For a class modulus 2^M we enumerate EVERY (a, c) residue pair in
    a = a_res mod 2^M,  c = c_res mod 2^M
and count obstructions for a given tau.  Running the same scan at 2^M and 2^(M+1) and
getting identical counts shows the obstruction is decided by the first M 2-adic digits.
"""
from solve_test import classify


def scan_class(a_res, c_res, M, tau):
    m = 1 << M
    bad = 0
    tot = 0
    for i in range(m // 8 if a_res % 8 else m):
        pass
    # a runs over a_res + 8*i  (a is odd, so a mod 8 is fixed)
    aa = [a_res + 8 * i for i in range(m // 8)]
    cc = [c_res + 8 * j for j in range(m // 8)]
    first = None
    for a in aa:
        for c in cc:
            ok, why, det = classify(a, 1, c, tau)
            tot += 1
            if not ok:
                bad += 1
                if first is None:
                    first = (a, c, det)
    return bad, tot, first


def main():
    A0 = (1, 3, 5, 7)
    C0 = list(range(8))
    taus = [1, 3, 5, 7, 9, 11, 13, 15]
    print("exhaustive over a = a0 mod 8, c = c0 mod 8, both full mod 2^M")
    for M in (8, 9):
        print()
        print("=== M=%d  (a: %d values, c: %d values per cell) ===" % (M, (1 << M) // 8, (1 << M) // 8))
        print("%3s %3s | %s" % ("a0", "c0", "  ".join("tau=%-2d" % t for t in taus)))
        any_bad = False
        for a0 in A0:
            for c0 in C0:
                cells = []
                for tau in taus:
                    bad, tot, first = scan_class(a0, c0, M, tau)
                    cells.append("%-6s" % ("%d/%d" % (bad, tot) if bad else "OK"))
                    if bad:
                        any_bad = True
                print("%3d %3d | %s" % (a0, c0, "  ".join(cells)))
        print("any obstruction in this pass:", any_bad)


if __name__ == "__main__":
    main()
