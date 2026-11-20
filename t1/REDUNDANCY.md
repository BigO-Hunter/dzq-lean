# REDUNDANCY.md — ideal-redundancy sweep of the 4,552-row system (final)

## Answer: 0 span drops. The system has FULL ROW RANK (measured, controlled).

The A3 estimate (−10..−50% of rows) is dead at the only rigorously checkable
level (row span). Both the shipped 4,552-row system and the 4,501-row swept
variant reduce to rank == rows under two independent primes (2^61−1 and
2^62−57): every residual is linearly independent. This matches
COMPRESSION.md's anti-target: "the remaining 4,552 look mutually needed."

## Tooling + control arms (the important part)

The first three elimination implementations had a silent **reduce-branch bug**
(leading coefficient not removed/normalized): the branch re-inserted the lead
column and any row that needed reduction hung — but rows that pivoted
immediately (all of them, in the buggy runs) never triggered it, so the runs
reported "full rank, 0 deps" without ever exercising reduction. The planted-
dependence controls exposed it:

| control | planted | buggy tool | fixed tool |
|---|---|---|---|
| duplicate row | dep = 1 | hang (timeout) | **dep = 1** ✓ |
| 2× row 5 | dep = 1 | hang | **dep = 1** ✓ |
| r0+r1 combination | dep = 1 | hang | **dep = 1** ✓ |
| perturbed row (coeff +1) | dep = 0 | — | **dep = 0** ✓ |
| 10 random perturbations | dep = 0 | — | **0/10** ✓ |
| duplicate under prime 2 | dep = 1 | — | **dep = 1** ✓ |

Final reducer: lead-normalized modular elimination (factor = f·lead⁻¹ mod P),
min-column pivoting under a static min-degree column order (the naive order
exploded fill-in; the ordered one runs in <1 s). Multiplier vectors are
carried through the elimination (R_d + Σ mult·R ≡ 0, mult[d] = 1) — retained
for any future lift, though no drop was taken.

## Drop classes (task-required labeling)

- **PROVED-consequence drops: 0.** No row is in the Q-span of the others
  (full rank, two primes, controls green). Nothing to drop on this class.
- **PATTERN-ASSUMED drops: 0.** The pattern hypothesis is refuted as
  redundancy: 4,552 rows share only 117 shape-signatures (largest family 467
  rows of `x − y²`-class), but family members bind disjoint variable blocks
  (top family: 1 variable-sharing neighbor). Same shape ≠ same constraint.
  Also measured: 0 exact/sign duplicates, 0 scalar-multiple pairs. The
  contact-index arithmetic progression (scale 47027, shift 3) creates shape
  regularity, NOT algebraic redundancy — each contact's rows bind that
  contact's private variables.
- **SAMPLED drops: 0.** Randomized evaluation was used only as a bug-catcher
  (checker S4-style), never as a drop justification.

## Consequence for the lane

The row count 4,552 (→4,501 after the definition sweep) is span-tight. Any
further row reduction needs ideal-level (higher-degree) consequence arguments,
which are infeasible to verify at this size and were not attempted — no
PATTERN-ASSUMED or SAMPLED drops were smuggled in.
