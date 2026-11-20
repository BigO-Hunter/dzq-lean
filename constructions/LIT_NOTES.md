# LIT_NOTES — z-diophantine-in-q, lane A2 (independent constructions from theory)

All claims below were read in the cited source text (arXiv HTML / LaTeX source / repo README),
not inferred from the task brief. Where the brief and the source disagree, the source wins and
the disagreement is recorded.

## 0. THE BRIEF IS INVERTED — read this first

The brief says: *"Koenigsmann 2016 proved Q\Z is Diophantine in Q — i.e. Z IS Diophantine in Q —
answering Mazur 1992 (who predicted no)"*. That is **wrong on both clauses**. From
Koenigsmann, *Defining Z in Q*, Ann. of Math. 183 (2016) 73–93, doi:10.4007/annals.2016.183.1.2
(arXiv:1011.3424v2), §1 (verbatim):

> "it is still open whether Z is existentially definable in Q, and, in fact, towards the end of
> the paper we provide a reason why it should not (Corollary 23)."

- **Theorem 1** (p. 2): Z is definable in Q by a **universal** formula: `t ∈ Z ⟺ ∀x₁…xₙ ∈ Q, g(t,x) ≠ 0`.
- **Corollary 2**: `Q∖Z` **is** Diophantine. (Proof = the negation of Theorem 1: `t ∉ Z ⟺ ∃x g(t,x)=0`.)
- **Corollary 23** (§4): assuming a strong Bombieri–Lang conjecture, **no infinite subset of Z is
  existentially definable in Q**; in particular Z is *not* Diophantine in Q.
- The brief's "Q\Z is Diophantine ⟹ Z is Diophantine" is not a valid inference: a set and its
  complement are independently Σ₁/Π₁; Z is Π₁ here, not Σ₁.

Consequence for the lane: the row's target (an *existential* / Diophantine definition of Z in Q) is
an **open problem**, expected **false**. Any submitted polynomial is a conditional claim, on pain of
refuting strong Bombieri–Lang. This reframes every count below.

## 1. PRIMARY SOURCES AND WHAT EACH ACTUALLY GIVES US

### 1.1 OpenAI, *Hilbert's tenth problem over the rational numbers*, preprint, 6 Oct 2026
Repo: github.com/openai/math → `preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026/`
(LaTeX source read from `build/sections/*.tex`; local copies in `lit/`.)

- **Theorem 1.1** (`main`): H10 over Q is undecidable — no algorithm decides rational solvability.
- **How**: a *finite-test* reduction (not a Diophantine definition): `f` has an integer zero ⟺ every
  test in an effectively generated sequence succeeds; compactness + elementary extension + elliptic
  heights; a failed test exists whenever `f` has no integer zero.
- The introduction **explicitly does not produce an existential definition** — it says so both in §1
  ("do not supply the existential membership condition for the direct transfer above") and, decisively,
  in §7: *"it gives no single existential definition of Z in Q."*
- **§7 Corollary (degree normal form)**: (i) rational solvability for polynomials of total degree ≤ 4
  is already 0′-complete; (ii) same for "is `Σᵢ qᵢ²  = 0` solvable" with each `qᵢ` quadratic.
  Proof technique that matters to us: encode the circuit, one variable per gate, then
  `∧ᵢ (qᵢ = 0) ⟺ Σᵢ qᵢ² = 0` over Q. **Degree 4 is free; the only currency is variables.**
- Also: Mazur's conjecture *"would rule out a Diophantine definition of Z in Q"* (§1) — i.e. the
  OpenAI proof deliberately routes *around* the open problem.
- What it gives our lane: the four arithmetic inputs that any *effective/bounded* version needs —
  (a) 5-point height estimate (§4), (b) prime-pattern theorem + simultaneous local witnesses (§6),
  (c) pole-parity / 2-descent condition using pointwise 2-converse + Cassels–Tate (§3),
  (d) rank-one + local elliptic results (§5). These are the hypotheses a conditional construction must name.

