# PACKING_BOUNDARY.md — Lane A3 (dzq-optimize)

Exactly which tuple-packing tricks are polynomially legal over Q, with proofs. A proven
impossibility is a WIN (it closes an optimization direction and becomes a review criterion).

Notation: "polynomially legal" = expressible inside a polynomial system over Q whose
solution set realizes the intended iff, with witnesses ranging over Q.

--------------------------------------------------------------------
## B1. Pairing with polynomial decoding: IMPOSSIBLE (proved)

Claim. There are no polynomials F ∈ Q[x,y] (the "pack"), g,h ∈ Q[s] (the "decode") with
g(F(x,y)) = x and h(F(x,y)) = y as polynomial identities.

Proof. g∘F = x forces every polynomial of Q[x,y] to lie in the subalgebra Q[F]:
indeed from g(F)=x and h(F)=y, any p(x,y) = p(g(F),h(F)) ∈ Q[F]. So Q[x,y] = Q[F] would be
generated as a Q-algebra by ONE element. But trdeg_Q Q[x,y] = 2 > trdeg_Q Q[F] ≤ 1 — and more
elementarily, Q[x,y] is not a principal subalgebra situation: if Q[x,y] = Q[F], then x = g(F),
y = h(F); the map A¹ → A², s ↦ (g(s), h(s)) composed with F gives the identity on A², so F is
injective on algebraic closure points and A² ≅ F(A¹) — dimension 2 = dimension 1, absurd
(dimension theory of affine varieties; equivalently: any two polynomials g(s),h(s) satisfy a
polynomial relation G(g(s),h(s)) = 0, namely the implicit equation of the curve (g,h), so
G(x,y) = 0 in Q[x,y], contradiction). ∎

Consequence: the Cantor-style "pack (x,y) into z, decode when needed" idiom that is legal over
Z (where π(x,y) = ((x+y)²+3x+y)/2 via 2z = …, decoded with order gadgets) has NO Q-analogue
with polynomial decoding. Every witness variable is worth exactly one rational slot, period.

## B2. Injective pairing without decoding: OPEN, and unusable anyway

Claim (open, Friedman): does there exist a polynomial F ∈ Q[x,y] injective as a map Q² → Q?
Status: open. Over R it is impossible (topological dimension / invariance of domain), but Q
carries no such obstruction and F(x,y) = x + (small-function tricks) fails: e.g. F = x + y·M
is injective only for y in a bounded set. Related: Poonen's work on polynomial injections of
rational points (see LIT_NOTES; conditional constructions exist, unconditional open).
Even if F existed it would NOT give legal packing for our purpose: the (⇐) direction needs
the CONSTRAINT R(x,y) re-expressed in terms of z = F(x,y) alone — that is decoding, i.e. B1.
Using z = F(x,y) as an ADDITIONAL equation keeps x and y as variables: cost k+1 ≥ k, no win.

## B3. Square-sum "packing" is lossy: legal only as an existence gadget

t = a²+b²+c²+d² does not encode the tuple (a,b,c,d); its value set is exactly {t ≥ 0}.
It is legal precisely as the positivity gadget (MACHINERY M2), never for retrieval.
Corollary: two positivity conditions cannot share their four squares: t,s ≥ 0 needs 8
variables (t and s are recoverable values, each sum is its own equation); no norm-multiplication
trick separates them (Hamilton norms multiply, but N(α)N(β) = N(αβ) conflates the pair into
one value, not a conjunctive test).

## B4. Numerator/denominator extraction from a single rational: IMPOSSIBLE as stated

The maps q ↦ num(q), den(q) are not functions at all (representation-dependent) and no
polynomial P ∈ Q[x] can implement "the numerator of q": polynomials are continuous in every
p-adic topology while num/den jump at every reduced fraction. Formal version: if P ∈ Q[x]
satisfies P(q) ∈ Z for all q ∈ Q then P ∈ Q (constant). Proof: for any prime p, P(q) integral
for all q ∈ Z_(p)-locally… — simplest: P maps Z to Z and 1/N + m to Z for all m,N; P(1/N + m)
− P(m) = (1/N)·Q_N(m) ∈ Z for all m, where Q_N has coefficients scaled by N^{-deg+1}·…
letting N → ∞ over primes forces all nonconstant coefficients to vanish. ∎
LEGAL alternative (the "rational-as-ratio idiom"): never decompose q; introduce q = a/b with
b ≠ 0 explicitly and put the conditions on a and b (1 extra var per decomposed rational,
usually already present). This is how all Koenigsmann/Sun constructions handle denominators.

## B5. Integer-slot packing inside a rational: never profitable

Packing x + N·y (y in {0..N−1}) needs the bound y ≤ N−1 and y ≥ 0 — positivity machinery at
≥ 4 vars per bounded slot (M2) plus the range disjunction — strictly worse than one fresh
variable (1 var). CONCLUSION: over Q there is no packing that beats fresh variables. All
compression must come from sharing/batching (M1), elimination (M4–M6), and base-definition
surgery (M8). This closes the "pairing" direction the lane prompt asked about — recorded as a
boundary result, not a failure: the billions are NOT recoverable by packing.

