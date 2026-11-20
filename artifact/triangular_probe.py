"""Test whether the 4552-row residual system is a forward-substitution (triangular) definition
chain from the input variable. Measures the sweep; does not assume an answer."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

Q = Path("work/current/quartics/quartic-4973")


def main() -> None:
    rows = json.loads(gzip.open(Q / "residuals.json.gz", "rt").read())
    nin = 4973
    incident: dict[int, set[int]] = {}
    for i, r in enumerate(rows):
        for _c, idx in r:
            for v in idx:
                incident.setdefault(v, set()).add(i)
    print("vars in residuals:", len(incident), "rows:", len(rows))

    used: set[int] = set()
    known = {0}
    steps = []
    stalled = False
    while True:
        progressed = False
        for i, r in enumerate(rows):
            if i in used:
                continue
            unk = {v for _c, idx in r for v in idx if v not in known}
            if len(unk) != 1:
                continue
            v = next(iter(unk))
            # v must occur only in monomials where every other factor is known, to power 1
            lincoef = 0
            ok = True
            for c, idx in r:
                if v not in idx:
                    continue
                if idx.count(v) != 1:
                    ok = False
                    break
                others = [u for u in idx if u != v]
                if any(u not in known for u in others) or len(set(others)) != len(others):
                    ok = False
                    break
                lincoef += c
            if not ok or lincoef == 0:
                continue
            known.add(v)
            used.add(i)
            steps.append((i, v, lincoef))
            progressed = True
        if not progressed:
            stalled = True
            break

    unknown = sorted(set(range(nin)) - known)
    print("sweep steps:", len(steps), "known vars:", len(known), "unused rows:", len(rows) - len(used))
    print("stalled:", stalled, "unknown vars:", len(unknown), "first unknown:", unknown[:20])
    # which rows are left, and their 'unknown count'
    left = [(i, len({v for _c, idx in rows[i] for v in idx if v not in known}), len(rows[i])) for i in range(len(rows)) if i not in used]
    print("left rows (idx, unknown-vars, terms):", left[:20], "... total", len(left))
    print("min unknown count among left:", min((x[1] for x in left), default=None))


if __name__ == "__main__":
    main()
