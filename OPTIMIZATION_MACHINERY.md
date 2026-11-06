# OPTIMIZATION_MACHINERY.md — Lane A3 (dzq-optimize)

Board `other-z-diophantine-in-q` (site commit f9fe0a4, 2026-11-06): minimize k+1 = #variables of
P(q, w_1..w_k) in Z[q,w] with q in Q: q in Z iff exists w in Q^k, P(q,w)=0. Ties: degree, then
nonzero terms, then max |coeff|. Incumbents (all Claimed, Lean sorry): Glazer 292,890,231,905;
qqwref 211,983,774,909; LEADER Conant–Farhangi–Freitag–Glazer–Park–Terry 12,504 vars, deg 4,
135,721 terms, max coeff < 2^80. Ranking contact: a72b58dd.

Every technique below is polarity-agnostic (works for Z or for Q\Z) and applies to ANY correct
construction. Cost notation: Δvars, Δdeg, Δterms.

--------------------------------------------------------------------
## 0. Canonical assembly and the variable ledger

Any finite ∃-system (E_1=0, …, E_r=0, G_1..G_s positivity/disequality gadgets) over Q assembles to

    P = Σ_j E_j² + Σ_i (G_i-as-equality)²          (∗)

P=0 iff every E_j=0 and every gadget holds (squares of rationals are ≥ 0; a sum is 0 iff all
terms are 0). So **conjunction is free** — all equations share one witness pool. Every witness
variable owes its existence to exactly four sources:

  (a) one ∃-quantifier of the source first-order definition;
  (b) a positivity gadget  t ≥ 0:  4 vars   [M2];
  (c) a disequality gadget t ≠ 0:  1 var    [M1, batchable];
  (d) private witnesses of an OR-branch                [M3].

Optimization = attack the four sources + prune. The (⇐) direction (w exists ⇒ q in Z) is where
the *mathematical* difficulty lives; the machinery below never weakens it — each move is an
if-and-only-if rewrite or a soundness-proved elimination.

## M1. Disequality batching — m disequalities cost 1 variable
    t_1,…,t_m ≠ 0   ⇔   ∃s: s·(t_1 t_2 ⋯ t_m) = 1.
(⇒ field is a domain, s = 1/∏t_i; ⇐ each t_i | 1.) Δvars: m → 1. Δdeg: +m. Sound both ways.
Beware edge case: an empty product is not usable (need m ≥ 1) and t_i = 0 kills the product
(s = 1/0 impossible) — correct.

## M2. Positivity gadgets — exact costs (proven)
  Weak:  t ≥ 0 ⇔ ∃a,b,c,d: t = a²+b²+c²+d².  4 vars, deg +2.
    (⇒ Hasse–Minkowski + Lagrange: t = m/n ≥ 0, mn = Σ4 int squares ⇒ t = Σ(m_i/n)².
     ⇐ squares ≥ 0. **Optimal among form representations**: 7 is not a sum of 3 squares of Q —
     mod-8 + infinite descent on the denominator (see PACKING_BOUNDARY B8).)
  Strict: t > 0 ⇔ ∃u,a,b,c,d: t·u² − 1 = a²+b²+c²+d².  5 vars, deg +4.
    (⇒ take u ∈ Z large with tu² ≥ 1. ⇐ tu² = 1 + Σ ≥ 1 > 0 and u ≠ 0 — note u = 0 is
     self-excluding (−1 = Σsq impossible), no extra disequality needed.)
  Disequality: t ≠ 0 ⇔ ∃s: ts = 1.  1 var, deg +1.

## M3. Disjunction accounting
  OR of two ∃-systems A, B with k_A, k_B witnesses: cost k_A + k_B (take the witness of the
  branch that holds, fill the other block with 0). Not shareable in general.
  Point-disjunctions on shared variables are FREE: (x=a_1 ∨ … ∨ x=a_m) ⇔ ∏(x−a_i) = 0:
  0 vars, Δdeg m. Mixed branch (∃ā: E=0) ∨ (x=a): product E·(x−a), cost k_A.
  Rule: DNF-normalize the base definition; fold every point-disjunction into factored form
  BEFORE assembly. Mechanical transforms routinely miss this.

## M4. Linear-unit elimination (the mechanical core)
If some equation is linear in a variable v with a unit coefficient — v = f(q, ŵ) — then
substituting v := f everywhere and deleting the equation is sound in BOTH directions:
∃(v,ŵ): P=0 ⇔ ∃ŵ: P[v:=f]=0, and (⇐) recovers v = f. Δvars: −1 each. Δdeg/Δterms: grow.
Iterate to a fixpoint. On mechanically generated constructions this alone typically deletes
a large fraction of transform-introduced auxiliaries (every Skolemized equality chain).

## M5. Dead-variable / tautological-cluster pruning
Delete (equation G, private vars U) when G=0 is solvable in U for EVERY valuation of the
remaining system (e.g. G = (v² + (f)² − (g)²) where v occurs nowhere else and f²+g² can be
nonneg… — decide per gadget: square-sum G=(t−Σu²) solvable iff t ≥ 0, so it is prunable only
if t ≥ 0 is forced elsewhere; G=(ts−1) solvable iff t ≠ 0). This is a DPLL-style fixpoint on
the gadget graph; sound because deleted constraints are satisfied by SOME U-extension of every
surviving valuation, so solution sets are unchanged. Run AFTER M4; this is where "billions
hide" in naive universal-polynomial specializations: unused branches of the FO formula leave
whole witness blocks that only ever need dummy values.

