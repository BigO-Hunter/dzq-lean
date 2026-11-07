import Mathlib.Tactic

set_option maxRecDepth 20000

/-!
# Z2FORM.lean — the explicit exists-3 formula for Z_(2)

Artifact of lane `dzq-c1` (`G2_REDERIVATION.md` §1), machine-verified in Python there and in
lane `dzq-exec`.  The formula, exactly as written in the derivation doc:

    x ∈ Z_(2) ⟺ x = 0 ∨ ∃ x1 x2 x3 : Q,
      10 * x^2 * (7 + 5*x1 - 5*x1^2 - 2*x2^2 - 2*x2*x3 + 2*x3^2) - 1 = 0

Origin: Daans Lemma 4.1 with the S = {2} constants Q = (5,2)_Q, pi_4 = 10, a = 8, so
`O_{{2}} = {0} ∪ {x : Q_(8 - (10x^2)^{-1}) splits the quaternion}` (splitting made
existential by Daans Prop 3.6(iii) at A = 1, B = 2, c = 1), denominators cleared.
`zW` below is the bracket of the displayed equation, definitionally.

Kernel-checked here (the algebraic layer; see FORMAL_REPORT.md for the honest split):
well-definedness; equation ⟹ x ≠ 0; the substitution algebra to the unsimplified
Prop 3.6(iii) instance; the denominator-clearing lemma; witness certificates by `decide`.

Named gap (needs quaternion/valuation theory): `x ∈ Z_(2) ↔ Z2Def x` — the ⇐ direction
of Daans Lemma 4.1 is Hensel + parity (algebraic but p-adic), the ⇒ direction rests on
quaternion splitting (ABHN class).  See FORMAL_REPORT.md.
-/

/-- The bracket of the G2 formula (the simplified LHS inside the equation). -/
def zW (x1 x2 x3 : ℚ) : ℚ :=
  7 + 5 * x1 - 5 * x1 ^ 2 - 2 * x2 ^ 2 - 2 * x2 * x3 + 2 * x3 ^ 2

/-- The exists-3 formula for `Z_(2)`, verbatim from `G2_REDERIVATION.md` §1. -/
def Z2Def (x : ℚ) : Prop :=
  x = 0 ∨ ∃ x1 x2 x3 : ℚ, 10 * x ^ 2 * zW x1 x2 x3 - 1 = 0

/-- The equation part of the formula, isolated. -/
def Z2Eq (x x1 x2 x3 : ℚ) : Prop := 10 * x ^ 2 * zW x1 x2 x3 - 1 = 0

/-- The unsimplified Prop 3.6(iii) LHS at A = 1, B = 2, c = 1. -/
def zL (x1 x2 x3 : ℚ) : ℚ :=
  x1 ^ 2 + x1 * (1 - 2 * x1) - (1 - 2 * x1) ^ 2 - 2 * (x2 ^ 2 + x2 * x3 - x3 ^ 2)

/-- (a) The predicate is well-defined: it is definitionally the displayed disjunction. -/
theorem Z2Def_pred_eq (x : ℚ) :
    Z2Def x = (x = 0 ∨ ∃ x1 x2 x3 : ℚ, Z2Eq x x1 x2 x3) := rfl

/-- (b) The equation never holds at x = 0: the stratum x = 0 is exactly the left disjunct. -/
theorem Z2Eq_zero (x1 x2 x3 : ℚ) : ¬ Z2Eq 0 x1 x2 x3 := by
  simp [Z2Eq, zW]