### 1.2 Koenigsmann 2016 (above)
- **§2 Step 1** (à la Poonen): explicit formula, degree **8** (Poonen's was **9244**):
  `t ∈ Z ⟺ ∀a,b ∃x₁..x₄,y₂..y₄ (a+Σx²)(b+Σx²)[(x₁²−ax₂²−bx₃²+abx₄²−1)² + ((t−2x₁)²−4ay₂²−4by₃²+4abx₄²−4)²] = 0`
  — 2 ∀ + **7 ∃**, all witnesses explicit.
- **§2 Step 2–3**: `Z_(p)` and its **Jacobson radical** `J(R)` are Diophantine, uniformly in rational
  parameters `p,q` (`Φ_k`, `Ψ`, `R_p^[k]`, `R_{p,q}^[1]`).
- **§2 Step 4 (Lemma 17)**: the key trick — `R̃ := {x : ¬∃y ∈ J(R), x·y = 1}` is **universal** and
  `R̃ = ⋃_{l∈Δ} Z_(l)`. This converts ∃-definitions into ∀-definitions.
- **Proposition 18(b)**: the explicit universal definition
  `Z = Z̃_(2) ∩ ⋂_{k=3,5,7} ⋂_{p∈Φ_k} R̃_p^[k] ∩ ⋂_{(p,q)∈Ψ} R̃_{p,q}^[1]`.
- **Corollary 21** (§3): a ∀∃-formula for Z with **exactly one** universal quantifier — the sharpest
  published quantifier complexity.
- **GAP**: `n` in Theorem 1 is never given a value ("there is a positive integer n"), and no explicit
  `g` is written down. So the *literal* variable count of the paper's own definition is a literature gap
  that our lane has to derive (see CONSTRUCTIONS C1).

### 1.3 Poonen 2009, *Characterizing integers among rational numbers with a universal-existential formula*,
Amer. J. Math. 131(3) (2009) 675–682, doi:10.1353/ajm.0.0057 (arXiv:math/0703907).
- ∀∃ definition, **2 ∀ + 7 ∃**, degree 9244. Mechanism: `Z = ⋂_{a,b>0} T_{a,b}` with
  `T_{a,b} = S_{a,b}+S_{a,b}+{0,…,2309}` — note the finite constant 2309, an early instance of the
  "pay for a ∀ with a finite enumeration" trade our lane is optimising.

### 1.4 Mazur 1995, *Speculations about the topology of rational points: an up-date*, Astérisque 228
(1995) 165–181 (numdam AST_1995__228__165_0), Conjecture 3: the closure of a Diophantine subset of Q in
R has finitely many connected components. Since Z is discrete and infinite, this **rules out** Z being
Diophantine in Q. (The earlier 1992 *Experiment. Math.* paper is the origin; OpenAI's bibliography,
which I read, cites the 1995 Astérisque as `Mazur1995`.)

### 1.5 Daans–Dittmann–Fehm, *Existential rank and essential dimension of diophantine sets*,
arXiv:2102.06941v5 — **the correct framework for this row's metric**.
- Defines `rk^∃_K(D)` = min number of existential quantifiers needed to define a Diophantine set D over K,
  and `efd_K(D)` (essential fibre dimension), and proves `rk^∃_K = rk^{∃+}_K` except for the 0/1 corner.
- Meaning for the board: SCORE = `rk^∃_Q(D) + 1` (input variable included). This is a *named, studied*
  invariant — the board is optimising a published quantity, so any count should be reported in its terms.

### 1.6 Koymans–Pagano, *Hilbert's tenth problem via additive combinatorics*, JAMS 2026,
doi:10.1090/jams/1081 (arXiv:2412.01768); Alpöge–Bhargava–Ho–Shnidman, Invent. Math. 243 (2026)
1129–1139, doi:10.1007/s00222-025-01392-3.
- Z is Diophantine in the *ring of integers* of every number field — those are rings, not the field Q
  ("Q is not a finitely generated Z-algebra", OpenAI §1). **No transfer to Z-in-Q.**

### 1.7 Poonen 2003, *H10 and Mazur's conjecture for large subrings of Q*, JAMS 16(4) 981–990,
doi:10.1090/S0894-0347-03-00433-8 — Diophantine *model* of Z in `Z[S⁻¹]` for a density-one recursive S.
Proper subring; does not give Q.

## 2. INCUMBENT NUMBERS — what I verified
- `qqwref/diophantine-z-q` PR #1 (closed, 2026-11-05), body read: "**211,983,774,909 total variables
  (27.62% fewer)**; the dated construction has **292,890,231,905** variables and `T < 2^(2^(2^9013))`".
  → the brief's two incumbent numbers are the *dated* and *optimized* variable counts of the same
  prime-catalogue construction. Its own text shows the currency is the catalogue: `W = 185640`,
  36,864 unit classes, **811,008 selected primes**, `H = 23,150,593`, `T` a tower.
- `elliotglazer/diophantine-z-q` V4 (README read, dated 2026-11-06): quartic polynomial, **4,973 total
  variables** / 4,972 witnesses, degree 4, 72,925 monomials, 4,552 squared quadratic residuals,
  max |coeff| < 2^80. Two admissions in its own README: the certificate "do[es] not prove the source
  system's arithmetic characterization of the integers", and "The Lean formalization is incomplete …
  the main bounded-polynomial declaration still contains `sorry`". It is built on the OpenAI preprint,
  and its lineage includes S. Farhangi's *"A conditional Diophantine definition of Z in Q from four
  arithmetic inputs"* (11 Oct 2026) — i.e. the lineage is **conditional by construction**.
- Reading: the billions are a *catalogue* count (variables ≈ primes×local-data), the 4,973 is the same
  object after the quartic normal form. Both are conditional on arithmetic inputs, both have sorry.

## 2b. PRECEDENT FOR THE "QUARTIC FRONTIER" (verified by search, 2026-11-06)
The quartic normal form the incumbents headline is **classical**, not novel:
- **Davis 1973, Thm 7.5** (coordinate/degree normal form, one variable per gate) — cited by the OpenAI
  preprint §7, which uses it to prove degree-≤4 completeness of H10(Q).
- **Jones, *Universal Diophantine equation*, J. Symbolic Logic 47(3) (1982) 549–571,
  doi:10.2307/2273588**: "by introducing some 30 additional unknowns and new equations one can reduce the
  degree of the system to 2. Then, by transposing terms to one side and **summing squares** one can
  construct a universal diophantine equation in **58 unknowns and degree 4**." That is precisely the
  `Σ(residual)²` step Glazer V4 uses (4,552 residuals ⟹ degree 4, 72,925 monomials).
- Jones' ν/δ trade-off table (same paper): (58,4), (38,8), (32,12), (29,16), (28,20), (26,24), (25,28),
  (24,36), (21,96), (19,2668), (14,2·10⁵), (13,6.6·10⁴³), (12,1.3·10⁴⁴), (11,4.6·10⁴⁴), (10,8.6·10⁴⁴),
  (9,1.6·10⁴⁵). Best known for *integer* unknowns: **11 variables (Zhi-Wei Sun, 1992)**;
  Matiyasevich–Robinson 1975: 13.
- Machine-checking precedent: *A Formal Proof of Complexity Bounds on Diophantine Equations*,
  arXiv:2505.16963 (2025, Isabelle/AFP) — first verified universal pairs over N and Z.
Reading: the incumbents' *degree* is rediscovery; their only novel content is the arithmetic
characterization of Z, which is exactly the part their own README says the certificate does not prove.

## 3. SEARCHES THAT RETURNED NOTHING (recorded as GAPs, no citations invented)
- No published **explicit polynomial** for a Diophantine definition of Z in Q exists to cite: the
  OpenAI paper disclaims one, Koenigsmann states the problem open and (mod BL) negative, Mazur's
  conjecture forbids it. Any "explicit polynomial" in this space is a *conditional* claim.
- No arXiv hit combining "existential rank" + "diophantine" other than DDF (arXiv API: 1 result).
- Koenigsmann's explicit `g` and its `n`: not in the paper (GAP).
