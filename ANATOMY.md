# ANATOMY — Strike Lane A1 (updated 2026-11-06, post-collapse)

## Lineage
| version | date | total vars | locals | final SoS residuals | slack (vars−resid) |
|---|---|---|---|---|---|
| huge (Glazer 11/4) | 11-04 | 292,890,231,905 | 1,305,811 src ops | n/a (not SoS) | — |
| base compiler F8 (deg 8) | — | 15,671 | — | — | — |
| v2 | 11-06 02:59Z | 12,504 | 12,038 | 11,939 | 565 |
| v3 | 11-06 14:17Z | 9,625 | 9,291 | 9,161 | 464 |
| **v4** | 11-06 15:49Z | **4,973** | 4,908 | **4,552** | 421 |

All quartics: deg 4, SoS with ALL WEIGHTS = 1, Φ = Σ R_i², R_i ∈ Z[·] deg ≤ 2,
max |coeff| < 2^80. v4: 72,925 monomials, max coeff 685,783,949,153,203,534,233,890.

## V4 structure (one paragraph)
The polynomial is Φ(X_0..X_4972) = Σ_{i=1..4552} R_i², weights all 1, from
`residuals.json.gz` (4,552 nonzero integer residuals, deg ≤ 2), reached from a
pinned arithmetic source system via `certificate.jsonl.gz`: 551 projection-preserving
transformations (266 invertible linear row ops, 148 eliminations modulo retained
equations, 121 rational definition eliminations, 13 contact-power circuit
replacements r^2,r^24,r^80, 2 shears, 1 height-parity block replacement:
8 old vars t,U,e,p,q,s,h → 12 vars/9 quadratics u,v,a,z,e,p,c,w,s,q,j,k, verified
by explicit conic identity u²+bv²=b² ⟺ old first residual). The SOURCE system
(construction-map.json, 115 instantiations, 4,908 locals) is the arithmetic core
of the huge construction stripped of the machine: 37 contact sites comparing
points on the fixed elliptic curve over Q(√2) (codes: 2E(K)=Z·P0), plus
Z_definition frame (212), anchor (4), height_batch (26), primeparity (7).
Arithmetic (not certificate-checked; proved in manuscript §"Arithmetic source"):
x∈Z ⟺ the comparison system is satisfiable; sum-of-squares makes Φ=0 ⟺ all
residuals vanish over Q. Input = coordinate 0; projection equality is the
certificate's job; the integer characterization is the manuscript's.

## V4 module ledger (per-site, 37 sites)
| mode | sites | per-site cost | composition |
|---|---|---|---|
| full | 13 | 159 | q_compare4 97 + q_conic13 52 + q_linearnormalpole 10 |
| lucas | 16 | 131 | q_compare_lucas 82 + q_conic10 39 + q_linearnormalpole 10 |
| beta | 8 | 62 | q_compare_beta 27 + q_conic6 25 + q_linearnormalpole 10 |
| fixed | — | 249 | Z_def 212 + anchor 4 + height_batch 26 + primeparity 7 |

## V3→V4 delta (9,625 → 4,973, −4,652 = −48.3%) — THE trick on the board
v3 had only 2 modes: 29 full sites (q_compare4 217 + q_batch41 55 + q_primeparity 7
= 279/site) + 8 beta sites (q_compare_beta 76 + q_batch17 25 + q_primeparity 7 =
108/site) + fixed 329. Five mechanisms bought −48%:
1. **Three-mode coverage** (−2,368): 16 of 29 full sites demoted to Lucas-only.
   Lucas test ℱ(s,t,z)=t²−s(s−2)tz+(s−2)²z²−1 (3 quadratic eqs, order-40 local
   quotients) replaces the full 4-index comparison. Sound: Lucas contacts cover
   S,T,Z; beta covers A,T (each point covered ≥ once — that's all the height
   argument needs). Full survives only at contacts 0–4, 21–28.
2. **Private conics + packed field tests** (batch41/batch17/primeparity machinery
   −1,795−259 net): per contact, conic θ²−rS_c=2 with locals θ,s_c,S_c; required
   field-element divisibilities packed into ONE norm-form tree N_r(u,v)=u²+rv²
   per site; ordinary-pole lemma (p>76176) replaces the 41-catalogue-prime
   sieve. primeparity: 38 sites×7 → 1×7, folded into q_linearnormalpole (10/site).