/-- (b') Hence a point satisfying the equation is nonzero. -/
theorem Z2Eq_ne_zero {x x1 x2 x3 : ℚ} (h : Z2Eq x x1 x2 x3) : x ≠ 0 := by
  rintro rfl
  exact Z2Eq_zero x1 x2 x3 h

/-! ## The substitution algebra (Prop 3.6(iii) instance, A = 1, B = 2, c = 1) -/

/-- `zL + 8 = zW`: the simplified LHS of G2 equals the unsimplified Prop 3.6(iii) LHS
at A = 1, B = 2, c = 1 up to the constant 8. -/
theorem z2_lhs_bridge (x1 x2 x3 : ℚ) : zL x1 x2 x3 + 8 = zW x1 x2 x3 := by
  simp only [zL, zW]
  ring

/-- **Substitution theorem (cleared form).** For x ≠ 0, the G2 equation is equivalent to
`zL·(10x²) = 1 − 80x²`, i.e. to `zL = 1/(10x²) − 8` — the unsimplified Prop 3.6(iii)
instance at d = −(8 − (10x²)⁻¹).  Inverse-free, so every step is ring/linarith. -/
theorem z2_eq_prop36_cleared (x x1 x2 x3 : ℚ) (hx : x ≠ 0) :
    Z2Eq x x1 x2 x3 ↔ zL x1 x2 x3 * (10 * x ^ 2) = 1 - 80 * x ^ 2 := by
  constructor
  · intro h
    have hw : 10 * x ^ 2 * zW x1 x2 x3 = 1 := by
      simp only [Z2Eq] at h
      linarith
    have e0 : 10 * x ^ 2 * (zL x1 x2 x3 + 8) = 1 := by
      rw [z2_lhs_bridge]
      exact hw
    ring_nf at e0 ⊢
    linarith [e0]
  · intro h
    have hw : 10 * x ^ 2 * zW x1 x2 x3 - 1 = 0 := by
      rw [← z2_lhs_bridge]
      have e0 : 10 * x ^ 2 * (zL x1 x2 x3 + 8) = 1 := by
        ring_nf
        linarith [h]
      linarith [e0]
    exact hw

/-- **Substitution theorem.** For x ≠ 0, the cleared G2 equation is equivalent to the
unsimplified Prop 3.6(iii) instance with d = −(8 − (10x²)⁻¹) — the exact substitution
`c = 1, d = −(a − (10x²)^{-1}), A = 1, B = 2` claimed in `G2_REDERIVATION.md` §1. -/
theorem z2_eq_prop36 (x x1 x2 x3 : ℚ) (hx : x ≠ 0) :
    Z2Eq x x1 x2 x3 ↔ zL x1 x2 x3 = -(8 - 1 / (10 * x ^ 2)) := by
  have hx2 : (10:ℚ) * x ^ 2 ≠ 0 := mul_ne_zero (by norm_num) (pow_ne_zero 2 hx)
  have key := z2_eq_prop36_cleared x x1 x2 x3 hx
  constructor
  · intro h
    have h2 := key.mp h
    have h3 : zL x1 x2 x3 = (1 - 80 * x ^ 2) / (10 * x ^ 2) := by
      rw [← eq_div_iff hx2]
      exact h2
    have e : (1 - 80 * x ^ 2) / (10 * x ^ 2) = -(8 - 1 / (10 * x ^ 2)) := by
      field_simp
      all_goals ring
    rw [h3, e]
  · intro h
    have h3 : zL x1 x2 x3 * (10 * x ^ 2) = 1 - 80 * x ^ 2 := by
      rw [h]
      field_simp
      all_goals ring
    exact key.mpr h3

/-! ## Denominator clearing -/

/-- **Clearing lemma.**  For `A B P Q R S : Q` with `B ≠ 0, Q ≠ 0`, the equation
`Z2Eq (A/B) (P/Q) (R/Q) (S/Q)` is equivalent to the integer identity
`10 * A^2 * (7Q^2 + 5PQ - 5P^2 - 2R^2 - 2RS + 2S^2) = B^2 * Q^2`. -/
theorem z2_cleared (A B P Q R S : ℚ) (hB : B ≠ 0) (hQ : Q ≠ 0) :
    ((10 : ℚ) * (A / B) ^ 2 * zW (P / Q) (R / Q) (S / Q) - 1 = 0 ↔
      10 * A ^ 2 * (7 * Q ^ 2 + 5 * P * Q - 5 * P ^ 2 - 2 * R ^ 2 - 2 * R * S + 2 * S ^ 2)
        = B ^ 2 * Q ^ 2) := by
  constructor
  · intro h
    simp only [zW] at h
    field_simp at h ⊢
    linarith [h]
  · intro h
    simp only [zW]
    field_simp
    linarith [h]

/-! ## Witness certificates (kernel `decide` on the cleared identity) -/

/-- Witness: x = 1/5, (x1,x2,x3) = (1, 3/2, 0).  Cleared (Q = 2): both sides = 100. -/
theorem z2_wit_cleared_1_5 :
    (10:ℚ) * 1 ^ 2 * (7 * 2 ^ 2 + 5 * 2 * 2 - 5 * 2 ^ 2 - 2 * 3 ^ 2 - 2 * 3 * 0 + 2 * 0 ^ 2)
      = 5 ^ 2 * 2 ^ 2 := by norm_num

/-- Hence x = 1/5 ∈ Z_(2) satisfies the formula. -/
theorem z2_mem_one_fifth : Z2Def (1 / 5 : ℚ) := by
  refine Or.inr ⟨1, 3 / 2, 0, ?_⟩
  exact (z2_cleared 1 5 2 2 3 0 (by norm_num) (by norm_num)).mpr z2_wit_cleared_1_5

/-- Witness: x = 1, (x1,x2,x3) = (−3, −39/10, 24/5). -/
theorem z2_wit_cleared_1 :
    (10:ℚ) * 1 ^ 2 * (7 * 10 ^ 2 + 5 * (-30) * 10 - 5 * (-30) ^ 2 - 2 * (-39) ^ 2
      - 2 * (-39) * 48 + 2 * 48 ^ 2) = 1 ^ 2 * 10 ^ 2 := by norm_num

theorem z2_mem_one : Z2Def (1 : ℚ) := by
  refine Or.inr ⟨-3, -39 / 10, 24 / 5, ?_⟩
  exact (z2_cleared 1 1 (-30) 10 (-39) 48 (by norm_num) (by norm_num)).mpr z2_wit_cleared_1

/-- Witness: x = 3, (x1,x2,x3) = (−1, −19/30, −26/15). -/
theorem z2_wit_cleared_3 :
    (10:ℚ) * 3 ^ 2 * (7 * 30 ^ 2 + 5 * (-30) * 30 - 5 * (-30) ^ 2 - 2 * (-19) ^ 2
      - 2 * (-19) * (-52) + 2 * (-52) ^ 2) = 1 ^ 2 * 30 ^ 2 := by norm_num

theorem z2_mem_three : Z2Def (3 : ℚ) := by
  refine Or.inr ⟨-1, -19 / 30, -26 / 15, ?_⟩
  exact (z2_cleared 3 1 (-30) 30 (-19) (-52) (by norm_num) (by norm_num)).mpr z2_wit_cleared_3

/-- x = −3: the cleared identity is even in A, same witnesses. -/
theorem z2_mem_neg_three : Z2Def (-3 : ℚ) := by
  refine Or.inr ⟨-1, -19 / 30, -26 / 15, ?_⟩
  exact (z2_cleared (-3) 1 (-30) 30 (-19) (-52) (by norm_num) (by norm_num)).mpr
    z2_wit_cleared_3

/-- Witness: x = 1/3, (x1,x2,x3) = (−3, −21/5, 49/10). -/
theorem z2_wit_cleared_third :
    (10:ℚ) * 1 ^ 2 * (7 * 10 ^ 2 + 5 * (-30) * 10 - 5 * (-30) ^ 2 - 2 * (-42) ^ 2
      - 2 * (-42) * 49 + 2 * 49 ^ 2) = 3 ^ 2 * 10 ^ 2 := by norm_num

theorem z2_mem_third : Z2Def (1 / 3 : ℚ) := by
  refine Or.inr ⟨-3, -21 / 5, 49 / 10, ?_⟩
  exact (z2_cleared 1 3 (-30) 10 (-42) 49 (by norm_num) (by norm_num)).mpr
    z2_wit_cleared_third

/-- Witness: x = 2/3, (x1,x2,x3) = (−3/2, −27/20, 11/5). -/
theorem z2_wit_cleared_two_thirds :
    (10:ℚ) * 2 ^ 2 * (7 * 20 ^ 2 + 5 * (-30) * 20 - 5 * (-30) ^ 2 - 2 * (-27) ^ 2
      - 2 * (-27) * 44 + 2 * 44 ^ 2) = 3 ^ 2 * 20 ^ 2 := by norm_num

theorem z2_mem_two_thirds : Z2Def (2 / 3 : ℚ) := by
  refine Or.inr ⟨-3 / 2, -27 / 20, 11 / 5, ?_⟩
  exact (z2_cleared 2 3 (-30) 20 (-27) 44 (by norm_num) (by norm_num)).mpr
    z2_wit_cleared_two_thirds

/-- The x = 0 stratum. -/
theorem z2_mem_zero : Z2Def (0 : ℚ) := Or.inl rfl
