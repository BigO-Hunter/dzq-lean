# CONSTRUCTIONS — lane A2, re-scored against the 4,973 bar

Bar: **4,973 total variables** (Glazer V4 quartic, 4,972 witnesses, degree 4, 72,925 monomials,
4,552 squared quadratic residuals). Board form: `q ∈ Z ⟺ ∃w ∈ Q^k, P(q,w) = 0`, SCORE = k+1.

## 0. Counting calculus (this is the whole game; degree is FREE)

Verified from the OpenAI preprint §7 (its own proof) and classical sources:

| construct | polynomial cost | variable cost |
|---|---|---|
| atom `f = 0` | — | 0 |
| conjunction `∧ᵢ fᵢ = 0` | `Σᵢ fᵢ²` over Q (formally real: sum of squares = 0 ⟺ each = 0) | **0** |
| disjunction `∨` | product | **0** |
| negation `f ≠ 0` | `∃z: f·z = 1` | **1** |
| `∃` over Q | — | **1 each** |
| degree | `Σ (quadratic)²` ⟹ degree 4 | **free** |

Two consequences the lane should bank:
1. **Degree 4 is a free normal form.** `Σqᵢ²` with each `qᵢ` quadratic is degree ≤ 4 (OpenAI §7(ii),
   itself Davis 1973 Thm 7.5 + Jones 1982). The board's degree tiebreak is therefore degenerate —
   every serious entry is quartic. Glazer's degree-4 headline is *rediscovery*, not the contribution.
2. **k ≈ (number of constraints in the source system) + (number of negations).** Glazer's numbers fit
   this exactly: 4,973 ≈ 4,552 residuals + 421 overhead. So **the only lever on SCORE is the size of
   the enumerated source system** — an arithmetic-input problem, not an encoding problem.

## 1. CANDIDATES, RE-SCORED

### C1 — Koenigsmann negation → **Q∖Z** is Diophantine (UNCONDITIONAL, published)
Koenigsmann, Ann. Math. 183 (2016) 73–93, Thm 1 + Cor 2 + Prop 18(b), Lemma 17.
`t ∈ Z ⟺ ∀x g(t,x) ≠ 0` hence `t ∉ Z ⟺ ∃x g(t,x) = 0`.

Explicit shape (Prop 18(b), verbatim structure):
```
Z = Z̃_(2) ∩ ⋂_{k=3,5,7} ⋂_{p∈Φ_k} R̃_p^[k] ∩ ⋂_{(p,q)∈Ψ} R̃_{p,q}^[1],
R̃ := {x : ¬∃y ∈ J(R), x·y = 1},  R̃ = ⋃_{l∈Δ} Z_(l)   (Lemma 17(b))
```
Σ₁ form of the complement, with `Φ_k`, `Ψ`, `J(·)` Diophantine (Koenigsmann Cor 15, Prop 16):
```
q ∉ Z  ⟺  ∃y (y ∈ J(Z_(2)) ∧ qy = 1)
        ∨ ∃p,k (p ∈ Φ_k ∧ ∃y (y ∈ J(R_p^[k]) ∧ qy = 1))
        ∨ ∃(p,q') ( (p,q') ∈ Ψ ∧ ∃y (y ∈ J(R_{p,q'}^[1]) ∧ qy = 1) )
```
- **iff, direction q ∈ Z ⟹ no witness**: if `qy = 1` with `y ∈ J(R)` then `q ∉ R̃` (Lemma 17's own
  argument: `q ∉ R̃ ⟺ v_l(q) < 0 ∀l ∈ Δ ⟺ q⁻¹ ∈ ⋂ l Z_(l) = J(R)`), and every branch ring contains Z.
- **iff, direction witness ⟹ q ∉ Z**: the branch ring is `⋂_{l∈Δ} Z_(l)` with `q ∉ Z_(l)` for some prime
  `l`, and `Z = ⋂_p Z_(p)`, so `q ∉ Z`.
- **Count**: single `J_{a,b}` membership = 2 elements of `I^c_{a,b}`, each needing 2 `T^×` memberships,
  each `T_{a,b} = S_{a,b}+S_{a,b}` with `S_{a,b}` = 4 witnesses ⟹ ≈16 vars per `T^×`, ≈64 per `I`, ≈128
  per `J`, ≈256 per `J(R)`; ×3 branches + `Φ_k`/`Ψ` witnesses ⟹ **k ≈ 3·10² – 1.5·10³**.
  Honest range, staged; Koenigsmann never states his `n` (**literature GAP**), so this is our derivation.
