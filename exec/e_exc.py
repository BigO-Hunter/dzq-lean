"""E_exc exactly, under this lane's corrected freezing rule.

Sun (2026), Remark 5.1 / the paragraph before (5.11): for char != 2 the excluded finite set is

    E_exc = supp(pi)  u  {poles of the tau in Lambda}  u  {zeros of all pairwise differences
            among the four parameters attached to each i}  u  {places with |kappa_w| <= 25}

(S = {2} is already removed).  Two more things must hold at every place w outside it:
  * the four parameters of a class have pairwise distinct residues at w (that is what the
    "zeros of pairwise differences" exclusion buys), and
  * at least one of them has residue not in {0, +-1} (pigeonhole: 4 distinct residues, only 3
    forbidden values).

This file (a) fixes the local cover and the four parameters per class, (b) verifies each of the
eight parameters really serves its class at 2, and (c) computes the exclusion set exactly, plus a
direct scan of the residue conditions at every prime up to LIMIT.
"""
import itertools
import json

from solve_test import classify

# ---- local cover of P_2 --------------------------------------------------------------
# class A := {v_2(c) <= 2} = {c not = 0 mod 8};  served by tau = 1 mod 16
# class B := {v_2(c) >= 2} = {c = 0 mod 4};      served by tau = 3 mod 8
CLASS_A = [1, 17, 33, 49]
CLASS_B = [3, 11, 19, 27]
LAMBDA = CLASS_A + CLASS_B

LIMIT = 3000


def class_ok(tau, allow_c_mod8, M=9):
    """exhaustive over a = odd mod 2^M, c = c mod 8 in allow_c_mod8: does tau serve all of it?"""
    m = 1 << M
    bad = 0
    tot = 0
    for a in range(1, m, 2):
        for c in range(0, m):
            if c % 8 not in allow_c_mod8:
                continue
            tot += 1
            if not classify(a, 1, c, tau)[0]:
                bad += 1
    return bad, tot


def primes_dividing(n):
    n = abs(int(n))
    out = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def main():
    A_SET = set(range(1, 8))     # c not = 0 mod 8
    B_SET = {0, 4}               # c = 0 mod 4

    print("--- (a) the eight parameters serve their local class (exhaustive, a mod 2^9) ---")
    res = {"A": {}, "B": {}}
    for tau in CLASS_A:
        bad, tot = class_ok(tau, A_SET)
        res["A"][tau] = bad
        print("  class A  tau=%-3d  obstructed %d/%d" % (tau, bad, tot))
    for tau in CLASS_B:
        bad, tot = class_ok(tau, B_SET)
        res["B"][tau] = bad
        print("  class B  tau=%-3d  obstructed %d/%d" % (tau, bad, tot))
    served = all(v == 0 for v in res["A"].values()) and all(v == 0 for v in res["B"].values())
    print("  every parameter serves its class:", served)

    print()
    print("--- (b) E_exc from Sun's formula ---")
    supp_pi = primes_dividing(2)
    poles = set()
    for tau in LAMBDA:
        # tau is an integer -> no poles
        pass
    diffs = set()
    for x, y in itertools.combinations(LAMBDA, 2):
        diffs |= primes_dividing(abs(x - y))
    small = {p for p in range(2, 26) if all(p % q for q in range(2, p))}
    E = set()
    E |= (supp_pi - {2})
    E |= poles
    E |= (diffs - {2})
    E |= (small - {2})
    print("  supp(pi)                  = %s   (minus S = %s)" % (sorted(supp_pi), sorted(supp_pi - {2})))
    print("  poles of Lambda           = %s" % sorted(poles))
    print("  pairwise-difference primes= %s   (minus S = %s)" % (sorted(diffs), sorted(diffs - {2})))
    print("  places with |kappa_w|<=25 = %s   (minus S = %s)" % (sorted(small), sorted(small - {2})))
    print("  E_exc                     = %s   (|E_exc| = %d)" % (sorted(E), len(E)))
    print("  E_exc minus {2}           = %s" % sorted(E - {2}))

    print()
    print("--- (c) residue conditions at every prime w <= %d ---" % LIMIT)
    bad_w = []
    for w in range(2, LIMIT):
        if any(w % q == 0 for q in range(2, w)):
            continue
        if w == 2:
            continue
        for name, cls in (("A", CLASS_A), ("B", CLASS_B)):
            res_ = [t % w for t in cls]
            distinct = len(set(res_)) == 4
            good = any(r not in (0, 1, w - 1) for r in res_)
            if not (distinct and good) and w not in E:
                bad_w.append((w, name, res_, distinct, good))
    print("  primes where a class fails distinct-residue or {0,+-1}-escape AND w not in E_exc: %s"
          % (bad_w if bad_w else "none"))

    with open("e_exc.json", "w") as f:
        json.dump({"class_A": CLASS_A, "class_B": CLASS_B, "lambda": LAMBDA,
                   "supp_pi": sorted(supp_pi), "poles": sorted(poles),
                   "difference_primes": sorted(diffs), "small_primes": sorted(small),
                   "E_exc": sorted(E), "E_exc_count": len(E),
                   "serves_own_class": served,
                   "residue_failures_outside_E": bad_w}, f, indent=1, sort_keys=True)
    print()
    print("wrote e_exc.json")


if __name__ == "__main__":
    main()
