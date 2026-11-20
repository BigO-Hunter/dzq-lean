# T1_CONSTRUCTION.md — no reduced construction exists (refutation record)

Task step 2 (construct the joint norm tree) is **not reached**: the
precondition (task step 1) failed. Recorded here so no successor re-derives
the attempt.

## What T1 would have needed

1. A partition of the 37 conic instances into classes sharing one conic
   θ² − r·S = 2 and one packed norm tree N_r(u,v) = u² + r·v².
2. Each class's members to satisfy r identical **as values at every solution**
   — either by sharing the variable (measured: no pair shares; 37 distinct
   carriers 119, 137–172) or by a forcing residual (measured: none; the only
   multi-r residuals are quadratic comparisons against fresh aux vars).
3. A leaf-merge lemma extending the within-site norm tree across sites. This
   fails structurally, not just accidentally: leaves of site j live in the
   quadratic extension Q(√2)(θ_j) with θ_j² = r_j·s_j² + 2 — distinct r_j
   gives distinct extensions with no common overfield element to multiply, so
   the product-W pole argument (which is intra-extension) does not compose.

## What was measured instead (all counts exact, from the pinned package)

- 37 conic instantiations: q_conic13 ×13 (52 locals), q_conic10 ×16 (39),
  q_conic6 ×8 (25) = 1,500 conic locals + 37 × 10 pole locals.
- r-carriers: 37 distinct variables; Z_definition log names them "ordinary
  contact" (×34), "affine numerator", arithmetic carrier.
- Site subtree variable spans: pairwise disjoint (0 overlaps).
- Cross-r residuals: 42, all quadratic-with-aux; 0 linear-difference forms.
- Contact geometry: 37 distinct points 2Q_j = n_j·Pstar (scale 47027, shift 3).

Conclusion: the reduced system R′ does not exist; Σ R_i² stays 4,552 rows /
4,973 vars / deg 4 / 72,925 monomials. See R_COINCIDENCE.md, COUNTS.md,
T1_CERTIFICATE.md.
