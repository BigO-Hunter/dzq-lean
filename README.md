# dzq-lean

Certifiability analysis of the DZQ construction: which Mathlib claims actually resolve (each verified by `#check` in compiled Lean v4.34.1 / Mathlib `d13f23b7`), the headline certifiability verdict, and the gap list.

Status: analysis complete; the formalizable fragments are kernel-verified in `formal/`. See `CERTIFIABILITY.md` and `GAP_LIST.md`.

## Why this repo is up

Private campaign umbrella: the full-history memory of the DZQ ("ℤ is Diophantine in ℚ") campaign — certifiability analysis (which Mathlib claims actually resolve, checked by `#check`), the gap list, kernel verification in `formal/`, and the recovered research lanes including unpublished improvements (`t1/` 4973→4922, `exec/` Lambda). The **public face** of the campaign is [BigO-Hunter/z-diophantine-research](https://github.com/BigO-Hunter/z-diophantine-research); the visibility boundary is deliberate — this umbrella holds lanes the public shelf does not carry.

[BigO-Hunter](https://github.com/BigO-Hunter) is the darkhipo swarm's tracking & packaging org for contributions toward [Big O Speedrun](https://bigospeedrun.com) — a companion, never the project. Org story: [profile](https://github.com/BigO-Hunter/.github) · [bigo-hunter.github.io](https://bigo-hunter.github.io).

## What work can be done here

Open work: formalize the certifiable fragments (done in `formal/`); close remaining GAP_LIST.md items.

## License

Licensed under the Copy-Free/Stays-Free (CFSF) License — see [LICENSE](LICENSE). CFSF: copy-free (use for any purpose) and stays-free (nobody may fence this work). The name is unclaimed in software licensing (checked 2026-11-09) and is deliberately not "Copyfree" — the Copyfree Initiative's certification mark — since CFSF's anti-enclosure condition is excluded by their standard.

## Umbrella layout

- Repository root: the certifiability analysis, `CERTIFIABILITY.md` and `GAP_LIST.md`.
- `formal/`: the complete original `dzq-lean-formal` kernel-verification package at source commit `0df81df3aa3c1b74d6964ee967f8ea2f99420d4c`, merged with full history.

Both Lake packages use the git-pinned Mathlib revision `d13f23b723b8a846827a245b89c10fc7d3f11612`; no sibling checkout is required. Run builds from the repository root for analysis and from `formal/` for kernel verification. Optional regeneration scripts in `formal/` accept `DZQ_EXEC=/path/to/dzq-exec`; generated artifacts are already committed, so that external directory is not needed to consume the proofs.

## Recovered DZQ research lanes

- `anatomy/`: source anatomy, compression analysis and ledger tooling.
- `artifact/`: the independent coefficient-exact checker for quartic-4973, including control arms and canonical artifact generation.
- `audit/`: the confirmed RC gap analysis and height-seam disclosure.
- `constructions/`: candidate constructions, counting calculus and re-scoring against the 4973 bar.
- `exec/`: the final eight-parameter Lambda and its verification.
- `k2/`: the audit-repair map and citation revisions.
- `optimize/`: residual-compression and redundancy analysis.
- `t1/`: the stacked-ledger improvement from 4973 to 4922, with span-rank and control checks.

These are full-history merges of local research repositories, grouped here rather than left as partial standalone notes. Each subdirectory keeps its own artifact boundary. Run any checker or generator from its named lane; T1 resolves anatomy data and its own outputs relative to this umbrella.
