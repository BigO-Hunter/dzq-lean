#!/usr/bin/env python3
"""Extract #print axioms results from the lake build output and gate the footprint."""
import re
import sys

ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
log_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/dzq_lean_cert.log"
txt = open(log_path).read()

# #print axioms prints:  '<name>' depends on axioms: [a, b, c]
pat = re.compile(r"'([^']+)' depends on axioms: \[([^\]]*)\]")
rows = pat.findall(txt)
bad = []
for name, ax in rows:
    deps = {a.strip() for a in ax.split(",") if a.strip()}
    extra = deps - ALLOWED
    status = "OK" if not extra else "VIOLATION: " + ",".join(sorted(extra))
    print(f"{name}: {sorted(deps)} {status}")
    if extra:
        bad.append(name)
print(f"\n{len(rows)} axchecked; violations: {len(bad)}")
sys.exit(1 if bad or not rows else 0)
