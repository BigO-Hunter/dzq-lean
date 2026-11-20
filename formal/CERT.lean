import Z2FORM
import LEAVES

set_option maxRecDepth 20000

/-!
# CERT.lean — assembly of the 11-variable F from the 34 leaves + axiom audit

`F_recipe.json` / `F_eval.py` (lane dzq-exec) define the polynomial as the straight-line
program

    F = (F_main * F_patch)^2 + (X*iota - 1)^2,
    F_main  = F_Phi^2 + F_Theta^2,
    F_Theta = prod_{tau in Lambda} thetafac_tau,   Lambda = (1,17,33,49,3,11,19,27),
    F_patch = prod_{p in E_exc ∪ {2}} F_p,         E_exc = (3,5,7,11,13,17,19,23),

with `z = iota^3` inside N and D.  Here the PRODUCT-OF-EMITTED-LEAVES representation is
proved equal to the COMPACT-RECIPE representation:

  * per-leaf:  `*_match` (in LEAVES.lean) — recipe formula = sha-pinned term list, by `ring`;
  * assembly:  `F_Theta_bridge`, `F_patch_bridge`, `F_assembly` — the product structure
    matches the recipe composition;
  * samples:   kernel `decide` evaluations of BOTH representations at integer points
    (34 leaves x 12 points in LEAVES.lean, mirroring the F_eval.py 408-check selftest,
    restricted to denominator-1 points; plus whole-F spot checks here).

The target theorem — `F = 0` has a rational solution iff `X ∉ Z` — is the Sun 2026 /
Daans bridge theorem; it is NOT claimed here (named gap, see FORMAL_REPORT.md).
-/

/-- F_Theta as a product of the 8 emitted thetafac term lists (Lambda order). -/
def F_Theta_prod (v : Fin 12 → ℤ) : ℤ :=
  thetafac_tau1_T v * thetafac_tau17_T v * thetafac_tau33_T v * thetafac_tau49_T v
    * thetafac_tau3_T v * thetafac_tau11_T v * thetafac_tau19_T v * thetafac_tau27_T v

/-- F_Theta in compact recipe form. -/
def F_Theta_c (v : Fin 12 → ℤ) : ℤ :=
  Vthetafac v 1 * Vthetafac v 17 * Vthetafac v 33 * Vthetafac v 49
    * Vthetafac v 3 * Vthetafac v 11 * Vthetafac v 19 * Vthetafac v 27

/-- F_patch as a product of the 9 emitted patch term lists (2 and E_exc). -/
def F_patch_prod (v : Fin 12 → ℤ) : ℤ :=
  patch_p2_T v * patch_p3_T v * patch_p5_T v * patch_p7_T v * patch_p11_T v
    * patch_p13_T v * patch_p17_T v * patch_p19_T v * patch_p23_T v