- **Board score: N/A.** It defines `Q∖Z`, not `Z`. Complement of Σ₁ is Π₁ — this can never be converted.
- **Value**: it is the *only* unconditional, citable artifact in this problem space, and its count is
  < 4,973 — i.e. cheap to certify relative to the incumbents.

### C2 — Poonen 2009 / Koenigsmann Step 1: ∀∃ with 7 witnesses
`t ∈ Z ⟺ ∀a,b ∃x₁..x₄,y₂..y₄ (a+Σx²)(b+Σx²)[(x₁²−ax₂²−bx₃²+abx₄²−1)² + ((t−2x₁)²−4ay₂²−4by₃²+4abx₄²−4)²] = 0`
(Koenigsmann §2 Step 1; degree **8** vs Poonen's 9244; Poonen AJM 131 (2009) 675–682.)
Koenigsmann Cor 21: a ∀∃ version with **one** universal quantifier — sharpest published complexity.
- **Board score: N/A** — the two `∀` are not existential in `w`. Removing them *is* the open problem.
- **Its real use**: it is the engine C3 must bound. 7 witnesses is the floor *if* the ∀ ever vanishes.

### C3 — bounded-catalogue Σ₁ (the incumbents' axis; our own re-derivation)
Replace `∀a,b` by a finite catalogue using: 5-point height estimate `h(s) ≤ H·M(s)^c` + prime-pattern
theorem + pole-parity condition (OpenAI preprint §4, §6, §3; primary sources: odd regular Fontaine–Mazur
at 2, pointwise 2-converse, Cassels–Tate).
- **iff, q ∈ Z ⟹ witnesses**: local witnesses exist at every catalogue prime by Hasse–Minkowski
  (Koenigsmann Fact (e), itself `S_{a,b}(Q) = Q ∩ ⋂_p S_{a,b}(Q_p)`).
- **iff, witnesses ⟹ q ∈ Z**: contact-prime divisibility at precision K + the height bound force
  every modelled coordinate into an ordinary finite interval, so `q ∈ ⋂_p Z_(p) = Z` (OpenAI §1 last
  three paragraphs — this is the hard direction and it is where all the arithmetic lives).
- **Count**: `k = Θ(|catalogue|)`, linear. Confirmed by the incumbents' own public text: W = 185640,
  36,864 unit classes, **811,008 selected primes**, H = 23,150,593, `T < 2^(2^(2^9013))` (dated) →
  292,890,231,905 vars; PR #1 shrank the catalogue → **211,983,774,909 (−27.62%)**. After the quartic
  normal form the same object is 4,973.
- **Board score: 4,973 (bar).** Within 10× — but only by shrinking `|catalogue|`, i.e. by improving `H`.

### C4 — universal-pair route: **does not exist**. Kill it.
A universal Diophantine pair (Jones 1982: **(58,4) over N**; Matiyasevich–Robinson 13 vars; Sun 1992:
**11 vars for Z**; Matiyasevich 9 vars at degree ~1.6·10⁴⁵) encodes *r.e. sets of integers*, not
"q ∈ Z inside Q". `Z` is r.e. as a subset of itself, so universality gives nothing here. Recorded as a
refuted candidate so nobody in the campaign spends a day on it.

## 2. CORRECTNESS AUDIT OF THE INCUMBENTS (the first-class deliverable)

Source: `diophantine-zq/upstream/quartic_4973.tex` (719,455 chars, read via bounded windows) + its README.

The `thm:quartic` statement is verbatim:
> "**With precisely the inherited arithmetic hypotheses and qualifications** of Section deg8-original and
> Appendix sources, … For every `q ∈ Q`, `q ∈ Z ⟺ ∃(w₁,…,w₄₉₇₂) ∈ Q⁴⁹⁷², Φ(q,w) = 0`."

So the headline is conditional, and the conditionality is exactly where the Lean `sorry` sits.

- **Weakest link = `hyp:RC`** ("Restricted converse"), stated as a theorem:
  `∀ ℓ > 0 squarefree, ℓ ≡ 11 (mod 12):  corank_{Z₂} Sel_{2^∞}(E_ℓ/Q) = 1 ⟹ ord_{s=1} L(E_ℓ,s) = 1`,
  for `E_ℓ: y² = x(x−ℓ)(x+3ℓ)`.
  Why this is the break point: `corank Sel = 1` gives an **upper** bound (rank ≤ 1). Root number −1
  (their Selmer-parity step, Dokchitser–Dokchitser Thm 1.8) gives only *odd* analytic rank, i.e. ≥ 1 —
  which could be 3, 5, … To conclude `ord = 1` you need an **upper** bound on the analytic rank
  (`L′(E,1) ≠ 0`), i.e. the Gross–Zagier / Kolyvagin direction. The 133k-char RC section mentions
  **Gross 2, Zagier 2, Kolyvagin 2, Heegner 5** times and never invokes the GZ/Kolyvagin nonvanishing
  machinery as a hypothesis, yet claims the conclusion for an *infinite twist family* via
  "visibility (O.8)" + odd-limit-symbol/2-adic bookkeeping. Establishing this for a whole family
  unconditionally would be a major standalone result in arithmetic geometry. **This is where the hard
  direction breaks** (or, at minimum, where the entire burden is parked).
- **Second seam = `hyp:o8-height`** (the five-contact height estimate, `h(a) ≤ H_* M₅(a)²⁴`,
  `log₂ H_* < 4,783,227`). Their own words: *"This is a check of the number H, not a proof that H is a
  height constant"* and *"The finite coefficient calculation does not establish the height bound."*
  The height estimate is precisely what converts `∀` over contact primes into a finite box; if `H_*` is
  not proved to be a height constant, the box is not shown to be sufficient and the ∀ is not eliminated.
- **Third seam = `hyp:PC`** (pole completeness), proved *from* RC — so it inherits RC's break.
  Their own prose flags a domain mismatch: the pole lemma "is not inferred from `hyp:PC`, which has
  different variables and a **restricted completeness domain**".
- **Soundness direction is fine**: `lem:pole` (one-sided obstruction) has a short, checkable proof
  (parity of `v_p(x)` on the cubic at a unit parameter). So the cheap direction is proved; the
  expensive direction (existence) is where the debt lives. Classic.
- **Verdict**: the construction is arithmetic-characterization-conditional, and the conditionality is
  not a proof gap that more Lean work closes — it is the *mathematics*. Expect the `sorry` to persist.

## 3. LITERATURE PRECEDENT FOR THE QUARTIC FRONTIER (mission 2)
Yes, the frontier is rediscovery, and the precedent is textbook:
- **Davis 1973, Thm 7.5** — circuit normal form: one variable per gate, gate equations of degree ≤ 2
  (cited by the OpenAI preprint §7, which uses it to prove degree-≤4 completeness).
- **Jones 1982, *Universal Diophantine equation*, J. Symbolic Logic 47(3) 549–571, doi:10.2307/2273588**:
  "by introducing some 30 additional unknowns and new equations one can reduce the degree of the system
  to 2. **Then, by transposing terms to one side and summing squares one can construct a universal
  diophantine equation in 58 unknowns and degree 4**" — i.e. **(ν, δ) = (58, 4)**, the exact technique
  (sum of squares of quadratics) Glazer V4 uses. Jones also tabulates the ν/δ frontier: (58,4), (38,8),
  (32,12), (29,16), (28,20), (26,24), (25,28), (24,36), (21,96), (19,2668), (14,2·10⁵), (13,6.6·10⁴³),
  (12,1.3·10⁴⁴), (11,4.6·10⁴⁴), (10,8.6·10⁴⁴), (9,1.6·10⁴⁵). Best for *integer* unknowns: **11 variables
  (Zhi-Wei Sun 1992)**.
- **Formalization precedent**: *A Formal Proof of Complexity Bounds on Diophantine Equations*,
  arXiv:2505.16963 (2025), Isabelle/AFP — first machine-checked universal pair over Z, built on Jones'
  (58,4). This is the template for certifying a variable/degree pair.

## 4. HONEST VERDICT ON THE ROW
No theory route undercuts 4,973. C3 shrinks only with `|catalogue|`; C1/C2 define the wrong set or the
wrong quantifier shape; C4 is refuted. The bar moves because the *source system* is the currency and the
incumbents halve it by iterating on `H` and the prime catalogue — a number-theory input, not a
derivation. Lane A2 should bank (i) the C1 unconditional artifact (only certifiable object here) and
(ii) the `hyp:RC` audit, which is worth more to the community than 3% off 4,973.
