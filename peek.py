"""Inspect gz/json artifacts structurally without dumping payloads."""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path


def peek_obj(o, depth=0, maxdepth=3):
    pad = "  " * depth
    if isinstance(o, dict):
        keys = list(o.keys())
        print(f"{pad}dict[{len(keys)}] keys={keys[:12]}{'...' if len(keys) > 12 else ''}")
        if depth < maxdepth:
            for k in keys[:8]:
                print(f"{pad}  .{k}:", end=" ")
                peek_obj(o[k], depth + 2, maxdepth)
    elif isinstance(o, list):
        print(f"{pad}list[{len(o)}]")
        if o and depth < maxdepth:
            peek_obj(o[0], depth + 1, maxdepth)
    else:
        s = repr(o)
        print(f"{pad}{type(o).__name__} {s[:160]}")


def main() -> int:
    for p in sys.argv[1:]:
        path = Path(p)
        print(f"\n===== {path.name}  ({path.stat().st_size:,} bytes) =====")
        if path.suffixes[-2:] == [".txt", ".gz"] or path.name.endswith(".gz"):
            with gzip.open(path, "rt", encoding="utf-8") as fh:
                first = fh.readline()
                print("first line:", first[:300])
                n = 1
                for _ in fh:
                    n += 1
                    if n > 3_000_000:
                        break
                print("lines:", n)
                fh.seek(0)
                try:
                    obj = json.load(fh)
                except Exception as e:  # noqa: BLE001
                    print("not-single-json:", type(e).__name__, str(e)[:120])
                    return 0
                peek_obj(obj)
        else:
            obj = json.loads(path.read_text())
            peek_obj(obj)
    return 0


if __name__ == "__main__":
    sys.exit(main())
