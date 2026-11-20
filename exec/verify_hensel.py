"""Independent verification of the valuation inequalities in G1_FREEZING.md 3.

Claims under test (G1:42-54):
  (I1)  v(dA) >= 6      for a = a0 mod 8
  (I2)  v(ddelta_tau) >= 6
  (I3)  v(dc^2) >= 4 (c0 odd) / 5 (c0 even)
  (I4)  v(dP) >= 6 > 2e = 4
  (I5)  v(d(dP/dy)) >= 6 > e = 2
  (I6)  128 mod-8 cells, one tau serves a cell
Everything is computed exactly (2-adic, 200 bits) at the cell centers and at random
perturbations inside each cell; plus a DIRECT existence test that does not go through Hensel:

        delta_tau (c^2 - A y^2) = 16   <=>   y^2 = (c^2 - 16/delta_tau)/A
"""
import random
from fractions import Fraction as Fr

from cells import build_cell, C0S, A0S
from padic import Q2


def vq(x):
    """valuation of a Q2, 'ZERO@k' when it vanishes to the tracked precision."""
    return x.val() if x.u else ">=%d" % (x.k + x.p)


def is_square_q2(x):
    """is x a square in Q2?  x = 2^k u (u odd): need k even and u = 1 mod 8."""
    if x.u == 0:
        return True, "zero"
    k, u = x.k, x.u % 8
    return (k % 2 == 0 and u == 1), "v=%d u=%d mod 8" % (k, u)


def perturb(cell, rng, maxk=9):
    """random point of the cell: a = a0 mod 8, c = c0 mod 8, tau = t_p mod 8."""
    a = cell["a0"] + 8 * rng.randrange(-2**maxk, 2**maxk)
    c = cell["c0"] + 8 * rng.randrange(-2**maxk, 2**maxk)
    tau = cell["tau"]
    return a, c, tau


def centre_and_perturbed(cell, n=12, seed=0):
    rng = random.Random(seed)
    A0 = cell["A0"]
    c0, tau = cell["c0"], cell["tau"]
    y_w = cell["y_w"]
    delta0 = cell["delta"]
    e = cell["e"]
    d0 = cell["dPdy"]
    out = {"a0": cell["a0"], "c0": c0, "tau": tau, "e": e, "v_y_w": cell["v_y_w"],
           "rows": [], "viol": []}
    for _ in range(n):
        a, c, tau = perturb(cell, rng)
        A = Q2.Z(1 + 4 * a * a)
        dtau = Q2.Z(1) - A * Q2.Z(tau * tau)
        dA = A - Q2.Z(A0)
        ddel = dtau - delta0
        dc2 = Q2.Z(c * c - c0 * c0)
        # (I4) the actual value of P at the perturbed parameter, keeping y = y_w, r=s=0
        f = dtau * (Q2.Z(c * c) - A * y_w * y_w) - Q2.Z(16)
        fp = Q2.Z(-2) * A * dtau * y_w            # dP/dy at the perturbed parameter
        row = {
            "a_mod8": a % 8, "c_mod8": c % 8, "a": a, "c": c,
            "v_dA": vq(dA), "v_ddel": vq(ddel), "v_dc2": vq(dc2),
            "v_P": vq(f), "v_dPdy_minus_d": vq(fp - d0),
            "v_dPdy": vq(fp),
        }
        # (I4)/(I5) as *stated*: v > 2e resp. v > e, with e from the centre
        row["I4_holds"] = (not f.u) or f.val() > 2 * e
        row["I5_holds"] = (not (fp - d0).u) or (fp - d0).val() > e
        # direct existence of a solution with y only (no Hensel):
        ys = (Q2.Z(c * c) - Q2.Z(16) * dtau.inv()) * A.inv()
        ok, why = is_square_q2(ys)
        row["y_exists"] = ok
        row["y_reason"] = why
        row["v_ysq"] = vq(ys)
        out["rows"].append(row)
        if not (row["I4_holds"] and row["I5_holds"]):
            out["viol"].append(row)
    return out


def main():
    cells = [build_cell(a0, c0) for a0 in A0S for c0 in C0S]
    print("cells: %d  (4 a-residues x 8 c-residues; b-residue does not enter r=s=0)" % len(cells))
    print()
    print("--- centre data ---")
    print("%3s %3s %4s %5s %5s %3s  %-8s %-8s %-8s %-8s" % (
        "a0", "c0", "A0", "tau", "v_y_w", "e", "v(delta)", "v(t_p)", "v(tau-t_p)", "v(del_tau)"))
    for c in cells:
        print("%3d %3d %4d %5d %5d %3d  %-8s %-8s %-8s %-8s" % (
            c["a0"], c["c0"], c["A0"], c["tau"], c["v_y_w"], c["e"], vq(c["delta"]),
            vq(c["tp"]), vq(c["tp"] - Q2.Z(c["tau"])), vq(Q2.Z(1) - Q2.Z(c["A0"]) * Q2.Z(c["tau"] ** 2))))

    print()
    print("--- inequalities over random perturbations of every cell ---")
    tot = 0
    i1 = i2 = i3 = i4 = i5 = yok = 0
    viol4 = viol5 = []
    worst = {}
    for c in cells:
        res = centre_and_perturbed(c, n=16, seed=1000 * c["a0"] + c["c0"])
        for row in res["rows"]:
            tot += 1
            i1 += _ge(row["v_dA"], 6)
            i2 += _ge(row["v_ddel"], 6)
            i3 += _ge(row["v_dc2"], 4)
            i4 += row["I4_holds"]
            i5 += row["I5_holds"]
            yok += row["y_exists"]
            if not row["I4_holds"]:
                viol4.append((c["a0"], c["c0"], row))
            if not row["I5_holds"]:
                viol5.append((c["a0"], c["c0"], row))
            # cheapest observed v(P) per cell
            v = row["v_P"]
            vv = 10 ** 6 if isinstance(v, str) else v
            if c["c0"] not in worst or vv < worst[c["c0"]][0]:
                worst[c["c0"]] = (vv, v, c["e"])
    print("perturbation points tested: %d" % tot)
    print("I1 v(dA)>=6            : %d/%d" % (i1, tot))
    print("I2 v(ddelta)>=6        : %d/%d" % (i2, tot))
    print("I3 v(dc^2)>=4          : %d/%d" % (i3, tot))
    print("I4 v(dP)>2e            : %d/%d   violations: %d" % (i4, tot, len(viol4)))
    print("I5 v(d(dP/dy))>e       : %d/%d   violations: %d" % (i5, tot, len(viol5)))
    print("direct: y solution exists (r=s=0): %d/%d" % (yok, tot))
    print()
    print("min v(P) per c0 class (min over sampled a in the class) vs 2e:")
    for c0 in C0S:
        vv, v, e = worst[c0]
        print("  c0=%d: min v(P)=%s   2e=%d   strict? %s" % (
            c0, v, 2 * e, "yes" if (isinstance(v, str) or v > 2 * e) else "NO (v(P) = 2e)"))
    if viol4:
        a0, c0, row = viol4[0]
        print()
        print("example I4 violation: a0=%d c0=%d a=%d c=%d  v(P)=%s  2e=%d" % (
            a0, c0, row["a"], row["c"], row["v_P"], 2 * cells[0]["e"]))


def _ge(v, n):
    if isinstance(v, str):
        return int(v[2:]) >= n
    return v >= n


if __name__ == "__main__":
    main()
