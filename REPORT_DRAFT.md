# REPORT — T1 lane re-task: T4 probe + ideal-redundancy sweep (draft)

## T4 probe (pole-into-conic fusion): measured, REFUTED as a lever
- Final-space pole blocks located structurally (37 E7 rows `−867w²+34wj−17qk+j²`,
  1/site; 307 pole-block variables).
- Classification: 232 DEG-blocked (definitions are squares/products — substitution
  leaves the deg≤2 budget), 74 with no linear definition, 1 eliminable (x1461, a
  global carrier). T4's −250 does not exist; ceiling −1 pole var.
- Whole-system bounded sweep (T5-class, subsumes the probe): 51 exact, per-op
  verified substitution ops → −51 vars, −51 rows; monomials 72,925→73,894;
  Φ coeff height 80→129 bits (cap 2^64/row held). Checker: identity 0-diff, exit 0.

## Ideal-redundancy sweep (A3)
- Pattern hypothesis REFUTED: 117 shape-signatures / 4,552 rows, members on
  disjoint variable blocks; 0 duplicates, 0 scalar multiples. No PATTERN-ASSUMED
  drops taken.
- Span drops: PROVED-class only (mod-p detection + CRT ratio lift + exact
  Fraction re-proof per drop); counts TBD from the stack run.

## Stack
4,973 → TBD (see STACKED_COUNTS.md; ≤2,486 flag: N/A).

## Control arms
- sign-corrupted sweep caught by per-op exact recomputation (measured);
- wrong-row drop bug caught by proof-trail review before commit (measured);
- pipeline control arm: shipped system through my finalize+checker → 0-diff, exit 0;
- variant checker arms: 5/5 (artifact lane), my variant 0-diff.
