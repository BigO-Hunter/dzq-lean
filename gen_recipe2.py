"""Rewrite F_recipe.json for the COMPLETE assembly: 8 frozen parameters, 8 patch primes,
every constant instantiated.
"""
import hashlib
import json

from F_eval import E_EXC, LAMBDA, PATCH

PI, U = 2, 1
CLASS_A = [1, 17, 33, 49]
CLASS_B = [3, 11, 19, 27]


def main():
    with open("branches2.json") as f:
        br = json.load(f)
    with open("perprime.json") as f:
        pp = json.load(f)
    with open("e_exc.json") as f:
        ee = json.load(f)

    recipe = {
        "artifact": "literal 11-variable polynomial defining Q \\ Z (Sun 2026 Thm 1.1, constructive folds)",
        "target": "X in Q : X not in Z  <=>  exists (a,b,b1,sigma,upsilon,y,r,s,zeta,zetap,iota) in Q^11: F = 0",
        "variables": [
            {"index": 0, "name": "X", "role": "rational input"},
            {"index": 1, "name": "a", "role": "quaternion parameter (a - u in m_S)"},
            {"index": 2, "name": "b", "role": "quaternion parameter (b a unit on S)"},
            {"index": 3, "name": "y", "role": "Psi_tau witness; also patch witness s1"},
            {"index": 4, "name": "r", "role": "Psi_tau witness; patch witness s2"},
            {"index": 5, "name": "s", "role": "Psi_tau witness; patch witness s3"},
            {"index": 6, "name": "zeta", "role": "delta_tau*zeta = 1"},
            {"index": 7, "name": "zeta'", "role": "D*zeta' = 1"},
            {"index": 8, "name": "b1", "role": "Phi: b*b1 - 1 = sigma*Pi_S"},
            {"index": 9, "name": "sigma", "role": "Phi"},
            {"index": 10, "name": "upsilon", "role": "Phi: a - u = upsilon*Pi_S"},
            {"index": 11, "name": "iota", "role": "X*iota = 1"},
        ],
        "constants": {
            "S": [2], "u": U, "pi": PI, "Pi_S": PI,
            "Lambda": list(LAMBDA),
            "Lambda_structure": {
                "class_A": {"set": "v_2(c) <= 2  (c not = 0 mod 8)", "taus": CLASS_A,
                            "why": "all four verified (exhaustive, a mod 2^9) to make Psi_tau "
                                   "solvable at every point of the class"},
                "class_B": {"set": "v_2(c) >= 2  (c = 0 mod 4)", "taus": CLASS_B,
                            "why": "same, exhaustive"},
                "four_per_class": "Sun's requirement: at each place outside E_exc four parameters "
                                 "have pairwise distinct residues, so at least one escapes {0,+-1}",
            },
            "E_exc": {"value": list(E_EXC), "count": len(E_EXC),
                      "derivation": ee,
                      "note": "all eight are forced by |kappa_w| <= 25 (Lemma 5.1 needs q > 25); the "
                              "tau-divisor and pairwise-difference contributions add only {2,3}, "
                              "already forced -- so the bound does not grow with Lambda"},
            "patch_constants": {str(p): {"pi": pi_p, "A": A_p, "B": B_p, "a": a_p,
                                         "q": pp[str(p)]["q"], "d": pp[str(p)]["d"],
                                         "Delta": pp[str(p)]["Delta"]}
                                for (p, pi_p, A_p, B_p, a_p) in PATCH},
            "patch_p2_control": {"constants": {k: pp["2"][k] for k in ("A", "B", "a", "q", "d", "pi")},
                                 "in_patch": False,
                                 "why": "E_exc is a subset of V_K minus S and S = {2}; m_2 lies inside "
                                        "Z_(2), so a p = 2 factor would wrongly admit even integers. "
                                        "The p = 2 constants pass the same hypothesis checker and "
                                        "are kept only as a control arm."},
            "patch_constant_term_note": "F_p = pi_p X^2 G_p - p^2.  The argument of the O_(p) formula "
                                        "is X/p because m_p = p*O_p, so the cleared constant term is "
                                        "p^2 (an earlier draft of this lane used -1, which defines "
                                        "Z_(p) rather than m_p; corrected here).",
        },
        "formulas": {
            "A": "1 + 4*a^2", "z": "X^3",
            "G": "16*a^4*b^2 - (b-1)^4*(1+4*a^2)",
            "N": "a^2*z^2*G", "D": "(1+4*a^2)*b^2*(1 - z - a^2*z^2)", "B": "b*pi = 2*b",
            "delta_tau": "1 - A*tau^2",
            "Phat_tau": "delta_tau*(N^2 - A*y^2*D^2) - 16*B*(r^2 - A*s^2)*D^2 - 16*D^2",
            "P0_tau": "-delta_tau*A*y^2 - 16*B*(r^2 - A*s^2) - 16",
            "F_Phi": "(b*b1 - 1 - sigma*Pi_S)^2 + (a - u - upsilon*Pi_S)^2",
            "F_Theta": "prod over tau in Lambda of [(delta_tau*zeta - 1)^2 + Phat_tau^2 + ((D*zeta' - 1)*P0_tau)^2]",
            "F_main": "F_Phi^2 + F_Theta^2",
            "F_p": "pi_p*X^2*((1+4A_p)(s1 - s1^2) + (a_p - A_p) - B_p*(s2^2 + s2*s3 - A_p*s3^2)) - p^2  [p in E_exc, odd]",
            "F_patch": "prod over p in E_exc of F_p   (witnesses s1,s2,s3 = y,r,s shared)",
            "F": "(F_main * F_patch)^2 + (X*iota - 1)^2",
        },
        "fold_justification": {
            "E1": "over Q (ordered), f = 0 and g = 0 <=> f^2 + g^2 = 0",
            "E2": "f*g = 0 <=> f = 0 or g = 0 (union by padded product; witnesses shared)",
            "E3": "product over Lambda realises the disjunction; zeta kills delta_tau = 0, zeta' the D = 0 case",
            "E4": "X*iota = 1 forces X != 0",
        },
        "term_counts_measured": br,
        "expansion_status": {
            "literal": "every constant, every leaf factor, as a hashed sparse term list; the whole F "
                       "as a straight-line program (F_eval.py), verified equal to the leaves",
            "F_Theta": "product of 8 factors of %s terms" % sorted(
                {v["terms"] for k, v in br["objects"].items() if k.startswith("thetafac")}),
            "F_patch": "product of 8 factors of 7 terms each",
            "F": "F_main^2 and (F_main*F_patch)^2 put the expanded single term list past 1e13 terms; "
                 "expansion remains infeasible and is not attempted",
        },
    }
    data = json.dumps(recipe, indent=1, sort_keys=True)
    with open("F_recipe.json", "w") as f:
        f.write(data + "\n")
    print("F_recipe.json rewritten, sha256 =", hashlib.sha256((data + "\n").encode()).hexdigest())
    print("Lambda =", LAMBDA)
    print("E_exc  =", E_EXC, "(%d primes)" % len(E_EXC))


if __name__ == "__main__":
    main()
