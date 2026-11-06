"""Inventory the 551-transform certificate: kinds, fields, sizes. No replay yet."""

from __future__ import annotations

import gzip
import json
from collections import Counter
from pathlib import Path

Q = Path("work/current/quartics/quartic-4973")


def main() -> None:
    lines = gzip.open(Q / "certificate.jsonl.gz", "rt").read().splitlines()
    print("lines:", len(lines))
    kinds: Counter[str] = Counter()
    fieldnames: dict[str, set[str]] = {}
    sizes = []
    last = None
    for n, ln in enumerate(lines):
        d = json.loads(ln)
        if "kind" in d:
            k = d["kind"]
            kinds[k] += 1
            fieldnames.setdefault(k, set()).update(d.keys())
            sizes.append((k, len(ln)))
        else:
            last = d
            print("non-op line", n, "keys:", list(d.keys()))
    print("kinds:", dict(kinds), "total ops:", sum(kinds.values()))
    for k, fs in fieldnames.items():
        print(f"  {k}: {sorted(fs)}")
    if last:
        print("final keys:", sorted(last.keys()))
        r = last.get("report", {})
        print("final.report:", json.dumps(r)[:400])
        print("final rows_sha256:", last.get("rows_sha256"), "allocated_variables:", last.get("allocated_variables"))
    # sizes by kind
    by: dict[str, list[int]] = {}
    for k, s in sizes:
        by.setdefault(k, []).append(s)
    for k, v in by.items():
        print(f"  size {k}: n={len(v)} total={sum(v):,} max={max(v):,}")
    # 'gates' key seen earlier
    d0 = json.loads(lines[0])
    print("op0:", {k: (str(v)[:200]) for k, v in d0.items()})
    for n in range(1, 6):
        d = json.loads(lines[n])
        print(f"op{n}:", {k: (str(v)[:160]) for k, v in d.items()})


if __name__ == "__main__":
    main()
