# T4_PROBE.md — pole-into-conic fusion probe (measured, final space)

## Answer: T4's estimated −250 does not exist. Measured ceiling: −1 variable.

The probe was run in FINAL space (the shipped 4,552-row residual system). Two
preliminary facts fix the methodology:

1. The construction-map's `first_residual` indexes the SOURCE row order
   (4,513 source rows; initial certificate state has 4,879), and its
   `first_local` indexes SOURCE variable ids (4,935 = source_variables), NOT
   the final 4,973-id space. Any block analysis must go through
   `variable-map.json` (final id → candidate id) or re-derive blocks
   structurally in final space. (This lane's earlier source-space reads are
   design-space statements; all counts below are final-space.)
2. The pole blocks were located structurally in final space: the pole
   second-conic rows `−867w² + 34wj − 17qk + j²` survive verbatim — exactly
   **37** of them (coefficient multiset {−867,−17,1,34}), one per site. Their
   1-step row neighborhoods define the final-space pole blocks: **307
   variables** (10 locals × 37 sites, minus overlaps with the shared
   carriers).

## Eliminability classification of the 307 pole-block variables

| class | count | mechanism |
|---|---|---|
| DEG-blocked | 232 | every candidate definition row has a degree-2 rest (e.g. `j − s_p²`, `k − r̂·q`, `z − l²`): substitution into the consumer (`w·j`, `q·k`, `z·c`) forces degree 3+ — outside the Σ(deg≤2)² contract |
| no-linear-def | 74 | the variable appears only inside degree-2 monomials in all its rows; no row is linear in it, so nothing to pivot on |
| ELIMINABLE | **1** | x1461 — the normalized r̂ carrier (shared across all 37 blocks); eliminated by the bounded sweep (alias row `−x9 + 828120733440·x1461`) |
| CONS-blocked | 0 | — |
| COEFF-blocked | 0 | — |

## Why T4 looked like −250 and isn't

The pole module's 8 rows per site are already the certificate-normalized
remnant: the release's own 121 definition eliminations + 148 relation
eliminations consumed everything linear-definable. What remains per site is
exactly the irreducible square-chain core of the norm tree + pole test
(`l²=z`, `s_p²=j`, `r̂q=k`, `p²=17r−51ec+34c`, `w=17e−zc`, the linear-unit row
and the two conic rows). Squares and products of field elements cannot be
substituted away without leaving the deg-2 budget — the fusion target rows
ARE those squares' consumers. There is no row-reorganization that drops
variables: every block local is load-bearing.

## Measured deltas (bounded elimination sweep, whole system)

See STACKED_COUNTS.md for the ledger. T4-specific: **−1 variable** (x1461) of
the 370 pole locals' final-space carriers; the other 306 are degree- or
structure-tight. T4 as scoped ("fuse 8 pole residuals into conic equations,
−interface duplication ≈ −250") is refuted at row level: the 296 pole rows in
final space are 37 E7 rows + already-fused definitions; nothing foldable
remains.