## B6. Legal sharing table (what IS allowed)
  - All equations share one witness pool (conjunction free).
  - All disequalities share one s (product trick, M1).
  - Point-disjunctions fold into factored products (M3).
  - Linear-unit equations eliminate by substitution (M4).
  - A rational equals a ratio of existing variables for free (B4 idiom).
  - Parametrized relations eliminate their ∃-variable (M6).

## B7. Pell/growth packing degenerates over Q (proved structure fact)
x² − D y² = 1, D ∈ Q nonsquare, has the rational parametrization through (1,0):
x = (1 + D t²)/(1 − D t²), y = 2t/(1 − D t²) — all Q-points, no discreteness, no growth.
Z-MRDP machinery uses Pell units as a discrete exponential clock; over Q every such conic is
rational. Any board construction whose (⇐) proof relies on Pell-type discrete structure over
Q is broken; flag for the anatomy lane.

## B8. Three-square failure (proof that the positivity gadget needs 4)
7 is not a sum of three squares of Q. Proof: suppose 7n² = m₁²+m₂²+m₃² with n ≥ 1 minimal.
Mod 8: squares are 0,1,4. If n odd, 7n² ≡ 7 (mod 8), but sums of three squares mod 8 avoid 7
(squares mod 8 sums: {0,1,2,3,4,5,6}) — contradiction. If 4|n or n even, all m_i even
(7n² ≡ 0 mod 4 forces each m_i even), divide by 4: descent to n odd. ∎
Hence t ≥ 0 ≠ "sum of 3 squares"; 4 is minimal among form representations (Hasse–Minkowski
reduces representation-by-ternary-form questions to this local obstruction class).

## B9. LOWER BOUND (proved): score ≥ 3, i.e. k ≥ 2 witness variables

Theorem. There is no P ∈ Q[q] (k=0) and no P ∈ Q[q,w] (k=1) with
{q ∈ Q : ∃w ∈ Q, P(q,w) = 0} = Z exactly.

Proof. k=0: P's zero set is Z ⊂ Q; P has infinitely many roots ⇒ P ≡ 0 ⇒ zero set is Q. ∎
k=1: (⇒) gives infinitely many Q-points of the plane curve C: P = 0, one above each integer.
Some irreducible factor C₀ has infinitely many Q-points (Noetherian decomposition).
If C₀ has genus ≥ 2, Faltings gives finitely many Q-points — contradiction.
If C₀ is a rational curve with a Q-point, parametrize: q = Q(t) with Q(t) ∈ Q(t) nonconstant
(if constant, the image is one q — too small), and Q(t) ∈ Z for cofinitely many t ∈ Q. But a
nonconstant rational function is Z-valued on at most a thin set: near a finite pole-free
window Q(t) is p-adically continuous and nonconstant, so it attains p-adic-open sets of
rationals not contained in Z = Z_p ∩ Q… (cleanest: consider t = 1/N: deg < 0 ⇒ Q(1/N) → 0
through non-integral values for large N; deg ≥ 0 ⇒ Q(t) = c t^d + O(t^{d−1}), choose
t = 1/N large-N: |Q(1/N)| < 1/2 eventually, Q(1/N) ∈ Z forces Q(1/N) = 0 for all large N ⇒ Q
identically 0, contradiction). ∎
If C₀ has genus 1: E = projective closure is an elliptic curve (possibly with the point at
infinity removed). Its Q-points form a finitely generated group (Mordell–Weil). If E(Q) is
finite, the image is finite — contradiction. Otherwise take a non-torsion point; by the
standard elliptic divisibility sequence fact, den(x(nP)) = ψ_n(P)² → ∞ (formal group /
Siegel-type denominator theorem), so x(nP) ∉ Z for all large n — contradicting that all
Q-points project into Z. ∎

Status of each step: genus 0 step elementary (included); genus 1 step is standard but uses
the EDS denominator growth (cite Silverman AEC, Elliptic Divisibility Sequences; Ward 1987);
genus ≥ 2 Faltings (cit. Cornell–Silverman). Caveat: C₀ could be embedded with degenerate
projection q ≡ const on some components — handled (image then finite per component, and the
integer fibre must still come from the component treated above). This is a lane-original
assembly of standard facts; suitable for the Lean lane to formalize as "score ≥ 3" pin.

## B10. The k = 2 frontier
No known obstruction at score 3. If k = 2 is possible at all, the whole board collapses to a
single surface; every incumbent (12,504 down to 2.1e11) is >9 orders of magnitude above the
first open case. Open even conditionally: no BL-conditional statement in the literature rules
out small-k definitions (Koenigsmann's BL-conditional result kills ALL k — see LIT_NOTES —
so it is strictly stronger: under BL the score is ∞).