3. **General root carrier + doubled targets** (compare4 217→97, i.e. −1,560 over
   13 full sites): roots may be ANY nontorsion points; indices = integer doubled
   indices 2Q=n_Q·P_*, h(x(Q))>n_Q²/4−4; charts retain x,y,q=x² only,
   y²=xq−Dx. Halves coordinate blocks; kills half-integer index handling.
4. **Shared field squares** (−within conic): common field F=a+b√2, bind once
   c=a²+2b², d_s=2ab, replace packed Y=a+θb, PW=2aY−a²+2b² by PW=c+θd_s —
   projection-preserving, reuses an already-available primary-f square.
5. **First-norm denominator fusion + direct tangent fusion** (−within conic/pole):
   first virtual denominator W_0=T_0/r² → T_0/r and rN−r−T_0²=0; order-e test
   needs only v_p(T)≥2e−1. Denominators fused into first-norm blocks.
Then the 551-transform certificate compiles the revised source to exactly the
4,552 quadratic residuals. Savings decomposition: demotion 2,368 + full-site
cheapening 1,560 + beta cheapening 368 + fixed-frame 80 + primeparity-fold 259
+ remainder ~25 (rounding/overhead).

## The 2,486 target
v4 README, verbatim: "The next manuscript version requires at most **2,486
total variables**, half the Version 4 count rounded down. This is a search
target, not a result." → **arbitrary halving goal, no known mechanism shipped.**
Both incumbents ship releases ~90 min apart; v4 landed 15:49Z.

## HYPOTHESIS-CHAIN (conditional surface map — for certificate + compression lanes)
Theorem reads "With precisely the inherited arithmetic hypotheses and
qualifications." The chain, bottom-up (tex refs to v4 manuscript):

1. **lem:pole (line 1003) — PROVED, unconditional.** One-sided obstruction:
   B≠0 ∧ Φ(B) ⟹ v_p(B) not negative-odd for p∉S_0. This is the pure
   soundness engine: no witness-existence claim. Enters residuals wherever a
   pole predicate Φ(R/Θ²) is imposed (huge-construction §6 "require them
   nonzero and impose Φ(R/Θ²)"; quartic: the ordinary-pole part of
   q_linearnormalpole, 37 sites × 8 = 296 residuals, + norm-tree valuations
   at p>76176). **Residuals leaning only on lem:pole are hypothesis-free on
   the soundness side.**
2. **hyp:o8-height (6670) — CHECKED CONSTANT, numerically verified, not
   conjectural.** h(a) ≤ H_*·M_5(a)^24 for a∉D; H_* =
   2(4608^165888+6^100)·B_*^24+128, B_* = ∏_{p≤76176} p, log2 H_* <
   4,783,227; five contacts {∞, 0, 1, 2401, −343/32}; M_5(a) = product of
   primes outside S_* with odd contact multiplicity (degree8-original/
   arithmetic/assumption-status.json, status: independently reviewed,
   open_obligations: []). Enters: q_height_batch (26 locals), the
   parity/denominator boundary residuals (§8525, 8555), frame constants
   S_*, D, M_5 (§8739), and every p>76176 threshold. Assumption-status
   explicitly: "log2(H) < 4783227 does not prove the height assertion."
3. **hyp:PC (1016) — PROVED FROM RC + lem:pole** (§1032–1135 exact descent,
   applies RC to n and nθ). Pole completeness: 0<B<1/2, square denominator,
   v_p(B)≥4 on S_0 ⟹ Φ(B). Supplies the pole WITNESSES (Θ=Tr(W⁻¹)≠0,
   B_pole=R/Θ², §6248 "Theorem hyp:PC supplies the pole witnesses") — i.e.
   the q∈Z ⟹ ∃w direction.
4. **hyp:RC (1020) — THE conditional core.** For squarefree ℓ≡11 mod 12:
   corank_{Z₂}Sel_{2^∞}(E_ℓ/Q)=1 ⟹ ord_{s=1}L(E_ℓ,s)=1 (curves: c_4=208ℓ²,
   Δ=2304ℓ⁶, j=35152/9, non-CM). Proved (conditionally) in §sec:rc–sec:limits;
   consumes classical inputs: Rankin factorization, L(E^k,1)≠0,
   finite-Σ/Sha sign discard (§5752, §14574), + the manuscript's Heegner
   descent/Kummer/determinant-transfer constructions. Non-CM vs CM generator
   branch kept separate. **Enters the residual system ONLY transitively
   through PC**: the pole-witness blocks (Θ/B_pole residuals inside
   q_linearnormalpole + the pole instances of the comparison machinery).

