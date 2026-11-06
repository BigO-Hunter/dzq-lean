import Mathlib

-- Exact types of the lemmas the scaffold will actually use.
#check @Rat.den_eq_one_iff
#check @Rat.den_pos
#check @Rat.den_intCast
#check @Rat.num_intCast
#check @Rat.num_div_den

-- Fin.cons: the Matrix-free way to say "first coord = q, rest = witnesses"
#check @Fin.cons
#check @Fin.cons_zero
#check @Fin.cons_succ
#check @Fin.tail

-- MvPolynomial eval₂ API, concretely
#check @MvPolynomial.eval₂_X
#check @MvPolynomial.eval₂_C
#check @MvPolynomial.eval₂_add
#check @MvPolynomial.eval₂_mul
#check @MvPolynomial.eval₂_pow
#check @MvPolynomial.eval₂_intCast
#check @MvPolynomial.eval₂_natCast

-- ===== RECIPE TEST 1: concrete eval via Fin.cons (no ![...], no Matrix) =====
example :
    (MvPolynomial.eval₂ (Int.castRingHom ℚ)
      (Fin.cons (1/2 : ℚ) (fun _ => (3:ℚ)) : Fin 2 → ℚ)
      (MvPolynomial.X 0 * MvPolynomial.X 1 - MvPolynomial.C (3/2))) = 0 := by
  simp [MvPolynomial.eval₂_X, MvPolynomial.eval₂_mul, MvPolynomial.eval₂_sub,
        MvPolynomial.eval₂_C, Fin.cons_zero, Fin.cons_succ]
  norm_num

-- ===== RECIPE TEST 2: does `simp` alone close a bigger one? =====
example :
    (MvPolynomial.eval₂ (Int.castRingHom ℚ)
      (Fin.cons (2 : ℚ) (fun _ => (1/4 : ℚ)) : Fin 3 → ℚ)
      ((MvPolynomial.X 0 - MvPolynomial.C 2)^2
        + (MvPolynomial.X 1 * MvPolynomial.X 2 - MvPolynomial.C (1/16)))) = 0 := by
  simp [MvPolynomial.eval₂_X, MvPolynomial.eval₂_mul, MvPolynomial.eval₂_sub,
        MvPolynomial.eval₂_add, MvPolynomial.eval₂_pow, MvPolynomial.eval₂_C,
        Fin.cons_zero, Fin.cons_succ]
  norm_num

-- ===== RECIPE TEST 3: the den = 1 direction for a concrete integer =====
example : ((3 : ℚ)).den = 1 := by
  rw [Rat.den_intCast]
  norm_num

example : ¬ ((3/2 : ℚ)).den = 1 := by
  norm_num [Rat.den_eq_one_iff]

-- ===== the "sums of squares are useless over Q" obstruction, concretely =====
-- every nonneg rational is a sum of four rational squares => P = q - (sos) never
-- defines Z. We test the *usable* direction: an integer IS a sum of 4 squares.
example : ∃ a b c d : ℚ, (a^2 + b^2 + c^2 + d^2 : ℚ) = 3 := by
  refine ⟨1, 1, 1, 0, ?_⟩
  norm_num
