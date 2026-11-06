/-
Probe file: every lemma name we intend to cite in GAP_LIST.md / CERTIFIABILITY.md
is #check'd here. Lines that error = the API does NOT exist. Nothing is
asserted unless this file compiles clean.
-/
import Mathlib

-- ===== Rat / Int coercion API (needed for the SCORING FORM: q.den = 1) =====
#check @Rat.den
#check @Rat.num
#check @Rat.den_pos
#check @Rat.den_eq_one_iff
#check @Rat.num_den
#check @Rat.num_div_den
#check @Rat.isInt
#check @Rat.isInt_iff
#check @Rat.den_intCast
#check @Rat.num_intCast
#check @Int.cast_injective
#check @Rat.divInt_eq_iff

-- ===== MvPolynomial: evaluating an Int-coefficient polynomial at rationals =====
#check @MvPolynomial.eval₂
#check @MvPolynomial.eval₂Hom
#check @MvPolynomial.eval
#check @MvPolynomial.aeval
#check @MvPolynomial.eval₂_eq_eval_map
#check @MvPolynomial.coeff
#check @MvPolynomial.totalDegree
#check @MvPolynomial.rename
#check @MvPolynomial.C
#check @MvPolynomial.X
#check @MvPolynomial.constantCoeff

-- ===== Fin n tuples: existential over witnesses =====
#check @Fin.forall_fin_succ
#check @Fin.exists_fin_succ
#check @Fin.succ
#check @Fin.cases

-- ===== Sums of squares over Q — the no-discreteness obstruction =====
#check @Nat.sum_four_squares
#check @Rat.sum_four_squares
#check @sq_nonneg
#check @sq_pos_of_ne_zero
#check @Rat.exists_eq_sum_four_squares

-- ===== p-adics / local fields =====
#check @padicValRat
#check @Padic
#check @padicNorm
#check @PadicInt

-- ===== Quadratic forms: Hasse-Minkowski / local-global =====
#check @QuadraticForm
#check @QuadraticForm.IsHassePrinciple
#check @HasseMinkowski
#check @hilbertSymbol
#check @QuadraticForm.equivalent_one_iff

-- ===== Elliptic curves (the incumbent's G / M / H / PC ingredients) =====
#check @WeierstrassCurve
#check @EllipticCurve
#check @WeierstrassCurve.Δ
#check @MordellWeil
#check @SelmerGroup
#check @canonicalHeight
#check @NeronTate

-- ===== Numbers fields Q(sqrt 2) — ingredient G lives there =====
#check @IsPrimitiveRoot
#check @Zsqrtd
#check @QuadraticField

-- ===== norm_num / ring behaviour on concrete rational eval (sanity) =====
example : (MvPolynomial.eval₂ (Int.castRingHom ℚ) (![ (1/2 : ℚ), 3 ])
    (MvPolynomial.X 0 * MvPolynomial.X 1 - MvPolynomial.C (3/2))) = 0 := by
  norm_num [MvPolynomial.eval₂_X, MvPolynomial.eval₂_mul, MvPolynomial.eval₂_C]
