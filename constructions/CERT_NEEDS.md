# CERT_NEEDS — what a sorry-free Lean certificate needs, per candidate

Mathlib checked at rev
`d13f23b723b8a846827a245b89c10fc7d3f11612` (grep counts below are from that checkout, so they are
measurements, not guesses).

## 0. What IS in Mathlib today (all verified present)
- `Mathlib/NumberTheory/SumFourSquares.lean` — Lagrange.
- `Mathlib/NumberTheory/LegendreSymbol/` — `Basic`, `JacobiSymbol`, `QuadraticReciprocity`. (Koenigsmann
  leans on quadratic reciprocity in Prop 10 and 16; that ingredient is **free**.)
- `Mathlib/NumberTheory/Padics/` — `PadicIntegers`, `Hensel`, `LocalField`, `HeightOneSpectrum`.
- `Mathlib/LinearAlgebra/QuadraticForm/` — `Basic`, `Real` (signature), `Signature`, `TensorProduct`,
  `Isometry`, `Radical`. So "quadratic form", "isometry", "signature at ∞" exist.
- `Mathlib/AlgebraicGeometry/EllipticCurve/` — Weierstrass models, division polynomials, Jacobian.
- `Mathlib/NumberTheory/LSeries/` + `Nonvanishing` + `EllipticCurve/LFunction.lean` — beginnings of L-series.

## 1. What is ABSENT (the honest gap list)
| needed by | item | Mathlib status |
|---|---|---|
| C1 (and every route) | **Hasse–Minkowski / local–global for quadratic forms** (`S_{a,b}(Q) = Q ∩ ⋂_p S_{a,b}(Q_p)`, Koenigsmann Fact (e)) | **absent** (0 files for `HasseMinkowski`) |
| C1 | **Hilbert symbol** `(a,b)_p` over Q, its reciprocity law, and the local-splitting criterion (Koenigsmann Observation 5's three case tables) | **absent** (0 files) |
| C1 | **isotropy / represents-a-value predicates** for quadratic forms | **absent** (`IsIsotropic`, `Isotropic`: 0 files) |
| C1 | Jacobson radical of a semilocal subring `⋂_{l∈Δ} Z_(l) ⊂ Q` (Lemma 13/14, 17) | not packaged; `Localization`/`IsLocalization` present, so `Z_(p)` is expressible — the *assembly* is new work |
| C3 | Selmer groups `Sel_{2^∞}(E/Q)` and their `Z_2`-corank | only `RingTheory/DedekindDomain/SelmerGroup.lean` + `RingTheory/Polynomial/Selmer.lean` (unrelated algebra); **no elliptic Selmer theory** |
| C3 | Mordell–Weil rank, Sha, Tamagawa numbers | **absent** (`MordellWeil`: 0 files) |
| C3 | order of vanishing `ord_{s=1} L(E,s)`, root number, modularity (BCDT), Dokchitser parity, Fontaine–Mazur | **absent** (no `ord_{s=1}`, no root-number API) |
| C3 | Faltings heights, canonical heights on abelian varieties | **absent** |

## 2. Per-candidate verdict

### C1 — Q∖Z Diophantine (Koenigsmann negation) — **MOST CERTIFIABLE**
Unconditional theorem, no extra hypotheses. Certification plan, in order of decreasing cost:
1. **Avoid full Hasse–Minkowski.** Only *specific* forms are needed: the quaternary norm form
   `x₁² − a x₂² − b x₃² + ab x₄² = 1` (trace-1 elements of the quaternion algebra `H_{a,b}`) and its
   `S+S` sums. For these the required input is the *split/norm criterion*
   `a ∈ N(Q(√b)) ⟺ Δ_{a,b} = ∅`, not the general theorem. A Lean development can prove the needed
   instances (Hilbert-symbol reciprocity for Q + the case tables of Observation 5) as a bounded task —
   still large, but finite and concrete, ~ the size of a serious Mathlib contribution.
2. `Z_(p)`, `Z_(2)`, `J(R)`, `Φ_k`, `Ψ` are then pure algebra over `⋂ Z_(l)`: localization +
   valuation (`PadicIntegers`) + the parity bookkeeping in Lemma 13(b) (which is `v_l` parity arithmetic,
   very formalizable).
3. The final step is Lemma 17 + Prop 18(b): a short, purely logical argument (`R̃ = ⋃ Z_(l)`) — the
   easiest part, and `lem:pole`-style arguments are short.
**Bottom line**: no unproved mathematics is imported anywhere. Everything is a Mathlib *build* problem.
That is the opposite of C3.

### C2 — ∀∃ (7 witnesses) — cheap to *state*, worthless to score
Certifying the formula's arithmetic needs the same Hasse–Minkowski core as C1 plus the 2309-style finite
enumeration. It is strictly more work than C1 for zero board score (two `∀`). Do it only as C3's engine.

### C3 — bounded catalogue / the incumbents' shape — **NOT certifiable today, by construction**
The Lean `sorry` is not the obstacle; the mathematics underneath it is. Three independent unproved inputs:
1. `hyp:RC`: `corank_{Z₂} Sel_{2^∞}(E_ℓ/Q) = 1 ⟹ ord_{s=1} L(E_ℓ,s) = 1` for all squarefree
   `ℓ ≡ 11 (mod 12)`. This is an upper bound on analytic rank — the Gross–Zagier/Kolyvagin direction —
   asserted for an infinite family. Nothing in Mathlib is within an order of magnitude of this.
2. `hyp:o8-height`: their own text says of `log₂ H_* < 4,783,227`: *"This is a check of the number H, not
   a proof that H is a height constant."* No Mathlib API for heights on abelian varieties exists.
3. `hyp:PC` (pole completeness), derived from (1).
A certificate for C3 would require formalizing BSD-adjacent arithmetic geometry first. **Recommendation:
never certify C3; do not spend the campaign's Lean budget on it.**

## 3. Precedent to copy for *any* certification attempt
*A Formal Proof of Complexity Bounds on Diophantine Equations* (arXiv:2505.16963, Isabelle/AFP, 2025)
machine-checks **universal pairs** `(ν, δ)` over `N` and `Z`, starting from Jones' (58,4). The reusable
pattern: (a) define the polynomial, (b) prove the *projection* equivalence (the only mathematically
loaded step), (c) verify the expansion numerically with an exact certificate. That is exactly the shape
Glazer V4's "certificate checks" take — and exactly why they admit they "do not prove the source
system's arithmetic characterization": step (b) is the whole problem.

## 4. If the campaign wants ONE certifiable artifact
Build **C1**: "`Q∖Z` is Diophantine in `Q`, explicitly, in ≈10²–10³ rational witnesses", from
Koenigsmann Thm 1 / Prop 18(b). It is true, published, unconditional, smaller than 4,973, and its
remaining work is Mathlib engineering rather than open arithmetic geometry.