## M6. Parametrization-as-elimination (Q-specific lever)
Over Q, every conic with a Q-point is rational (Hasse for conics). If an ∃-variable is
constrained only by a parametrizable relation, substitute its rational parametrization and
delete the variable; Δdeg ×~2 per use. Example: the Pythagorean triple x²+y²=z², z≠0
disappears into (m²−n², 2mn, m²+n²). Corollary (anatomy review criterion): any construction
importing Z-style Pell x²−Dy²=1 "exponential sequence" gadgets is structurally broken over Q
— every rational Pell conic degenerates to a parametrized curve with no discrete structure.
Flag, don't repair: such a construction is evidence the (⇐) direction is not doing real work.

## M7. Witness-map discipline for the (⇒) direction
The easy direction (q in Z ⇒ ∃w) needs only ONE witness family. Design the system so every
E_j vanishes identically along an explicit rational curve w = f(q) for q ∈ Z (typically f ≡ 0
plus the "tracking" variables set to their defining values). Then (⇒) costs ZERO extra
gadget variables and needs no separate proof effort. Constructions that add post-hoc
"correctness witnesses" for (⇒) are paying for something the witness map gives free.

## M8. Base-definition surgery (the exponent of everything)
The source first-order definition determines (a)–(d) multiplicatively. Known bases, best to
worst:
  - Koenigsmann 2016 (Annals): Z is ∀-definable in Q; also an ∀∃-definition with ONE universal
    quantifier (arXiv:1011.3424). Transform cost from this base is the smallest known.
  - Poonen 2009 (Amer. J. Math.): Z is ∀∃-definable.
  - Julia Robinson 1948/49: full FO definition via her induction formula
    θ(r) = ∀y∀z[φ(0,y,z) ∧ ∀w(φ(w,y,z) → φ(w+1,y,z)) → φ(r,y,z)],
    φ(r,y,z) = ∃a∃b∃c(2 + yzr² = a² + yb² − zc²) — several alternations; a naive MRDP
    transform of THIS base is plausibly where the 2e11 rows came from.
Specialize, never universalize: the board needs ONE predicate. Jones' universal polynomial
(1982) exists at (ν,δ) = (9, 1.64·10^45), (58, 4), (13, …) over N (Jones–Matijasevich–Robinson
13; Matiyasevich 9; Jones 58 @ deg 4; Bayer–David ITP 2025 formalized (9,1.64e45) in
Isabelle). Universality overhead (tape/cell/register encodings) is dead weight for a fixed
predicate — M4/M5 delete it. The leader's degree-4 12,504-var shape is consistent with a
specialized Hasse–Minkowski/norm-form core (cf. Koenigsmann's T_{a,b} quaternion-norm rings).

## M9. Structural review criterion (for incumbent-anatomy lane)
Any construction whose skeleton quantifies over primes cannot close (FO definitions of
subsets of Q quantify over Q-elements only — Koenigsmann's paper is explicit). A correct
definition must be a FINITE algebraic core (local conditions folded into quaternion
norm-form equations, Sun-style). Also flag: Pell/growth gadgets (M6), post-hoc (⇒) witnesses
(M7), unnegated ∀-blocks left in the ∃-system.

## M10. Tie-breaker ledger
  - Sum-of-squares assembly (∗) doubles degree. Minimum-degree single-polynomial conjunction
    over Q is OPEN (any P with P=0 ⇔ E_1=0 ∧ E_2=0 and deg P < 2·max deg E_i is unknown to
    us; cf. effective Nullstellensatz bounds). Variables dominate the board order anyway.
  - M4 substitutions multiply degrees (deg P' ≤ deg P · deg f). Parametrizations ~×2.
  - Term counts blow up as (terms)² under squaring; the leader's 135,721 terms at deg 4 is a
    hand-compressed shape that mechanical assembly will not match — term hygiene is a
    post-pass (factor, collect, drop zero coefficients), tertiary priority.

## 11. Proven floor and the real frontier
PROVED (PACKING_BOUNDARY B9): no definition with k = 0 or k = 1; **score ≥ 3**.
No obstruction known at k = 2 (score 3). Literature anchor: the COMPLEMENT polarity
Q∖Z is diophantine with **7** witnesses (Sun 2026, improving Daans 2024's 10; both via
Koenigsmann's norm-form local rings). Every technique above should be measured against the
k=2 horizon, not against 12,504.

## 12. Recommended pipeline (hand to constructions lane)
 1. Take the best base definition (M8: Koenigsmann ∀∃ one-universal-quantifier form, or the
    leader's own core if it can be re-derived).
 2. DNF-flatten; fold point-disjunctions (M3). Design the witness map (M7).
 3. Eliminate ∀ via: ∀x φ ⇒ ¬∃x ¬φ; ¬(E=0) ⇒ E·s=1 (M1 batching); positivity via M2.
 4. Assembly (∗). Then M4 to fixpoint, M5 prune, M4 again.
 5. M6 opportunistic parametrizations. Tie-breaker pass (M10).
 6. Every step carries a two-line soundness certificate (for the Lean lane).

## 13. Caveat on the race itself (coordinator should know)
Koenigsmann 2016 §(Thm 4/last section): **conditional on a strong Bombieri–Lang variant,
Z is NOT existentially definable in Q** (Mazur 1992 predicted no; board statement cites
both). The three rows are Claimed with a sorry in the Lean main theorem. Under BL the race
may be unwinnable regardless of optimization; the machinery remains valid for the complement
polarity (Q∖Z, where n=7 is the record) and for any correct ∃-definition should BL fail.
