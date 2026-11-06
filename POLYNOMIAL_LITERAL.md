# POLYNOMIAL_LITERAL.md — how literal the 11-variable polynomial now is

**One line: literal down to every leaf, and to a runnable straight-line program; NOT literal as a
single expanded term list (combinatorially out of reach), and one constant group is still open
(the patch primes other than 2).**

    F = (F_main · F_patch)² + (X·ι − 1)²
    F_main  = F_Φ² + F_Θ²
    F_Θ     = ∏_{τ∈Λ} [ (δ_τ ζ − 1)² + P̂_τ² + ((D ζ′ − 1) P₀_τ)² ]
    F_patch = ∏_{p∈E_exc} F_p        (F_2 literal; the rest = NAMED BLOCKER, §4)

Constants instantiated here: **S = {2}, u = 1, π = Π_S = 2**, and **Λ = (1, 3)** — the two-τ map
verified in `VERIFICATION.md` §4 (the derivation lane's τ values do not serve their cells;
the corrected set is smaller and proved).

## 1. What is emitted (all sha256-pinned, artifact-lane sparse format)

Format is `dzq-artifact`'s: `# comment` header, then `<coeff> <var>:<exp> ...`, sorted by the
sparse monomial key, variables `0=X 1=a 2=b 3=y 4=r 5=s 6=ζ 7=ζ′ 8=b₁ 9=σ 10=υ 11=ι`.

| object | terms | degrees (X,a,b,y,r,s,ζ,ζ′,b₁,σ,υ,ι) | sha256 |
|---|---|---|---|
| `phi.terms.txt` — F_Φ | 11 | 0,2,2,0,0,0,0,0,2,2,2,0 | `4bf5f5dbc3d67a2805df957ca99fc5eb5c13a1143a771e9915ab0bebe89626b1` |
| `patch2.terms.txt` — F_2 | 7 | 2,0,0,2,2,2,0,0,0,0,0,0 | `4da3a7e7fb13cd5a9cf7cf8f75b679493cb60d54a026bd0f86e1edfdafcddec4` |
| `Phat_tau1.terms.txt` | 103 | 12,14,8,2,2,2,0,0,0,0,0,0 | `fee45d45c0b54c211f25f225614dbb47779e4d64ba7a5488cb20010f01e1bc93` |
| `Phat_tau3.terms.txt` | 116 | 12,14,8,2,2,2,0,0,0,0,0,0 | `31e07260e7df347fd53e12399c5c66dd5041d0a826f5ee7ac71190a131ad0658` |
| `P0_tau1.terms.txt` | 6 | 0,4,1,2,2,2,0,0,0,0,0,0 | `55e629db654ba51cc43f73088ac55909341bbea7379078de951e0c9aaf3b6b30` |
| `P0_tau3.terms.txt` | 7 | 0,4,1,2,2,2,0,0,0,0,0,0 | `8ec3517dee49ab32399ea44c730f68bf5fafca68c24621e5baaf6d2c4166e864` |
| `thetafac_tau1.terms.txt` | 2,022 | 24,28,16,4,4,4,2,2,0,0,0,0 | `20eff90d491963a16a65db29512ad75e9e80888754a355b71f211752dbcceeb3` |
| `thetafac_tau3.terms.txt` | 2,347 | 24,28,16,4,4,4,2,2,0,0,0,0 | `398035ccded30b4ce666ffec454cb6deb752345f376d3acb721b8afecbf02cdb` |
| `F_recipe.json` — structural spec, every constant filled | — | — | `1d372b309047ee22d089f2dc3fc41333d68dc8b3e66e6e48f3cd90bf84cd24ee` |
| `TAU.json` — per-cell frozen data (32 cells, 64-bit rational truncations) | — | — | `df2307858a606bf37bb293b66ea7cdf356ce24d06cb413c87fb65d0d055895d9` |
| `measurements.json` — every number quoted in VERIFICATION.md | — | — | `74c04e6757d485ce7d26391d83e264493499753f4198d6e0bfe884aacebf2cb3` |

