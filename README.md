# dzq-lean

Lean certifiability analysis of **"ℤ is Diophantine in ℚ"** (DZQ): which Mathlib lemmas
actually resolve (each `#check`-verified in Lean v4.34.1 / Mathlib `d13f23b7`), a
**kernel-verified sum-of-squares collapse**, the honest gap list, and the recovered research
lanes.

## Race status (Big O Speedrun board, fetched 2026-11-26)

The **Z Diophantine in Q** race is **OPEN**. Current leader: **Jose Brox — 257 variables,
Nov 16 2026, Claimed** (not yet Lean Verified). A race closes only when the best bound is
provably optimal *and* Lean Verified.

The variable-count construction recovered here (incumbent 4,973 → stacked 4,922, `t1/`) is
**superseded on variable count** by Brox's 257. This repo's standing contribution is
independent of that count: the **certifiability framework** and the **proved, kernel-checked
mechanical half** (the sum-of-squares collapse), which apply to *any* construction — including
a future verified one. `CERTIFIABILITY.md` explains why the arithmetic leaf, not the variable
count, is the binding constraint.

## What is here

- `CERTIFIABILITY.md` — headline verdict: the mechanical half is certifiable now; the
  arithmetic half is research-level for every mechanism.
- `GAP_LIST.md` — exactly what Mathlib has vs what a sorry-free certificate needs; each
  EXISTS/ABSENT checked by `#check`.
- `Dzq/`, `Dzq.lean`, `AxCheck.lean`, `Probe*.lean`, `Statement_*.lean` — the root Lake
  package: the certifiability harness (compiled, zero `sorry`) and axiom probes.
- `formal/` — the kernel-verification package (`CERT` = `Z2FORM` + `LEAVES` assembly),
  `FORMAL_REPORT.md` (what is kernel-checked), reproducible generators, `axcheck.py`.
- `anatomy/` — source anatomy, compression analysis, ledger tooling.
- `artifact/` — independent coefficient-exact checker for quartic-4973, control arms,
  canonical artifact generation, acquisition receipts (`dl/`).
- `audit/` — confirmed RC gap analysis and height-seam disclosure.
- `constructions/` — candidate constructions, counting calculus, re-scoring vs the 4973 bar.
- `exec/` — the eight-parameter Lambda and its independent exact 2-adic machine verification.
- `k2/` — audit-repair map and citation revisions.
- `optimize/` — residual-compression and redundancy analysis.
- `t1/` — the stacked-ledger 4,973 → 4,922 variant (verified definition-elimination), plus the
  refutation record showing identification-based further reduction is unsound.

The public face of the campaign is
[BigO-Hunter/z-diophantine-research](https://github.com/BigO-Hunter/z-diophantine-research).

## Reproduce / verify

Both Lake packages pin Mathlib to git rev `d13f23b723b8a846827a245b89c10fc7d3f11612`
(`lake-manifest.json`); no sibling checkout is required. Toolchain: `leanprover/lean4:v4.34.1`.

```sh
# Root certifiability harness (builds Dzq, then axiom-probes the analysis theorems)
lake build
lake env lean AxCheck.lean

# formal/ kernel verification (CERT = Z2FORM + LEAVES)
cd formal && lake build
```

CI (`.github/workflows/lean.yml`) runs both builds via `leanprover/lean-action` with the
Mathlib cache. Python checkers/generators run from their named lane; `formal/gen_leaves.py`
accepts `DZQ_EXEC=/path/to/exec` for optional leaf regeneration (the committed `LEAVES.lean`
is authoritative, so regeneration is not needed to consume the proofs).

## Next steps for a continuer

1. **Reflection layer** for sparse polynomial data (`GAP_LIST.md` §1): turn `SosCert.ident`
   from intractable elaboration into a `decide`-able comparison. Bounded, no new math.
2. **The arithmetic leaf** (`GAP_LIST.md` §2): the `HardDirection` obligation — Selmer /
   L-function / height machinery, or a valuation-only converse. Research-level.
3. Close the remaining `GAP_LIST.md` items; extend `formal/` LEAVES propagation.

## License

Copy-Free/Stays-Free (CFSF) — see [LICENSE](LICENSE). Copy-free (use for any purpose) and
stays-free (nobody may fence this work).

## Disclosure

AI-assisted; disclosed. Produced with AI assistance and machine verification (Lean kernel
checks, exact 2-adic arithmetic, coefficient-exact checkers). Receipts and refutation records
are kept as-is.

[BigO-Hunter](https://github.com/BigO-Hunter) is the tracking & packaging org for
[Big O Speedrun](https://bigospeedrun.com) contributions ·
[org profile](https://github.com/BigO-Hunter/.github) ·
[bigo-hunter.github.io](https://bigo-hunter.github.io).
