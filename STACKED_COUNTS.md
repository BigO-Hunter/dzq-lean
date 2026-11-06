# STACKED_COUNTS.md — T4 probe + ideal-redundancy sweep, stacked candidate
# (T4-probe numbers final; stack span-drop numbers filled from stacked.log)

## Ledger: T4-probe variant (checker-verified, `variantB_check.out`)

| quantity | shipped v4 | swept variant (T4 probe) | delta |
|---|---|---|---|
| total variables | 4,973 | 4,922 | **−51** |
| residual rows | 4,552 | 4,501 | **−51** |
| Φ monomials | 72,925 | 73,894 | +969 |
| degree | 4 | 4 | — |
| max \|Φ coeff\| bits | 80 | 129 | +49 |
| max \|row coeff\| bits | 40 | 64 | +24 |
| weights | all 1 | all 1 | — |
| checker (S3 identity, exact) | 0-diff | **0-diff, exit 0** | — |

## Ledger: stacked variant (sweep + proved span drops)

| quantity | shipped v4 | stacked | delta |
|---|---|---|---|
| total variables | 4,973 | TBD | TBD |
| residual rows | 4,552 | TBD | TBD |
| Φ monomials | 72,925 | TBD | TBD |
| degree | 4 | TBD | TBD |
| checker | 0-diff | TBD | — |

(≤2,486 flag: N/A — the stack does not approach the halving target; see report.)

## Move ledger (every move exactly verified; see REDUNDANCY.md for proof classes)

- elimination-sweep ops (definition substitutions, exact per-op): **51**
  (21 constant pins ±3^16, 29 height/scalar/beta carriers, 1 pole-adjacent
  global carrier x1461); 0 further ops after drops (measured in iterations).
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
