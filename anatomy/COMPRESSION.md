# COMPRESSION TARGETS — v4 4,973 → 2,486 (need −2,487)

Target is an arbitrary halving (v4 README: "search target, not a result").
Need ~50% off a system where per-site costs are: full 159, lucas 131, beta 62,
fixed 249, ×37 sites + frame. Ranked:

## T1. Share private conics across sites (SAFE, ALGEBRAIC, biggest certified-class win)
Each of 37 sites pays its own conic block (conic13 52 / conic10 39 / conic6 25)
+ linearnormalpole 10. The conic θ²−rS_c=2 and its norm tree N_r(u,v)=u²+rv²
certify field divisibilities for ONE site's r-value. BUT conic instantiations
take the site's root coordinate as first arg — sites within one root point's
block may share the same r (runtime variable). **Move:** one conic per root
POINT (not per site), with all sites of that point feeding one packed norm
tree (the tree already merges within a site; extend across sites — the pole
conclusion is about the product W, so a shared conic + bigger tree is sound
with the same lemma). Est: if 37 sites collapse to ~13 distinct roots →
−24 conic blocks × ~40 = **−960**. Proof needed: joint packing lemma (tree
ascent/descent with multiple W_i already proved per site; extending the leaf
set is mechanical). Measure first from construction-map args + variable-map
whether r-coincidence holds structurally.

## T2. Deeper demotion: contacts per point 8 → 6 (ARITHMETIC, needs re-proof)
The 3-mode coverage uses fixed 8-contact finite blocks per point (0–4 shared,
5–12 = A,T blocks, 13–20/21–28, 29–36). Block size 8 comes from the 41-prime
pattern lineage. The manuscript already proves "an absolute bound of FIVE new
primes" (§13642) for the odd transfer — the block size may be reducible. If
blocks drop to 6: −2 contacts × ~3 point-blocks × ~130 avg = **−780**. Needs:
re-proof of the height/pole coverage with the shorter blocks (the six-contact
→ five-contact history shows this is how they shrink). Risk: breaks the iff
if the comparison no longer pins non-integer inputs — must re-check the
"missing-address contradiction" count.

## T3. Fifth mode: demote remaining 13 full sites partially (ARITHMETIC)
Full sites (159) vs lucas (131): the compare4 part (97) vs compare_lucas (82).
The full mode exists for the shared positions and the final contradiction.
If the shared block (0–4) can run beta+Lucas jointly instead of full:
5 sites × (159−131) = **−140**. Cheap variant of T2.

## T4. Pole/interface fusion (SAFE, mechanical)
q_linearnormalpole is a separate module at every site (10/site = 370) purely
for interface cleanliness. Fuse its 8 residuals into the conic modules'
equations (they share the site's locals). −interface duplication ≈ **−250**.
Certificate-level, same projection; needs only row reorganization the
certificate machinery already supports.

## T5. Slack tightening via elimination sweep (SAFE, mechanical)
421 variables carry no final residual (Z_def frame 212, height_batch 26,
anchor 4, wiring). The 551-certificate already does 148 eliminations-modulo-
retained-equations + 121 definition eliminations. An automated deeper sweep
(alternating elim + shear search, deg ≤2 preserved, occurrence checks) on the
frame/wiring vars: est **−150**. Diminishing: certificate moves can't touch
the 4,552 residuals themselves — the binding constraint is source architecture.

## T6. Lucas block packing (RISKY, check soundness)
compare_lucas (82/site × 16 = 1,312) holds 3 quadratic eqs ℱ + normalized
evaluation (B_iΛ=G_i, PB_s=p_s, (U+V)p_t=PB_t, K_Lp_t=(1−2P)B_t, Vp_z=(1−2P)B_z,
E_L=U²−K_LV−P²). The s,t,z triple shares P,Λ structure across the three
numerators — partial sharing may already be exploited; remaining slack looks
small (~10/site). **−160** at best. Verify against variable-map first.

## Sum: T1 −960 + T2 −780 + T3 −140 + T4 −250 + T5 −150 + T6 −160 ≈ −2,440
Just short of −2,487 → T2 (or a stronger T1 measurement) must over-deliver,
or combine T2+T3. **Most promising for the optimization lane: T1** — it is
certificate-class (projection-preserving, machine-checkable), its proof is a
mechanical extension of lemmas already in the manuscript, and it composes with
everything else. T2 is the arbiter of whether 2,486 is reachable at all.

## Anti-targets (negative results)
- **Weights are already all 1** — no weight-based savings.
- **SoS shape is forced**: Φ=0 ⟺ all R_i=0 over Q requires the sum of squares
  (or equivalent); no residual can be dropped unless it is a consequence of
  the others (ideal-level reduction) — the certificate's 148 eliminations are
  exactly this; the remaining 4,552 look mutually needed.
- **Variable sharing across residuals is already free** (one system, not
  independent equations) — "can quadratics share variables?" is answered: they
  do; 4,552 residuals in 4,973 vars. Sharing is not the lever; residual COUNT
  and source architecture are.
- **Degree stays 4**: going deg 6→squares-of-cubics would RAISE variables
  (lift), not lower (v2 already paid the lift cost; the quartic form is the
  compressed end of that trade).