/-- F_patch in compact recipe form (constants from F_eval.py's PATCH table). -/
def F_patch_c (v : Fin 12 → ℤ) : ℤ :=
  Vpatch v 2 6 (-1) 2 4 * Vpatch v 3 15 1 (-3) 3 * Vpatch v 5 15 (-1) 5 7
    * Vpatch v 7 35 1 (-7) 9 * Vpatch v 11 33 (-1) 11 1 * Vpatch v 13 65 1 (-13) 4
    * Vpatch v 17 51 (-1) 17 13 * Vpatch v 19 133 (-2) 19 1 * Vpatch v 23 69 (-1) 23 7

/-- F_main in compact recipe form. -/
def F_main_c (v : Fin 12 → ℤ) : ℤ := Vphi v ^ 2 + F_Theta_c v ^ 2

/-- F_main as a product of emitted leaves. -/
def F_main_prod (v : Fin 12 → ℤ) : ℤ := phi_T v ^ 2 + F_Theta_prod v ^ 2

/-- The full polynomial F, straight-line-program form (compact recipe). -/
def F_slp (v : Fin 12 → ℤ) : ℤ :=
  (F_main_c v * F_patch_c v) ^ 2 + (v 0 * v 11 - 1) ^ 2

/-- The full polynomial F, assembled from the emitted leaf term lists. -/
def F_prod_assembled (v : Fin 12 → ℤ) : ℤ :=
  (F_main_prod v * F_patch_prod v) ^ 2 + (v 0 * v 11 - 1) ^ 2

/-! ## The assembly theorems -/

/-- The product of the 8 emitted thetafac term lists equals the compact F_Theta. -/
theorem F_Theta_bridge : ∀ v : Fin 12 → ℤ, F_Theta_prod v = F_Theta_c v := by
  intro v
  rw [← thetafac_tau1_match, ← thetafac_tau17_match, ← thetafac_tau33_match,
    ← thetafac_tau49_match, ← thetafac_tau3_match, ← thetafac_tau11_match,
    ← thetafac_tau19_match, ← thetafac_tau27_match]

/-- The product of the 9 emitted patch term lists equals the compact F_patch. -/
theorem F_patch_bridge : ∀ v : Fin 12 → ℤ, F_patch_prod v = F_patch_c v := by
  intro v
  rw [← patch_p2_match, ← patch_p3_match, ← patch_p5_match, ← patch_p7_match,
    ← patch_p11_match, ← patch_p13_match, ← patch_p17_match, ← patch_p19_match,
    ← patch_p23_match]

/-- F_main: emitted leaves vs compact recipe. -/
theorem F_main_bridge : ∀ v : Fin 12 → ℤ, F_main_prod v = F_main_c v := by
  intro v
  rw [F_Theta_bridge, ← phi_match]

/-- **Assembly theorem.** The polynomial assembled from the 34 sha-pinned leaf term lists
equals the straight-line-program polynomial of `F_recipe.json` / `F_eval.py`, at every
integer assignment of the 12 variables. -/
theorem F_assembly : ∀ v : Fin 12 → ℤ, F_prod_assembled v = F_slp v := by
  intro v
  rw [F_main_bridge, F_patch_bridge]

/-! ## Whole-F kernel spot checks at integer sample points -/

set_option maxHeartbeats 4000000 in
example : F_prod_assembled (pt 1) = F_slp (pt 1) := by decide

set_option maxHeartbeats 4000000 in
example : F_prod_assembled (pt 4) = F_slp (pt 4) := by decide

set_option maxHeartbeats 4000000 in
example : F_prod_assembled (pt 8) = F_slp (pt 8) := by decide

/-! ## Axiom audit

Every named theorem must rest on `[propext, Classical.choice, Quot.sound]` only
(no `sorryAx`, no `Lean.ofReduceBool` — hence no `native_decide` anywhere). -/

#print axioms Z2Def_pred_eq
#print axioms Z2Eq_zero
#print axioms Z2Eq_ne_zero
#print axioms z2_lhs_bridge
#print axioms z2_eq_prop36
#print axioms z2_cleared
#print axioms z2_wit_cleared_1_5
#print axioms z2_mem_one_fifth
#print axioms z2_wit_cleared_1
#print axioms z2_mem_one
#print axioms z2_wit_cleared_3
#print axioms z2_mem_three
#print axioms z2_mem_neg_three
#print axioms z2_wit_cleared_third
#print axioms z2_mem_third
#print axioms z2_wit_cleared_two_thirds
#print axioms z2_mem_two_thirds
#print axioms z2_mem_zero
#print axioms P0_tau1_match
#print axioms P0_tau3_match
#print axioms P0_tau11_match
#print axioms P0_tau17_match
#print axioms P0_tau19_match
#print axioms P0_tau27_match
#print axioms P0_tau33_match
#print axioms P0_tau49_match
#print axioms Phat_tau1_match
#print axioms Phat_tau3_match
#print axioms Phat_tau11_match
#print axioms Phat_tau17_match
#print axioms Phat_tau19_match
#print axioms Phat_tau27_match
#print axioms Phat_tau33_match
#print axioms Phat_tau49_match
#print axioms thetafac_tau1_match
#print axioms thetafac_tau3_match
#print axioms thetafac_tau11_match
#print axioms thetafac_tau17_match
#print axioms thetafac_tau19_match
#print axioms thetafac_tau27_match
#print axioms thetafac_tau33_match
#print axioms thetafac_tau49_match
#print axioms patch_p2_match
#print axioms patch_p3_match
#print axioms patch_p5_match
#print axioms patch_p7_match
#print axioms patch_p11_match
#print axioms patch_p13_match
#print axioms patch_p17_match
#print axioms patch_p19_match
#print axioms patch_p23_match
#print axioms phi_match
#print axioms F_Theta_bridge
#print axioms F_patch_bridge
#print axioms F_main_bridge
#print axioms F_assembly
