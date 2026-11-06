# STACKED_COUNTS.md — T4 probe + ideal-redundancy sweep: final stacked ledger

## Verdict: stacked candidate = 4,973 → 4,922 variables (−51). The −2,486 flag: N/A.

Stack = definition-elimination sweep (51 exact, per-op-verified substitutions)
+ span-redundancy drops (0 — the system has full row rank; see REDUNDANCY.md).

| quantity | shipped v4 | stacked variant | delta |
|---|---|---|---|
| total variables | 4,973 | **4,922** | **−51** |
| residual rows | 4,552 | **4,501** | **−51** |
| Φ monomials | 72,925 | **73,894** | +969 |
| degree | 4 | 4 | — |
| max \|Φ coeff\| bits | 80 | 129 | +49 |
| max \|row coeff\| bits | 40 | 64 (cap 2^64 held) | +24 |
| weights | all 1 | all 1 | — |
| artifact checker (S3 exact identity + S1 metrics) | 0-diff | **0-diff, exit 0** | — |

Artifacts: `stacked/phi_stacked.canonical.txt.gz`
(sha256 `d4364aab4d474c858119bcdf098dd2b005198c6de02407770bc9d509f2c3d705`),
`stacked/package/{residuals.json.gz,weights.json,variable-map.json}`,
checker output `stacked/stacked_check.out`. Row-level transform log:
`stack_log.json` / `phaseD_ops.json` (51 ops; every consumer rewrite
independently re-verified by exact rational recomputation).

≤2,486 flag: **not reached, not approached** (−51 of the needed −2,487).

## Move ledger (all measured; proof classes in REDUNDANCY.md)

- Definition-elimination sweep: 51 variables/rows removed.
  - 21 constant pins: x4118..x4138 := ±3^16 (rows 0–20, anchor/beta chain).
  - 29 linear-definition carriers (height-batch/scalar/beta blocks).
  - 1 pole-adjacent global carrier (x1461) — the entire T4 harvest.
- Span drops: **0** (full row rank under two primes; controls 5/5 green).
- Pattern-family drops: **0** (hypothesis refuted; 117 shapes / 4,552 rows,
  disjoint variable blocks).
- T4 proper ("pole-into-conic fusion, est −250"): **−1 variable**; refuted —
  the 307 final-space pole-block carriers are 232× DEG-blocked (square-chain
  definitions leave the deg≤2 budget) + 74× without a linear definition
  + 1 eliminable. See T4_PROBE.md.

## Control arms (all measured)

1. Sign-corrupted sweep: per-op exact recomputation rejects 51/51 rewrites ✓
2. Wrong-row drop bookkeeping: caught by proof-trail review before any run ✓
3. Pipeline control: shipped system through my finalize → checker → 0-diff,
   exit 0, 72,925 monomials reproduced ✓
4. Elimination controls: planted duplicate/2×/combination rows detected
   (dep=1 each), perturbed rows rejected (0/10 false deps), under both primes ✓
   — these caught a silent reduce-branch bug in the first three reducers
   (see REDUNDANCY.md; the fix flipped the controls green).
5. Variant checker arms: control 5/5 (artifact lane), my variant 0-diff ✓
