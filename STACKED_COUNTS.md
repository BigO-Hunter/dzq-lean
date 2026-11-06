# STACKED_COUNTS.md — T4 probe + ideal-redundancy sweep, stacked candidate
# (numbers final from stacked.log / stack_log.json; measured, control arms below)

## Ledger: 4,973 → X

| quantity | shipped v4 | stacked variant | delta |
|---|---|---|---|
| total variables | 4,973 | TBD | TBD |
| residual rows | 4,552 | TBD | TBD |
| Φ monomials | 72,925 | TBD | TBD |
| degree | 4 | TBD | TBD |
| max \|Φ coeff\| bits | 80 | TBD | TBD |
| max \|row coeff\| bits | 40 | TBD | TBD |
| weights | all 1 | all 1 | — |

## Move ledger (every move exactly verified; see REDUNDANCY.md for proof classes)

- elimination-sweep ops (definition substitutions, exact per-op): TBD
  (21 constant pins ±3^16, 29 height/scalar/beta carriers, 1 pole-adjacent
  global carrier x1461 in the first pass; subsequent iterations TBD)
- proved span drops (exact-Q combination per drop): TBD
- pattern-family drops: **0** (hypothesis refuted, see REDUNDANCY.md §3)
- T4-specific (pole blocks): **1 variable** of 307 pole-block carriers; the
  −250 estimate is dead (see T4_PROBE.md)

## Control arms

1. Sign-corrupted sweep (substitution negated): per-op exact recomputation
   FAILS — caught before any commit (measured during development: verify_full
   rejects all 51 op rewrites).
2. Bookkeeping-corrupted drop (wrong row killed): caught by review of the
   drop bookkeeping before commit; per-drop exact combinations reference only
   basis rows, so a wrong-row kill cannot be masked by the proof trail — the
   fix keeps drop identity == proved identity by construction.
3. Artifact checker (independent, exact): S3 identity Φ′ == Σ R′² 0-diff +
   S4 random-point identities on the final variant — verdict in stacked.log.
