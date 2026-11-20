# COUNTS.md — exact ledger (T1 outcome: 4,973 → 4,973)

Baseline verified against `reproducibility/manifest.json`: variables **4,973**,
rows 4,552, degree 4, monomials 72,925, max|coeff| 685,783,949,153,203,534,233,890.

## Conic + pole block census (measured from construction-map.json)

| block | instances | locals each | total |
|---|---|---|---|
| q_conic13 | 13 | 52 | 676 |
| q_conic10 | 16 | 39 | 624 |
| q_conic6 | 8 | 25 | 200 |
| **conic total** | **37** | — | **1,500** |
| q_linearnormalpole | 37 | 10 | 370 |

## T1 savings

| item | estimate | measured |
|---|---|---|
| conic blocks eliminated by per-root sharing | −24 × ~40 = −960 | **0** (coincidence classes: 37 singletons; see R_COINCIDENCE.md) |

**New variable count: 4,973 (no change).** Term count and degree: unchanged
(4,552 rows, deg ≤ 2 residuals, 72,925 monomials — no transform was applied).

## Lane arithmetic impact

COMPRESSION.md ranked sum assumed T1 −960. Actual: −0. Remaining safe levers:
T4 (pole/interface fusion −250, certificate-class) and T5 (elimination sweep
−150) ≈ −400 certified-class; the −2,486 target now requires T2 (−780,
conditional-surface-adjacent) or arithmetic-lane work.
