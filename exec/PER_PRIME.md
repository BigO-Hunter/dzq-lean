# PER_PRIME.md — the Prop-4.2 constants for all nine patch primes

**Headline: every prime in the patch set has explicit constants satisfying every hypothesis of
Daans's Lemma 4.1, verified by direct Hilbert computation; the resulting existential-3 formulas are
emitted as sparse term lists and their local behaviour is verified over Q_p. No obstruction.**

## 1. What had to be found, per prime p

For K = Q and S = {p}, Daans Lemma 4.1 needs Q = [A,B) nonreal with {p} ⊆ Δ(Q), plus π and 𝔞 such
that, for every v ∈ Δ(Q):

    (h1) v(π) = 1
    (h2) v(𝔞) ≥ 0 and v(1+4𝔞) = 0
    (h3) X² − X − 𝔞 has a root over Q_v  ⟺  v = p

For |Δ| even and {p} ⊆ Δ we need a second ramified prime q, so Δ(Q) = {p, q}. Then π = pq, and
(h3) says: the discriminant d = 1+4𝔞 must be a **square at p** and a **nonsquare at q** (v_p(d) =
v_q(d) = 0, which is (h2)). One further condition kills the degenerate witness (see §3): π·d must
not be a perfect square in Q.

`perprime.py` searches: (i) small (A,B) with Δ(1+4A, B) = {p,q}, ∞ ∉ Δ, and — mirroring the
published p = 2 shape — B ≡ 0 mod p with D = 1+4A a unit at p; (ii) the least 𝔞 ≥ 0 meeting (h2),
(h3) and the degeneration condition. The p = 2 row came out of the same search, and the derivation
lane's own documented choice (A=1, B=2, 𝔞=8, π=10) passes the same checker as a control.

## 2. The constants

| p | A | B | q | Δ(Q) | 𝔞 | d = 1+4𝔞 | π = pq | d square at p? | d nonsquare at q? |
|---|---|---|---|---|---|---|---|---|---|
| 2 | −1 | 2 | 3 | {2,3} | 4 | 17 | 6 | yes (17 ≡ 1 mod 8) | yes (17 ≡ 2 mod 3) |
| 3 | 1 | −3 | 5 | {3,5} | 3 | 13 | 15 | yes (13 ≡ 1 mod 3) | yes (13 ≡ 3 mod 5) |
| 5 | −1 | 5 | 3 | {5,3} | 7 | 29 | 15 | yes (29 ≡ 4 mod 5) | yes (29 ≡ 2 mod 3) |
| 7 | 1 | −7 | 5 | {7,5} | 9 | 37 | 35 | yes (37 ≡ 2 mod 7) | yes (37 ≡ 2 mod 5) |
| 11 | −1 | 11 | 3 | {11,3} | 1 | 5 | 33 | yes (5 ≡ 4 mod 11) | yes (5 ≡ 2 mod 3) |
| 13 | 1 | −13 | 5 | {13,5} | 4 | 17 | 65 | yes (17 ≡ 4 mod 13) | yes (17 ≡ 2 mod 5) |
| 17 | −1 | 17 | 3 | {17,3} | 13 | 53 | 51 | yes (53 ≡ 2 mod 17) | yes (53 ≡ 2 mod 3) |
| 19 | −2 | 19 | 7 | {19,7} | 1 | 5 | 133 | yes (5 ≡ 9 mod 19) | yes (5 ≡ 5 mod 7) |
| 23 | −1 | 23 | 3 | {23,3} | 7 | 29 | 69 | yes (29 ≡ 6 mod 23) | yes (29 ≡ 2 mod 3) |

Every row: `check_all()` reports **ALL PASS** for (h0)-(h3) plus the degeneration condition
(`perprime.json`). The shape is uniform — B = ±p carries the ramification at p, D = 1+4A is a small
unit (±3, 5, ±7, ±11) — which is exactly the published p = 2 pattern (A = 1, B = 2, D = 5) with the
roles of "the small unit" and "the prime" swapped or not, as the Hilbert symbols require.

## 3. The emitted polynomial

Prop 3.6(iii) with c = 1 (verified symbolically for arbitrary (A,B) by `checks2.py (b)`):

    LHS(c=1) = (1+4A)(x₁ − x₁²) − A − B(x₂² + x₂x₃ − A x₃²)      [identity, sympy]

so the equation LHS = d_quad with d_quad = −𝔞′ (𝔞′ = 𝔞 − (πx²)⁻¹) reads

    π x² · G_p(x₁,x₂,x₃) = 1,     G_p = (1+4A)(x₁ − x₁²) + (𝔞 − A) − B(x₂² + x₂x₃ − A x₃²).

**Degenerate stratum.** The excluded witness (2x₁ − c, x₂, x₃) = (0,0,0) is x₁ = 1/2, x₂ = x₃ = 0,
where G_p = d/4, so the equation becomes x² = 4/(πd). It has no rational solution iff πd is a
square in Q; the search enforces squarefree(πd) ≠ 1, so the "not all zero" side condition can be
dropped. ✓ every row.

**The instantiation used.** The polynomial defines Q ∖ Z = {X : 1/X ∈ ⋃ m_p} (Sun's duality (1.1)),
so the O_(p) formula is applied to the argument x = 1/(pX), which clears to

    F_p(X, y, r, s) = π_p · G_p(y, r, s) − p² X²        (7 terms, degrees (2,0,0,2,2,2) in (X,a,b,y,r,s))

with the same three witnesses (y, r, s) serving every patch factor (only one factor need vanish).

## 4. Verification of the local behaviour

`SMOKE2.md §1` (criterion and independent brute force, 81 cells) and `localtest.py`:

    F_p is soluble over Q_p  ⟺  v_p(X) ≤ −1   ⟺  X ∉ Z_(p)

for all **nine** primes. Mechanically: substituting u = s₁ − 1/2, v = s₂ + s₃/2, w = s₃/2 turns
F_p = 0 into the ternary form D u² + B v² − BD w² = R with R = d/4 − p²X²/π, i.e. the pure norm
form of the quaternion (D,B) — ramified at p — so by Prop 3.3 (splitting over every quadratic
extension of a local field) solubility is exactly "R is a nonsquare at p", which at these constants
is exactly v_p(R) odd = 1 + 2v_p(X) odd = v_p(X) ≤ −1. `checks2.py (c)` confirms criterion and
brute force agree on 197 random points spanning v_p(X) ∈ {−2,…,3}.

## 5. Files

| file | content |
|---|---|
| `perprime.py` | the search, the hypothesis checker, the constant dictionary and the F_p term lists |
| `perprime.json` | all nine rows with checks, constants and coefficient dictionaries (sha256 `b523be5f632aa476cc25ae3b7ded0a2c8cc1e8d82d7151a2d2703759f9e93ebe`) |
| `patch_p{p}.terms.txt` | the emitted F_p per prime (7 terms each, hashes in `POLYNOMIAL_LITERAL.md`) |
| `hilbert.py` | Hilbert symbols over Q, with the (5,2) control arm |
| `localtest.py`, `checks2.py`, `smoke2.py` | the local-behaviour verification |
