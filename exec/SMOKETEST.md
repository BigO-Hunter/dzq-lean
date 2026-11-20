# SMOKETEST.md — sampled smoke tests, and what is NOT reachable

**Label: SAMPLED throughout. Nothing here is a proof; every claim's proof (where one exists) is in
VERIFICATION.md.**

The mission asks for a two-direction check of the iff on random rationals: q ∈ Z ⟹ no witness;
q ∉ Z ⟹ witness exists. **The global version is NOT REACHED**, for two independent reasons:

1. `F` cannot be assembled completely today: the patch members for p ∈ E_exc ∖ {2} are the named
   blocker (POLYNOMIAL_LITERAL.md §4). With an incomplete patch, `F_partial = 0` does not mean
   `X ∉ Z`, so a pass/fail on integers would be meaningless rather than reassuring.
2. Even fully assembled, the (⇐) direction (q ∉ Z has a witness) is the arithmetic theorem — a
   global Hasse/weak-approximation argument over all places, not something a finite numerical
   search can decide. Sun's §11 and Daans's (9.2) own it.

What *is* testable is the local content the assembly rests on, and that is what is tested below
(`smoketest.py`, `verify_tau_map.py`, `brute_check.py`).

## Test A — freezing at 2 (the piece the freezing machinery exists for)

ψ_τ(a,b,c) must be satisfiable at every point of P₂ = {a odd, b unit, c ∈ Z₂}. With the corrected
2-τ map (τ = 1 if c ≢ 0 mod 4, τ = 3 if c ≡ 0 mod 4):

| test | result |
|---|---|
| full grid a ≡ a₀, c ≡ c₀ mod 2^10, all 32 cells (524,288 points) | **0 obstructed** |
| 60,000 random points with unbounded depth, criterion test | **0 failures** |
| 2,000 random c-odd points, *constructive*: y = √w built, δ(c²−Ay²) = 16 verified exactly | **2000/2000** |
| same 524,288-point grid with the derivation lane's τ (t_p mod 8) | **76,446 obstructed** |

Directional sanity: the *soundness* side of Prop 2.1 (ψ_τ ⟹ c ∈ O₂) is vacuous at v = 2, because
every c in P₂ is already integral — there is nothing there to test, and nothing here overclaims it.

Explicit counterexample carried through the rigorous (non-criterion) search: a = 145, b = 1,
c = −208, τ = 1 (the τ the canonical construction produces for that cell) admits **0** admissible y
residues mod 2^10 and mod 2^12, i.e. no Q₂ solution exists; τ = 3 at the same point is solvable.

## Test B — the p = 2 patch formula's local iff

G2_REDERIVATION.md §1: `x ∈ Z_(2) ⟺ x = 0 ∨ ∃x₁,x₂,x₃: 10x²(7+5x₁−5x₁²−2x₂²−2x₂x₃+2x₃²) = 1`.
With u = x₁−1/2, φ = x₂²+x₂x₃−x₃² it is `5u² + 2φ = T(x) := 33/4 − 1/(10x²)`. Since 2φ takes
exactly the odd-valuation values and 5u² exactly the even-valuation ones (in the right square
class), a witness exists iff some u makes `v(T−5u²)` odd, or T = 5u². Searched over
v(u) ∈ [−4,8], u mod 2⁸:

| x (samples) | v₂(x) | in Z_(2)? | witness |
|---|---|---|---|
| 0 | — | yes | x = 0 branch of the disjunction |
| 1, 3, −1, −5, 1/3 | 0 | yes | found, v(T−5u²) = −1 |
| 2, 6 | 1 | yes | found, v = −3 |
| 4, 12 | 2 | yes | found, v = −5 |
| 8, 8/3 | 3 | yes | found, v = −7 |
| 1/2, 3/2 | −1 | **no** | **none in range** |
| 1/4 | −2 | **no** | **none in range** |
| 1/8 | −3 | **no** | **none in range** |
| −7/16 | −4 | **no** | **none in range** |

**17/17 samples agree with the iff**: all 12 points inside Z_(2) produced a witness; all 5 outside
produced none in the search range. The negative side is the interesting one, and "none found" there
is *suggestive, not proof* — the search covers a bounded range of u. For the freezing obstruction
the same question was settled rigorously instead, by the exhaustive y-search of
`brute_check.py (B)`.

## Test C — the assembly is self-consistent

* `F_eval.py` (straight-line evaluator) vs the emitted sparse term lists: identical values on 20
  random rational witness tuples for each of the 8 objects (F_Φ, F_2, P̂_τ, P₀_τ, Θ-factor for both
  τ). Two representations, one polynomial.
* A degenerate witness (all witnesses 0, X = 3/2) gives F = 1864462541792015147665225/4 > 0 — as it
  must, F being a sum of squares; it also shows the evaluator is live rather than returning 0
  everywhere.
* F is by construction ≥ 0, so F = 0 forces every conjunct to vanish exactly — the fold checks are
  not vacuous.

## What a future run should add

1. Compute the p ∈ E_exc ∖ {2} patch constants, re-run Test B per prime, assemble `F_patch` fully.
2. Only then attempt the global smoke test, and even then only as a search over a restricted
   witness ansatz — an honest smoke test, never a proof.
