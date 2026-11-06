# REDUNDANCY.md — ideal-redundancy sweep of the 4,552-row system

## Method ladder (verification strength stated per class)

1. **PROVED (row span, exact-Q).** A row whose polynomial equals an exact
   rational linear combination of surviving rows is dropped: the row-list zero
   set is unchanged (evaluate the combination at any common zero), hence
   V(Σ survivors R²) = V(Σ all R²) and the SoS form Φ′ = Σ survivors R² keeps
   the iff. Detection: sparse Gaussian elimination mod p (61-bit primes,
   re-sorting reduction); each dependent row's multiplier vector is lifted
   across primes by CRT, ratios rationally reconstructed (Wang), and the
   candidate combination is **re-proven by exact Fraction expansion** before
   the drop is accepted. A drop without a passing exact check is never taken.
2. **PROVED (definition, exact).** The elimination sweep (see T4_PROBE.md /
   STACKED_COUNTS.md): variable v with a linear definition row (rest of degree
   ≤ 1) is substituted into its consumers with exact integer row rewrites,
   each rewrite re-verified independently by exact rational recomputation.
3. **PATTERN-ASSUMED — measured and REFUTED as a redundancy source.** The A3
   hypothesis (same-form families redundant by the contact pattern) is wrong:
   4,552 rows fall into only 117 shape-signatures (e.g. 467 rows of shape
   `x − y²`-class, 464 of `−x + yz + w`-class), but family members bind
   **disjoint variable blocks** (top family: 467 rows, only 1 shares any
   variable with a given member). Same shape on different variables is an
   independent constraint, not a consequence. Measured: 0 exact/sign
   duplicates, 0 scalar-multiple pairs. No row was dropped on pattern
   grounds; nothing in the final variant rests on PATTERN-ASSUMED.
4. **SAMPLED:** not used as a drop justification anywhere. (The checker's S4
   random-point identity is a bug-catcher for the produced term list, not a
   soundness argument.)

## Results (measured on the final system; see STACKED_COUNTS.md for the ledger)

- Single-occurrence-linear variable drops: **0** (the release's own elims
  consumed every such case).
- Two-occurrence / linear-definition substitutions under the degree-2 budget
  and 2^64 coefficient cap: **51 variables** (rows die with them 1:1).
  Breakdown: 21 constant pins (x4118..x4138 := ±3^16, rows 0–20), 29
  height/scalar/beta linear carriers, 1 global normalized carrier (x1461,
  the only pole-adjacent one).
- Span dependencies (exact-Q proved): see STACKED_COUNTS.md — filled from
  `stack_log.json` / `exactq_swept.json`.
- Pattern families: 117 signatures / 4,552 rows; largest 467; **0 dropped on
  pattern grounds** (refuted as redundancy).