`branches.json` reproduces the same table programmatically (`assemble.py` regenerates the leaves).

**The degree table of POLYNOMIAL.md §4 is confirmed exactly** by the expanded leaves: P̂_τ is
(12,14,8,2,2,2) in (X,a,b,y,r,s), the Θ-factor (24,28,16,4,4,4,2,2). With the corrected |Λ| = 2
the estimate `deg_X(F) ≈ 24|Λ| + deg(F_patch) + 2` becomes ≈ 50 + patch, not ≈ 12,300.

## 2. Why no single expanded term list

Measured, not guessed:

* a Θ-factor has 2,022 (τ=1) / 2,347 (τ=3) terms;
* F_Θ = their product ⟹ ~**4.7·10⁶** terms before cancellation;
* F_main = F_Φ² + F_Θ² ⟹ ~2·10¹³ terms; F = (F_main·F_patch)² + … squares again.

So the top-level product and squares are left as products — which is exactly what POLYNOMIAL.md §2
writes. Nothing is approximated: the object is a product of literal factors.

## 3. The runnable form (`F_eval.py`)

`F_eval.py` is the same polynomial as a straight-line program over `Fraction` — every constant
literal, no symbolic gaps. `python3 F_eval.py` re-checks, on 20 random rational witness tuples per
object, that the evaluator and the sparse term lists agree bit-for-bit (all 8 objects pass), i.e.
the two representations are the same polynomial.

Limitation, stated in the file: `F_eval.py` includes only the p = 2 patch member. It is therefore
`F_partial`, and `F_partial = 0` must not be interpreted as "X ∉ Z".

## 4. The one open constant group — precisely

**BLOCKER: `E_exc` and the per-prime patch constants for p ∈ E_exc ∖ {2}.**

* `E_exc` is Sun's finite exceptional set in (9.4) (`D_Θ ∪ ⋃_{w∈E_exc} m_w = ⋃_{w∉S} m_w`). It is
  not enumerated in the derivation lane either: it is the union of the primes with residue field
  ≤ 25 (Lemma 5.1 needs q > 25) — at least {3,5,7,11,13,17,19,23} — the poles of τ, the primes
  dividing τ(τ²−1) for the τ actually used, and whatever §§7–8 force.
* For each p ∈ E_exc one needs the Daans Prop 4.2 constants (A_p, B_p, π₄_p, 𝔞_p) and hence the
  ∃₃ formula for Z_(p). The template is written in G2_REDERIVATION.md §1 and executed there for
  **p = 2 only** (Q = [1,2)_Q, ΔQ = {2,5}, π₄ = 10, 𝔞 = 8 → `10x²(7 + 5x₁ − 5x₁² − 2x₂² − 2x₂x₃
  + 2x₃²) − 1 = 0`).
* It is a finite search per prime, so nothing is mathematically blocked — but with ≥ 8 primes
  needing it, `F_patch` is not literal today. This is the only constant group in the assembly
  that is not instantiated.

Second, softer, gap: the τ set. Λ = (1,3) is verified to serve all of `P_2` *locally*, but the Sun
construction needs 4 distinct lifts per class with residues ∉ {0,±1} at the places in play (τ = 1
has residue 1 everywhere, so it is unusable on its own, and τ = 3 ≡ 0 mod 3). Choosing those lifts
is what determines E_exc — so the two gaps are one gap viewed twice.

## 5. Reproduce

```bash
cd ~/bigo-campaign/dzq-exec
python3 test_padic.py        # 20 checks on the 2-adic machinery
python3 cells.py             # 32 cells, 17 exact checks each
python3 measure.py           # measurements.json (all numbers in VERIFICATION.md)
python3 verify_tau_map.py    # the 2-tau map: 60k points, 0 failures
python3 gen_tau.py           # TAU.json
python3 assemble.py          # the literal leaves + branches.json
python3 gen_recipe.py        # F_recipe.json
python3 F_eval.py            # evaluator == term lists, 8 objects x 20 tuples
python3 smoketest.py         # SMOKETEST.md
```
