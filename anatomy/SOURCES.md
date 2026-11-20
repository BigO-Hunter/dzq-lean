# SOURCES — all read 2026-11-06

## Primary (v4 analysis)
- Repo clone: https://github.com/elliotglazer/diophantine-z-q (HEAD bdc5f4aa)
- v4 worktree at tag **quartic-4973-version-4** = commit 2ba2e731eba9a9886bd10a0c3535ad0a8d368a7c → `v4/`
  - `quartic_4973.tex` (14,982 lines): §main (59), sec:degree8-original (6607,
    F8=15,671 vars deg 8), arithmetic source revisions (9117–10031: three-mode
    9205, private conics 9314, Lucas tests 9521, general root carrier 9648,
    doubled targets 9750, shared-field-square lemma 9858, first-norm fusion
    9869ff, refinements 9825), quartic reductions 10060, finite realization +
    certificate census 10174, "five new primes" 13642.
  - `quartics/quartic-4973/`: construction-map.json (115 instantiations),
    weights.json (4,552, all 1), residuals.json.gz, certificate.jsonl.gz
    (551 transforms), polynomial.expanded.txt (72,925 monomials),
    verify_certificate.py, README.md, reproducibility/.
  - `degree8-original/` (base-compiler evidence; modules q_compare4/q_batch41/
    q_primeparity/q_anchor/q_height_batch/Z_definition).
- Release: https://github.com/elliotglazer/diophantine-z-q/releases/tag/quartic-4973-version-4
  (published 2026-11-06T15:49:49Z). v3 tag quartic-9625-version-3 (14:17:01Z),
  v2 quartic-12504-version-2 (02:59:53Z), handoffs 11-06 r2/r3.

## Historical (pre-collapse lane)
- elliot @ bdc5f4aa: `diophantine_zq.tex` (4,618 lines): template/recipe witness
  tables (~3095), slope/test_group/height_certificate semantics (640–790).
- qqwref clone (fork): PR #1 = 97cec7f..3e718ba via api.github.com pulls/1
  (body quoted in analysis); construction/ordinary-integer-definition.json
  (recipe DAG), construction/precision-natural-polynomial.json (17.9MB source
  DAG: 293,620 nodes = 125,327 add + 98,382 mul + 54,056 var + 15,845 calls),
  construction/optimized/{README.md, program-and-square.md, cutoff.md}.

## Not read (gaps)
- v2/v3 tex manuscripts (only construction-map + README of v3 used).
- research handoff zips (349MB/375MB v4; 340MB 11-04) — skipped by size.
- Lean dir (main declaration still `sorry` per README).
- Polynomial expansion binary-checked only via README stats + gz listing.
