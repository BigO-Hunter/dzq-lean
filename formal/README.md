# dzq-lean-formal

Lean kernel verification of the DZQ artifacts (lane 2026-11-06): `FORMAL_REPORT.md` lists what is kernel-checked; `CERT.lean`/`Z2FORM.lean` carry the verified core; `LEAVES.lean` + `gen_leaves.py` are the generated-leaf layer; `axcheck.py` audits axioms. Toolchain v4.34.1 + Mathlib pinned at a git revision (see lake-manifest.json).

Status: kernel-checked list complete per the report; leaf propagation open.

## Why this repo is up

Public evidence: the Lean kernel-verified core of the DZQ artifacts, with the kernel-checked list and reproducible generators.

[BigO-Hunter](https://github.com/BigO-Hunter) is the tracking & packaging org for [Big O Speedrun](https://bigospeedrun.com) contributions · [org profile](https://github.com/BigO-Hunter/.github) · [bigo-hunter.github.io](https://bigo-hunter.github.io).

## What work can be done here

Open work: extend LEAVES propagation; complete the certificate chain per FORMAL_REPORT.md.

## License

Licensed under the Copy-Free/Stays-Free (CFSF) License — see [LICENSE](LICENSE). CFSF: copy-free (use for any purpose) and stays-free (nobody may fence this work). The name is unclaimed in software licensing (checked 2026-11-09) and is deliberately not "Copyfree" — the Copyfree Initiative's certification mark — since CFSF's anti-enclosure condition is excluded by their standard. 
