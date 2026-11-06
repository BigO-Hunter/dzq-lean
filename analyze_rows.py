"""Characterize the 4552 residual polynomials: degree, terms, lead-variable structure."""

from __future__ import annotations

import gzip
import json
from collections import Counter
from pathlib import Path

Q = Path("work/current/quartics/quartic-4973")


def deg(p) -> int:
    return max((len(idx) for _c, idx in p), default=0)


def main() -> None:
    rows = json.loads(gzip.open(Q / "residuals.json.gz", "rt").read())
    w = json.loads((Q / "weights.json").read_text())
    print("rows:", len(rows), "weights:", len(w), "distinct weights:", Counter(w))
    dh = Counter(deg(r) for r in rows)
    tc = Counter(len(r) for r in rows)
    print("degree hist:", dict(sorted(dh.items())))
    print("terms-per-row top:", tc.most_common(12))
    print("max terms in a row:", max(len(r) for r in rows))
    maxc = max(abs(c) for r in rows for c, _ in r)
    print("max |coeff| in residuals:", maxc, "bits:", maxc.bit_length())

    # lead-variable structure: does each row contain exactly one pure linear monomial [c,[v]]?
    lc = Counter()
    examples = {}
    for i, r in enumerate(rows):
        lin = [(c, idx[0]) for c, idx in r if len(idx) == 1]
        lc[len(lin)] += 1
        if len(lin) != 1 and len(examples) < 8:
            examples[i] = r[:6]
    print("rows by #pure-linear-monomials:", dict(sorted(lc.items())))
    for i, e in examples.items():
        print("  odd row", i, "deg", deg(rows[i]), "terms", len(rows[i]), e)

    # is the linear var unique across rows (a permutation / triangular order)?
    leads = []
    for i, r in enumerate(rows):
        lin = [idx[0] for _c, idx in r if len(idx) == 1]
        leads.extend(lin)
    c = Counter(leads)
    print("pure-linear vars:", len(leads), "dupes:", [v for v, n in c.items() if n > 1][:10])
    print("lead var range:", min(leads), max(leads))
    print("input var (0) appears as a pure-linear lead?:", 0 in c)
    # which vars appear ONLY in the pure-linear position (i.e. never inside nonlinear monomials of same row)?
    print("first 5 rows:", [[list(t) for t in r] for r in rows[:3]])


if __name__ == "__main__":
    main()
