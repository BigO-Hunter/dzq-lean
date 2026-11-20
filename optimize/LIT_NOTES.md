# LIT_NOTES.md — Lane A3 (dzq-optimize)

Verification legend: [FETCHED] = abstract/page retrieved this session; [SECONDARY] = seen in a
retrieved source's text/references; [GAP] = could not fetch, cite with care.

## Board / race
- [FETCHED] bigospeedrun/site commit f9fe0a4 (2026-11-06 15:39Z, author nil + claude):
  "Other bounds: add the race Z is Diophantine in Q (Nil, 2026-11-06; ask a72b58dd for the
  ranking)". Rows: Glazer et al. 292,890,231,905 vars (repo elliotglazer/diophantine-z-q
  bdc5f4aa, 11-04); qqwref 211,983,774,909 (PR #1, 11-05); LEADER Conant, Farhangi, Freitag,
  Glazer, Park, Terry 12,504 vars, deg 4, 135,721 terms, max coeff < 2^80 (release
  quartic-12504-version-2, 11-06 02:59Z). All Claimed; "the Lean development's main theorem
  still has a sorry". Statement context cites Koenigsmann 2016 and Mazur 1992 (predicted no).

## Definability of Z in Q (the base-definition supply chain)
- [FETCHED] J. Koenigsmann, "Defining Z in Q", Annals of Math. 183 (2016) 73–93;
  arXiv:1011.3424. Z is ∀-definable in Q; an ∀∃-definition with ONE universal quantifier;
  Q∖Z diophantine; nonsquares diophantine (elementary proof); NO existential definition of Z
  in Q under a strong Bombieri–Lang variant. Machinery: local rings Z_(p) via quaternion
  norm-form sets T_{a,b} and R^[3],R^[5],R^[7],R^[1]_{p,q} = norm-form sums; explicit
  criterion for Δ_{a,b} at p=2. [FETCHED, annals-v183-n1 PDF + arXiv abs]
- [SECONDARY] B. Poonen, "Characterizing integers among rational numbers with a
  universal-existential formula", Amer. J. Math. 131 (2009) 675–682. Predecessor ∀∃-definition.
- [SECONDARY] Julia Robinson (1948/49): first FO definition of Z in Q; formula θ via
  φ(r,y,z) = ∃abc(2 + yzr² = a² + yb² − zc²) and induction [Carol Wood's slides, FETCHED].
- [SECONDARY] J. Park, "A universal first-order formula defining the ring of integers in a
  number field", Math. Res. Lett. 20 (2013) 961–980. (Number-field generalization; note Jenn
  Park is on the board's leader row.)

## Variable-count state of the art (the lane's home literature)
- [FETCHED] Z.-W. Sun, "Q∖Z is diophantine over Q with 7 unknowns", arXiv:2607.28606
  (30 Jul 2026). n = 7 for Q∖Z (and any global field), improving:
- [SECONDARY] N. Daans (2024), record n = 10 for Q∖Z [London Math. Soc. 109 (2024) e12864,
  seen in Sun's refs].
- [FETCHED] N. Daans, P. Dittmann, A. Fehm, "Existential rank and essential dimension of
  diophantine sets", arXiv:2102.06941 (v5 2025). Minimal number of ∃-quantifiers ("essential
  dimension of the functor of points") — THE academic formalization of this board's score.
  Also: N. Daans, "Universally defining finitely generated subrings of global fields",
  Doc. Math. 26 (2021) 1851–1869 [SECONDARY].
- N. Daans, P. Dittmann, A. Fehm, quantitative version w.r.t. variable count for general
  fields: [GAP — not fetched, title/inference uncertain; the 2102.06941 abstract is the
  verified anchor.]

## Universal-polynomial variable counts (universality overhead reference)
- [FETCHED] J. P. Jones, "Universal Diophantine Equation", J. Symbolic Logic 47 (1982)
  549–571: 58 variables, degree 4 (sum of 37 equations in 53 unknowns + ~5 params; the
  MO/JSL commentary cites "37 equations in 53 unknowns", and Jones 1980 Bull. AMS
  "Undecidable Diophantine Equations" [FETCHED] states 58 unknowns degree 4 explicitly,
  and the table: Matiyasevich ν = 9 at δ ≈ 10^45; Robinson–Matijasevich ν = 13).
- [FETCHED] J. Bayer, M. David, "A Formal Proof of Complexity Bounds on Diophantine
  Equations", ITP 2025 / arXiv:2505.16963: Isabelle/HOL formalization that (ν,δ) = (9,
  1.64·10^45) is universal over N (Jones' pair), with a reusable substitution/degree/variable
  library — directly reusable by the dzq-lean lane as a harness reference.
- [SECONDARY] Matiyasevich: 3-variable EXPONENTIAL diophantine universality (1979), via
  Wolfram NKS notes [FETCHED].

## Local-global / forms (gadget theory)
- [SECONDARY] Hasse–Minkowski theorem for quadratic forms (Serre, "A Course in Arithmetic",
  ch. IV) — basis of M2 (positivity = 4 squares over Q).
- [SECONDARY] Lagrange four-square; Legendre three-square (7-mod-8 obstruction) — B8 proof.
- [SECONDARY] Faltings' theorem (Cornell–Silverman, "Arithmetic Geometry") — B9 genus ≥ 2.
- [SECONDARY] Elliptic divisibility sequences / denominator growth of x(nP) (Silverman,
  "The Arithmetic of Elliptic Curves"; Ward 1987) — B9 genus 1 step. Formal citation for the
  exact "den(x(nP)) = ψ_n(P)²" form: Everest–van der Poorten–Shparlinski–Ward, "Recurrence
  Sequences" (AMS, 2003), ch. 3 [SECONDARY — check before Lean use].

## Pairing / injections (B1–B2 boundary)
- Poonen on polynomial injections of rational points and the open polynomial-injection Q²→Q
  problem: Poonen, "Undecidable problems: a sampler" (Bull. London Math. Soc. / AMS survey)
  [GAP — not fetched this session; the Friedman open problem status is common knowledge in
  the area but the lane flags it for a coordinator-side double-check].
- B1 (no polynomial pairing with polynomial decode) is lane-original, one-line algebra
  (subalgebra/dimension argument) — no citation needed.

## Unprovability context
- [FETCHED] Koenigsmann (Annals 2016): ∃-definition of Z in Q would refute a strong BL
  variant; Mazur 1992 conjectured no ∃-definition. Board statement echoes this. Hence the
  three Claimed rows stand against a conjectural no-go; the sorry is not cosmetic.
