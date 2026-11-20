"""One consolidated measurement pass: every number quoted in VERIFICATION.md.

Writes measurements.json and prints the tables.
"""
import json
import random
from fractions import Fraction as Fr

from cells import A0S, C0S, build_cell
from padic import Q2
from solve_test import classify

TAUSU = {1: 3, 3: 1, 5: 3, 7: 1}  # not used; kept out of the way


def v_of(x):
    return None if x.u == 0 else x.k


def main():
    cells = [build_cell(a0, c0) for a0 in A0S for c0 in C0S]
    rng = random.Random(4242)
    out = {"centre": [], "perturb": {}}
    # ---- centre data
    for c in cells:
        out["centre"].append({
            "a0": c["a0"], "c0": c["c0"], "A0": c["A0"], "c1": c["c1"], "tau_cayley": c["tau"],
            "v_tp": c["v_tp"], "v_delta": c["v_delta"], "v_Y": c["v_Y"],
            "v_y_witness": c["v_y_w"], "e": c["e"],
            "all_checks_pass": all(c[k] for k in (
                "z1_integral", "Tr_z1_eq_c1", "N_z1_eq_1", "N_z2_eq_1", "Tr_sum_eq_c0",
                "z1_ne_pm1", "z2_ne_pm_z1", "z2_ne_z1inv", "i_sq_ok", "gamma_ne_m1",
                "gamma_plus1_unit", "gamma_minus1_unit", "tp_in_Q2", "Ysq_ok",
                "P_center_zero", "coord_consistency", "delta_tau_nonzero")),
        })
    print("centre data: %d cells, checks all pass: %s" % (
        len(cells), all(c["all_checks_pass"] for c in out["centre"])))
    print("  v(Y) values      :", sorted({c["v_Y"] for c in out["centre"]}))
    print("  v(y_witness)     :", sorted({c["v_y_witness"] for c in out["centre"]}))
    print("  e values         :", sorted({c["e"] for c in out["centre"]}))
    print("  v(delta)         :", sorted({c["v_delta"] for c in out["centre"]}))
    print("  v(t_p)           :", sorted({c["v_tp"] for c in out["centre"]}))

    # ---- perturbation measurements (400 points per cell)
    agg = {"v_dA": [], "v_ddelta": [], "v_dc2": [], "v_dP": [], "v_ddPdy": [], "e": [],
           "I4": [0, 0], "I5_holds_true_ineq": [0, 0], "I5_as_stated_ge6": [0, 0]}
    for c in cells:
        a0, c0, tau = c["a0"], c["c0"], c["tau"]
        A0, y_w, delta0, e = c["A0"], c["y_w"], c["delta"], c["e"]
        d0 = c["dPdy"]
        for _ in range(400):
            a = a0 + 8 * rng.randrange(-256, 256)
            cc = c0 + 8 * rng.randrange(-256, 256)
            A = Q2.Z(1 + 4 * a * a)
            dtau = Q2.Z(1) - A * Q2.Z(tau * tau)
            dA = A - Q2.Z(A0)
            ddel = dtau - delta0
            dc2 = Q2.Z(cc * cc - c0 * c0)
            f = dtau * (Q2.Z(cc * cc) - A * y_w * y_w) - Q2.Z(16)
            fp = Q2.Z(-2) * A * dtau * y_w
            for key, val in (("v_dA", dA), ("v_ddelta", ddel), ("v_dc2", dc2),
                             ("v_dP", f), ("v_ddPdy", fp - d0)):
                v = v_of(val)
                if v is not None:
                    agg[key].append(v)
            agg["e"].append(e)
            agg["I4"][1] += 1
            if f.u == 0 or f.k > 2 * e:
                agg["I4"][0] += 1
            agg["I5_holds_true_ineq"][1] += 1
            if (fp - d0).u == 0 or (fp - d0).k > e:
                agg["I5_holds_true_ineq"][0] += 1
            agg["I5_as_stated_ge6"][1] += 1
            if (fp - d0).u == 0 or (fp - d0).k >= 6:
                agg["I5_as_stated_ge6"][0] += 1
    print()
    print("perturbations: %d points" % agg["I4"][1])
    for key in ("v_dA", "v_ddelta", "v_dc2", "v_dP", "v_ddPdy"):
        print("  min %-10s = %s   (distribution: %s)" % (
            key, min(agg[key]), sorted({v: agg[key].count(v) for v in set(agg[key])}.items())[:6]))
    print("  I4  v(dP) > 2e          : %d/%d" % tuple(agg["I4"]))
    print("  I5  v(ddPdy) > e (needed): %d/%d" % tuple(agg["I5_holds_true_ineq"]))
    print("  I5' v(ddPdy) >= 6 (stated): %d/%d" % tuple(agg["I5_as_stated_ge6"]))
    out["perturb"] = {k: (v if not isinstance(v, list) else
                          {"min": min(v) if v else None, "max": max(v) if v else None,
                           "n": len(v), "hist": sorted({x: v.count(x) for x in set(v)}.items())[:12]})
                      for k, v in agg.items()}

    # ---- the decisive counterexample, with a rigorous no-solution proof at K=10/12
    from brute_check import necessary_y_search
    ex = []
    for (a, cc) in ((145, -208), (-415, -368), (233, -400)):
        for tau in (1, 3):
            ok, why, det = classify(a, 1, cc, tau)
            nmax = None
            if not ok:
                g10 = necessary_y_search(a, 1, cc, tau, 10)
                g12 = necessary_y_search(a, 1, cc, tau, 12)
                nmax = (len(g10), len(g12))
            ex.append({"a": a, "c": cc, "tau": tau, "solvable": ok, "why": why, "detail": det,
                       "admissible_y_mod_2_10_2_12": nmax})
    print()
    print("counterexample battery (a, c, tau) -> solvable?  adversarial y-search:")
    for e_ in ex:
        print("  a=%-5d c=%-5d tau=%d  %-8s %s  %s" % (
            e_["a"], e_["c"], e_["tau"], e_["solvable"], e_["detail"],
            ("admissible y: K=10: %d, K=12: %d" % e_["admissible_y_mod_2_10_2_12"])
            if e_["admissible_y_mod_2_10_2_12"] else ""))
    out["counterexamples"] = ex

    # ---- coverage numbers
    tot = bad_cayley = bad_fixed = 0
    for a0 in A0S:
        for c0 in C0S:
            c = build_cell(a0, c0)
            tau_ok = 3 if c0 % 4 == 0 else 1
            for a in range(a0, 1024, 8):
                for cc in range(c0, 1024, 8):
                    tot += 1
                    if not classify(a, 1, cc, c["tau"])[0]:
                        bad_cayley += 1
                    if not classify(a, 1, cc, tau_ok)[0]:
                        bad_fixed += 1
    print()
    print("full grid mod 2^10 (%d points): cayley tau obstructed %d, verified 2-tau map obstructed %d"
          % (tot, bad_cayley, bad_fixed))
    out["coverage"] = {"points": tot, "obstructed_cayley_tau": bad_cayley,
                       "obstructed_tau_map": bad_fixed}
    with open("measurements.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("measurements.json written")


if __name__ == "__main__":
    main()
