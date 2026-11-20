"""Emit the literal assembly: F_recipe.json (structural spec, every constant instantiated where
computed) and F_eval.py (the same polynomial as a self-contained straight-line evaluator).

F = (F_main * F_patch)^2 + (X*iota - 1)^2
F_main = F_Phi^2 + F_Theta^2
F_Theta = prod_{tau in Lambda} [ (delta_tau*zeta - 1)^2 + Phat_tau^2 + ((D*zeta' - 1)*P0_tau)^2 ]
F_patch = prod_{p in E_exc} F_p        (p = 2 literal; the others are the named blocker)
"""
import hashlib
import json

TAUS = [1, 3]     # verified local cover (VERIFICATION.md 4)
PI = 2
U = 1


def main():
    recipe = {
        "artifact": "literal 11-variable polynomial for Q \\ Z (Sun 2026 Thm 1.1, constructive folds)",
        "target": "X in Q : X not in Z  <=>  exists (a,b,b1,sigma,upsilon,y,r,s,zeta,zetap,iota) in Q^11: F = 0",
        "variables": [
            {"index": 0, "name": "X", "role": "the rational input"},
            {"index": 1, "name": "a", "role": "quaternion parameter (a - u in m_S)"},
            {"index": 2, "name": "b", "role": "quaternion parameter (b a unit on S)"},
            {"index": 3, "name": "y", "role": "Psi_tau witness (also patch witness)"},
            {"index": 4, "name": "r", "role": "Psi_tau witness"},
            {"index": 5, "name": "s", "role": "Psi_tau witness"},
            {"index": 6, "name": "zeta", "role": "delta_tau*zeta = 1 witness"},
            {"index": 7, "name": "zeta'", "role": "D*zeta' = 1 witness"},
            {"index": 8, "name": "b1", "role": "Phi: b*b1 - 1 = sigma*Pi_S"},
            {"index": 9, "name": "sigma", "role": "Phi"},
            {"index": 10, "name": "upsilon", "role": "Phi: a - u = upsilon*Pi_S"},
            {"index": 11, "name": "iota", "role": "X*iota = 1"},
        ],
        "constants": {
            "S": [2], "u": U, "pi": PI, "Pi_S": PI,
            "Lambda": TAUS,
            "Lambda_status": "2 tau values verified to serve every point of P_2 "
                             "(exhaustive over a full mod-2^10 grid; see VERIFICATION.md)",
            "E_exc": {
                "status": "NOT ENUMERATED -- named blocker",
                "contains_at_least": [3, 5, 7, 11, 13, 17, 19, 23],
                "why": "E_exc is the finite exceptional set of Sun Prop 9.1 (9.4); it is the primes "
                       "with residue field <= 25 (Lemma 5.1 needs q > 25), the poles of tau, and the "
                       "primes dividing tau, tau-1, tau+1 for the tau actually used, plus the primes "
                       "forced by the sections 7/8 target-place arguments",
            },
            "patch_p2": {"formula": "10*x^2*(7 + 5*x1 - 5*x1^2 - 2*x2^2 - 2*x2*x3 + 2*x3^2) - 1",
                         "meaning": "x in Z_(2) <=> x = 0 or exists x1,x2,x3: formula = 0",
                         "source": "G2_REDERIVATION.md 1, from Daans Prop 3.6(iii) with c=1, A=1, B=2, "
                                   "pi4=10, alpha=8"},
            "patch_other_primes": {"status": "NOT COMPUTED -- named blocker",
                                   "recipe": "same Lemma 4.1 / Prop 3.6(iii) template with per-prime "
                                             "constants (A_p, B_p, pi4_p, alpha_p) found by finite search"},
        },
        "formulas": {
            "A": "1 + 4*a^2",
            "z": "X^3",
            "G": "16*a^4*b^2 - (b-1)^4*(1+4*a^2)",
            "N": "a^2*z^2*G",
            "D": "(1+4*a^2)*b^2*(1 - z - a^2*z^2)",
            "B": "b*pi = 2*b",
            "delta_tau": "1 - A*tau^2",
            "Phat_tau": "delta_tau*(N^2 - A*y^2*D^2) - 16*B*(r^2 - A*s^2)*D^2 - 16*D^2",
            "P0_tau": "-delta_tau*A*y^2 - 16*B*(r^2 - A*s^2) - 16",
            "F_Phi": "(b*b1 - 1 - sigma*Pi_S)^2 + (a - u - upsilon*Pi_S)^2",
            "F_Theta": "prod over tau in Lambda of [(delta_tau*zeta - 1)^2 + Phat_tau^2 + ((D*zeta' - 1)*P0_tau)^2]",
            "F_main": "F_Phi^2 + F_Theta^2",
            "F_patch": "prod over p in E_exc of F_p",
            "F": "(F_main * F_patch)^2 + (X*iota - 1)^2",
        },
        "fold_justification": {
            "E1": "over Q (ordered), f = 0 and g = 0 <=> f^2 + g^2 = 0",
            "E2": "f*g = 0 <=> f = 0 or g = 0 (union by padded product; witnesses shared)",
            "E3": "the product over Lambda realises the disjunction; zeta kills delta_tau = 0, "
                  "zeta' the D = 0 case",
            "E4": "X*iota = 1 forces X != 0 (0^{-1} = 0 would otherwise admit X = 0)",
        },
        "degrees": {
            "Phat_tau": {"X": 12, "a": 14, "b": 8, "y": 2, "r": 2, "s": 2},
            "theta_factor": {"X": 24, "a": 28, "b": 16, "y": 4, "r": 4, "s": 4, "zeta": 2, "zeta'": 2},
        },
        "term_counts_measured": {},   # filled below
        "expansion_status": {
            "per_branch_term_lists": "emitted: phi, Phat_tau1/3, P0_tau1/3, thetafac_tau1/3, patch2",
            "F_Theta": "product of |Lambda| = 2 factors of 2022 and 2347 terms -> ~4.7e6 terms "
                       "before cancellation (measured factor sizes)",
            "F": "F_main^2 and (F_main*F_patch)^2 push the expanded size past 1e13 terms; "
                 "the expanded term list is NOT producible",
            "consequence": "the polynomial is literal as a straight-line program (F_eval.py) and "
                           "literal leaf-by-leaf as sparse term lists; the top-level product is "
                           "left as a product",
        },
    }
    try:
        with open("branches.json") as f:
            br = json.load(f)
        recipe["term_counts_measured"] = br
    except FileNotFoundError:
        pass

    data = json.dumps(recipe, indent=1, sort_keys=True)
    with open("F_recipe.json", "w") as f:
        f.write(data + "\n")
    print("F_recipe.json sha256 =", hashlib.sha256((data + "\n").encode()).hexdigest())
    print("Lambda =", TAUS)


if __name__ == "__main__":
    main()