**Lane implications.** Certificate lane: expose exactly {RC's classical
inputs, RC-instance ⇒ PC descent, o8-height constant check}; the finite
checks (verify_certificate.py) prove NONE of {RC, H5, the characterization}
(assumption-status `finite_checks_do_not_prove`). Compression lane: residuals
whose EXISTENCE (completeness) needs PC←RC are the pole-witness blocks —
removing/merging a pole instance changes the conditional surface (one fewer
PC/RC application); soundness-side residuals (lem:pole-only) can be
compressed without touching the hypothesis set; height residuals are exposed
to o8-height's constant, so conic/norm rewrites that keep the p>76176
threshold and M_5 shape inherit the same hypothesis, while any change to the
contact set {∞,0,1,2401,−343/32} reopens hyp:o8-height (this is exactly what
T2 in COMPRESSION.md does — flag it as conditional-surface-touching).

## RECIPE: catalogue→quartic (2.9e11 → 12,504) — body wealth

1. **Cut the machine.** Huge P = elliptic-curve label model + universal
   register-machine interpreter specialized to a fixed program. 96.2% of its
   variables = 15,845 `power_value` (base^exponent) calls × 17,786,698 witnesses;
   each elliptic point-op dragged ~224K witnesses (27 slope-certs × 1,298 each;
   slope = 8 test_groups of 162). The quartic lineage keeps ONLY the label core:
   a FIXED finite comparison of contact points + one Lucas equation + five-contact
   height estimate (base compiler F8, deg 8, 15,671 vars).
2. **Cut the cutoff & catalogue.** Huge construction's finite false-triple guard
   (one quadratic factor per false triple in [−T,T]³, degree ≤ 12T+3,
   T = (96·10^13)^13·2^8861398783796 ≈ 2^6.45M) and the 811,008-prime catalogue
   (W=185,640) for the six-contact/pole completeness machinery — all gone.
   Quartic needs: 5-contact height estimate, exceptional primes p>76176,
   bounded contact set. The T-cutoff existed to make the guard finite; without
   the guard, no cutoff, no catalogue, no sieve asymptotics.
3. **Sum-of-squares compile.** F8 (deg 8 SoS) → reciprocal revision → quadratic
   lift (targets for products) → certified reductions (row ops / eliminations /
   shears / circuit rewrites, each with polynomial-identity certificates checked
   by `verify_certificate.py`) → deg-4 Σ R_i². Machine-checked projection
   equality is what lets them iterate versions ~90 min apart.
4. **Then v2→v3→v4** are source-revision sweeps (batching, demotion, chart
   sharing) of the SAME skeleton, each re-certified.

## Historical appendix — huge-construction variable ledger (pre-collapse lane)
- 96.2%: 15,845 × power_value @ 17,786,698 = 281,830,229,810 (interpreter's
  base^exponent certificates; 82 src ops: 190 muls + 196 adds on point codes).
- 1.2%: 98,382 multiplications @ 35,134 = 3,456,553,188.
- ~2.6%: 125,327 adds + 54,056 var setups + wrappers ≈ 7.6e9.
- Atom chain: test_group(162) → slope(1,298) → height_certificate(35,106) →
  multiply(35,134=27 slopes+28) → natural(140,604=4×35,106+180) → power_value.
- qqwref delta (292.9e9→212.0e9, −80.9e9): Lagrange 4-square → Legendre
  3-square nonnegativity (8n+3=x²+y²+z²): −35,100/natural test; ~140 tests per
  power_value → −4.92M/call; ×15,845 = −77.9e9; rest from natural tests outside.
  Plus interpolation guard (deg O(T³)→O(T), 1 witness: no variable change) and
  catalogue/cutoff shrink (no variable change). PR#2 (−60.8e9): square(A,A,C)
  certificate sharing (−11,708/square; 77 squares per power + 54,052 outer) +
  program compaction 146,779→93,880 instructions (no variables; enabled U bound).
- Lesson: per-op witness blocks × op count = the whole game; both qqwref levers
  were "share identical conjuncts" and "cheaper positivity encoding" — the same
  two lever classes v3→v4 uses at residual scale.
