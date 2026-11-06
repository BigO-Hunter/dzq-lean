# SMOKE2.md — post-fold smoke suite (SAMPLED where marked)

Everything below was run after the patch fold. Scripts: `smoke2.py`, `checks2.py`, `localtest.py`,
`F_eval.py`. Nothing here is a proof; the proofs/derivations live in `VERIFICATION.md`, `E_EXC.md`,
`PER_PRIME.md`.

## 1. Each patch factor has the right local semantics (all nine primes)

Claim: F_p = π_p G_p(y,r,s) − p²X² is soluble over Q_p **exactly** when v_p(X) ≤ −1, i.e. X ∉ Z_(p).
Checked twice per cell — the square-class criterion (Prop 3.3) and an independent brute-force
representation search for ⟨D,B,−BD⟩ — over X ∈ {1, 2, 3, 5, 1/p, 1/p², 2/p, 1, p}:

    p   |  X : v_p(X) : criterion/brute
    2   |  1:0:n/n  2:1:n/n  3:0:n/n  5:0:n/n  1/2:-1:Y/Y  1/4:-2:Y/Y  2/2:-1:Y/Y
    3   |  1:0:n/n  2:0:n/n  3:1:n/n  5:0:n/n  1/3:-1:Y/Y  1/9:-2:Y/Y  2/3:-1:Y/Y
    5 … 23 | same pattern, shifted to p

**81/81 cells as expected**, and criterion == brute force in every cell (`checks2.py (c)` extends
this to 197 random points spanning v_p(X) ∈ {−2,…,3}).

## 2. Integers are rejected by every patch factor

For X = 1…30 (all integers) and all nine primes: no F_p is locally soluble. **0 exceptions.** The
patch therefore cannot manufacture a witness for an integer.

## 3. Non-integers are accepted at exactly their denominator primes

| X | denominator primes | patch factors soluble |
|---|---|---|
| 1/3 | {3} | {3} |
| 1/5 | {5} | {5} |
| 1/7 | {7} | {7} |
| 2/9 | {3} | {3} |
| **3/10** | **{2, 5}** | **{2, 5}** |
| 1/23 | {23} | {23} |

This is the (9.4) union in action: a rational has a negative p-adic valuation exactly at the primes
of its denominator, and the patch covers precisely those. It is also the measurement that
**justifies the p = 2 member**: X = 3/10 is missed without it.

## 4. The freezing layer still holds with the eight parameters

Exhaustive over a ≡ odd mod 2⁷, c mod 2⁷, per class (and a mod 2⁹ in `e_exc.py`):

| class | parameters | obstructions |
|---|---|---|
| A (c ≢ 0 mod 8) | 1, 17, 33, 49 | 0 / 7,168 each (0 / 114,688 at 2⁹) |
| B (c ≡ 0 mod 4) | 3, 11, 19, 27 | 0 / 2,048 each (0 / 32,768 at 2⁹) |

## 5. The assembly is self-consistent after the fold

`F_eval.py`: the straight-line evaluator equals the 34 emitted sparse term lists on 12 random
rational witness tuples each — **408 comparisons, 0 mismatches** (objects: F_Φ; P̂_τ, P₀_τ and the
Θ-factor for each of the 8 τ; the 9 patch factors).

A degenerate witness (all witnesses 0, X = 3/2) evaluates to
1141615009904235514611987408921645910344701075861716603243147398432371713269790311301831526418367238287265408685614150390625/4294967296 > 0 — F is a sum of squares times a product squared
plus (Xι−1)², so a positive value is the expected outcome and shows the evaluator is live.

## 6. What is still NOT reached

The global two-direction iff on rationals (q ∈ Z ⟹ no witness; q ∉ Z ⟹ witness) remains
**NOT REACHED**, now for one reason only:

* the *(⇐)* direction is the arithmetic theorem — a global Hasse / weak-approximation argument over
  all places (Sun §§7–8, §11), not a numerical search. No finite evaluation can establish it.

The constant-level blockers are gone: every constant in the assembly is computed and verified, so
the obstruction to a *smoke test* of the (⇒) side is only the search dimension (11 witnesses, and
the main branch's conditions are Diophantine rather than open, so numerical search finds nothing).

## 7. Corrections this suite forced

1. **Patch constant term.** The earlier draft used πX²G − 1 (which encodes X ∈ Z_(p)); the duality
   requires the argument x = 1/(pX), giving πG − p²X². `SMOKE2 §1/§3` would fail on the old form
   (it fires for X = p, not for X = 1/p).
2. **Patch prime set.** Nine primes, not eight: S₀ = ∅ while S = {2}, so m_2 is adjoined by (9.4).
3. **h-bridge variable.** z = ι³ (ι = 1/X), not X³ — otherwise the polynomial defines the proper
   subset ⋃_w m_w ⊊ Q∖Z (1/3 ∈ Q∖Z ∖ ⋃_w m_w).
