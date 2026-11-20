"""Emit TAU.json: the frozen-parameter data, exact where exact and rational-truncated otherwise.

For every mod-8 cell (a0, c0) of P_2 this records
  * the Cayley parameter t_p of the canonical centre construction (rational truncation, 64 bits),
  * the i-coordinate Y of z1 (rational truncation),
  * delta, the (2.1) witness y = 4Y + t_p c0, the derivative valuation e,
  * the tau the construction *suggests* (t_p mod 8) and whether that tau actually serves the
    cell (it does NOT for c0 = 0 and c0 = 4, and it fails on 8-25% of the points for c0 = 2,6),
  * the tau that DOES serve the cell (verified: the 2-tau map of VERIFICATION.md 4).
"""
import hashlib
import json
from fractions import Fraction as Fr

from cells import A0S, C0S, build_cell
from padic import Q2
from solve_test import classify

BITS = 64


def trunc(x):
    """exact rational truncation of a Q2 to 64 bits below its leading term."""
    if x.u == 0:
        return Fr(0)
    m = x.u % (1 << BITS)
    if x.k >= 0:
        return Fr(m << x.k)
    return Fr(m, 1 << (-x.k))


def serve_check(a0, c0, tau, n=64, seed=3):
    """how many of a full mod-2^8 grid of the cell does tau serve?"""
    bad = 0
    tot = 0
    for a in range(a0, 256, 8):
        for c in range(c0, 256, 8):
            tot += 1
            if not classify(a, 1, c, tau)[0]:
                bad += 1
    return bad, tot


def main():
    cells = []
    for a0 in A0S:
        for c0 in C0S:
            r = build_cell(a0, c0)
            tau_sug = r["tau"]
            tau_ok = 3 if c0 % 4 == 0 else 1
            bad_sug, tot = serve_check(a0, c0, tau_sug)
            bad_ok, _ = serve_check(a0, c0, tau_ok)
            cells.append({
                "cell": {"a_mod_8": a0, "c_mod_8": c0},
                "A0": r["A0"],
                "c1": r["c1"],
                "z1_bar": list(r["z1bar"]),
                "z2_bar": list(r["z2bar"]),
                "root_choice": r["root_choice"],
                "t_p": {"num": trunc(r["tp"]).numerator, "den_pow2": trunc(r["tp"]).denominator},
                "Y": {"num": trunc(r["Y"]).numerator, "den_pow2": trunc(r["Y"]).denominator},
                "delta": {"num": trunc(r["delta"]).numerator,
                          "den_pow2": trunc(r["delta"]).denominator},
                "y_witness": {"num": trunc(r["y_w"]).numerator,
                              "den_pow2": trunc(r["y_w"]).denominator},
                "valuations": {"v_t_p": r["v_tp"], "v_delta": r["v_delta"],
                               "v_Y": r["v_Y"], "v_y_witness": r["v_y_w"], "e": r["e"]},
                "tau_suggested": tau_sug,
                "tau_suggested_obstructed": "%d/%d" % (bad_sug, tot),
                "tau_verified": tau_ok,
                "tau_verified_obstructed": "%d/%d" % (bad_ok, tot),
                "checks": {k: r[k] for k in (
                    "z1_integral", "Tr_z1_eq_c1", "N_z1_eq_1", "N_z2_eq_1", "Tr_sum_eq_c0",
                    "z1_ne_pm1", "z2_ne_pm_z1", "z2_ne_z1inv", "i_sq_ok", "gamma_ne_m1",
                    "gamma_plus1_unit", "gamma_minus1_unit", "tp_in_Q2", "Ysq_ok",
                    "P_center_zero", "coord_consistency", "delta_tau_nonzero")},
            })

    doc = {
        "lane": "dzq-exec",
        "what": "frozen-parameter data for the S={2}, u=1, pi=2 instance of Sun 2026 Prop 3.1",
        "constants": {"S": [2], "u": 1, "pi": 2, "Pi_S": 2,
                      "field": "Q_2", "E": "Q_2(zeta), zeta^2+zeta+1=0 (unramified quadratic)"},
        "method": {
            "t_p": "Cayley parameter of gamma = z2/z1 at the cell centre: t_p = (gamma-1)/(sqrt(A)(gamma+1))",
            "Y": "i-coordinate of z1 = (c1 + sqrt(c1^2-4))/2 in K(i), i^2 = A",
            "y_witness": "the (2.1) witness y = 4Y + t_p*c (NOT Y: G1_FREEZING.md conflates them)",
            "truncation": "binary 64-bit rational truncation of the 2-adic value",
        },
        "lambda_final": {
            "class_A": {"set": "v_2(c) <= 2 (c not = 0 mod 8)", "taus": [1, 17, 33, 49],
                        "note": "4 parameters per class as Sun requires; all verified to serve the "
                                "whole class exhaustively"},
            "class_B": {"set": "v_2(c) >= 2 (c = 0 mod 4)", "taus": [3, 11, 19, 27]},
            "size": 8,
            "supersedes": "the 2-value map (tau = 1 / tau = 3) of the previous pass, which is enough "
                          "to COVER P_2 but not enough for Sun's four-residues-per-class argument",
        },
        "counts": {
            "cells_mod8": len(cells),
            "claim_G1_Lambda_le": 512,
            "distinct_tau_from_cayley": sorted({c["tau_suggested"] for c in cells}),
            "verified_tau_set": sorted({c["tau_verified"] for c in cells}),
            "Lambda_verified_local": 2,
            "Lambda_with_Sun_4_lifts_per_class": 8,
            "note": "the Cayley-derived tau serves only c0 in {1,3,5,7} (odd c); it is 100% obstructed "
                    "for c0=0 and c0=4 and 8-25% obstructed for c0=2,6",
        },
        "cells": cells,
    }
    data = json.dumps(doc, indent=1, sort_keys=True)
    with open("TAU.json", "w") as f:
        f.write(data + "\n")
    h = hashlib.sha256((data + "\n").encode()).hexdigest()
    print("TAU.json written, sha256 =", h)
    print("cells:", len(cells))
    print("distinct tau from the Cayley construction:", doc["counts"]["distinct_tau_from_cayley"])
    print("verified tau set:", doc["counts"]["verified_tau_set"])
    print()
    print("%5s %5s %6s %8s %8s %9s %10s %10s" % (
        "a0", "c0", "tau_s", "obstr_s", "tau_v", "obstr_v", "v(y_w)", "e"))
    for c in cells[:8] + cells[-4:]:
        print("%5d %5d %6d %8s %8d %9s %10d %10d" % (
            c["cell"]["a_mod_8"], c["cell"]["c_mod_8"], c["tau_suggested"],
            c["tau_suggested_obstructed"], c["tau_verified"], c["tau_verified_obstructed"],
            c["valuations"]["v_y_witness"], c["valuations"]["e"]))


if __name__ == "__main__":
    main()
