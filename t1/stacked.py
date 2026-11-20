#!/usr/bin/env python3
"""STACKED candidate: iterate {bounded elimination sweep} and {proved span drops}
to a fixed point, then finalize (compact + expand + canonical term list + variant
package) and run the artifact checker on it.
All moves carry exact per-op proofs:
  - sweep: v := -rest/cv substitutions (verified per consumer with Fractions)
  - drops: row in Q-span of survivors (verified by exact Fraction combination)
"""
import os
import json, gzip, sys, collections, subprocess, hashlib, time
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(200000)
BASE = os.path.join(os.path.dirname(__file__), "..", "anatomy", "v4", "quartics", "quartic-4973")
OUT = os.path.dirname(__file__)
CAP = 1 << 64
PRIMES = [(1 << 61) - 1, (1 << 62) - 57, (1 << 63) - 25]

with gzip.open(f"{BASE}/residuals.json.gz") as f:
    rows_raw = json.load(f)
rows = [ {tuple(sorted(m)): c for c, m in row} for row in rows_raw ]
alive = [True] * len(rows)
log = {"sweep_ops": [], "dropped_rows": [], "iterations": []}

# ---------------- sweep ----------------
def subst(row, v, cv, rest):
    L = {m: -c for m, c in rest.items()}
    new = {}
    for m, a in row.items():
        if v in m:
            m2 = tuple(x for x in m if x != v)
            for n, lc in L.items():
                mm = tuple(sorted(m2 + n))
                nc = new.get(mm, 0) + a * lc
                if nc: new[mm] = nc
                elif mm in new: del new[mm]
        else:
            nc = new.get(m, 0) + a * cv
            if nc: new[m] = nc
            elif m in new: del new[m]
    return new

def verify_full(v, cv, rest, old, new):
    sigma = {m: Fraction(-c, cv) for m, c in rest.items()}
    exp = collections.defaultdict(Fraction)
    for m, a in old.items():
        if v in m:
            m2 = tuple(x for x in m if x != v)
            for n, lc in sigma.items():
                exp[tuple(sorted(m2 + n))] += a * cv * lc
        else:
            exp[m] += a * cv
    got = {m: c for m, c in exp.items() if c}
    if any(c.denominator != 1 for c in got.values()):
        return False
    return {m: int(c) for m, c in got.items()} == new

def sweep_pass():
    version = 0
    rejected = {}
    ops = 0
    while True:
        occ = collections.defaultdict(list)
        for i, r in enumerate(rows):
            if not alive[i] or not r: continue
            for m in r:
                for v in m:
                    occ[v].append(i)
        fired = False
        for v in sorted(occ):
            if v == 0: continue
            for r0 in occ[v]:
                if rejected.get((v, r0), -1) >= version:
                    continue
                row0 = rows[r0]
                cv = row0.get((v,), 0)
                if cv == 0:
                    rejected[(v, r0)] = version; continue
                rest = {m: c for m, c in row0.items() if m != (v,)}
                if any(len(m) > 1 for m in rest):
                    rejected[(v, r0)] = version; continue
                consumers = [i for i in occ[v] if i != r0]
                news = {}
                mx = 0
                ok = True
                for r1 in consumers:
                    nr = subst(rows[r1], v, cv, rest)
                    if max((len(m) for m in nr), default=0) > 2 or max((abs(c) for c in nr.values()), default=0) > CAP:
                        ok = False; break
                    news[r1] = nr
                if not ok:
                    rejected[(v, r0)] = version; continue
                for r1 in consumers:
                    if not verify_full(v, cv, rest, rows[r1], news[r1]):
                        print(f"VERIFY FAILED v={v}"); sys.exit(1)
                for r1, nr in news.items():
                    rows[r1] = nr
                rows[r0] = {}; alive[r0] = False
                log["sweep_ops"].append({"var": v, "def_row": r0, "n_consumers": len(consumers)})
                ops += 1
                fired = True
                version += 1
                break
            if fired: break
        if not fired:
            return ops

# ---------------- span drops ----------------
def elim(rows_list, P):
    mons = {}
    vecs = []
    for r in rows_list:
        d = {}
        for m, c in r.items():
            if m not in mons: mons[m] = len(mons)
            d[mons[m]] = c % P
        vecs.append(d)
    piv = {}
    deps = {}
    for idx, vec in enumerate(vecs):
        cur = dict(vec)
        mult = {idx: 1}
        is_dep = True
        while cur:
            col = min(cur)
            if col in piv:
                pv, pm, _ = piv[col]
                f = cur[col]
                for c2, v2 in pv.items():
                    nc = (cur.get(c2, 0) - f * v2) % P
                    if nc: cur[c2] = nc
                    elif c2 in cur: del cur[c2]
                for r2, m2 in pm.items():
                    nm = (mult.get(r2, 0) - f * m2) % P
                    if nm: mult[r2] = nm
                    elif r2 in mult: del mult[r2]
            else:
                piv[col] = (dict(cur), dict(mult), idx)
                is_dep = False
                break
        if is_dep and vec:
            deps[idx] = dict(mult)
    return len(piv), deps

def crt_pair(a1, m1, a2, m2):
    inv = pow(m1, -1, m2)
    return (a1 + m1 * ((a2 - a1) * inv % m2)) % (m1 * m2), m1 * m2

def rat_recon(y, M):
    if y == 0: return Fraction(0)
    B = int((M / 2) ** 0.5)
    s1, s2 = M, y % M
    t1, t2 = 0, 1
    while s2 > B:
        q = s1 // s2
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2
    if s2 == 0 or t2 == 0 or abs(s2) > B or abs(t2) > B: return None
    n, d = s2, t2
    if d < 0: n, d = -n, -d
    if (y * d - n) % M != 0: return None
    return Fraction(n, d)

def try_lift(rows_list, deps_list, d):
    ms = [(deps.get(d), P) for deps, P in zip(deps_list, PRIMES)]
    if any(m is None for m, _ in ms): return None
    ref = None
    for m, _ in ms:
        if ref is None:
            ref = max((k for k in m if k != d), key=lambda k: m[k], default=None)
    if ref is None: return None
    acc = {}
    for m, P in ms:
        yref = m.get(ref)
        if not yref: return None
        new_acc = {}
        for i in set(m) | {d}:
            yi = m.get(i, 1 if i == d else 0)
            ri = yi * pow(yref, -1, P) % P
            if i in acc:
                v, M2 = acc[i]
                nv, NM = crt_pair(v, M2, ri, P)
                new_acc[i] = (nv, NM)
            else:
                new_acc[i] = (ri, P)
        acc = new_acc
    xs = {}
    for i, (v, M2) in acc.items():
        if v > M2 // 2: v -= M2
        r = rat_recon(v % M2, M2)
        if r is None: return None
        xs[i] = r
    exp = collections.defaultdict(Fraction)
    for i, x in xs.items():
        if x:
            for m, c in rows_list[i].items():
                exp[m] += x * c
    if all(c == 0 for c in exp.values()):
        return xs
    return None

def drop_pass():
    """mark alive[i]=False for exactly the rows proved in the Q-span of other ALIVE rows.
    Lazy prime escalation: prime 1 gives a superset of Q-dependencies; the exact
    Fraction lift+proof decides each drop. More primes only for unlifted rows."""
    live_idx = [i for i in range(len(rows)) if alive[i] and rows[i]]
    live_rows = [rows[i] for i in live_idx]
    deps_by_prime = []
    dropped = 0
    for pi, P in enumerate(PRIMES):
        n, deps = elim(live_rows, P)
        deps_by_prime.append(deps)
        cand = set(deps_by_prime[0])
        for k in range(1, pi + 1):
            cand &= set(deps_by_prime[k])
        print(f"    prime rank {n}, deps {len(deps)} (intersect {len(cand)})", flush=True)
        drops = []
        for d in sorted(cand):
            xs = try_lift(live_rows, deps_by_prime[:pi + 1], d)
            if xs is not None:
                drops.append((d, xs))
        print(f"    proved with {pi+1} prime(s): {len(drops)}", flush=True)
        if drops or pi == len(PRIMES) - 1:
            for d, _ in drops:
                alive[live_idx[d]] = False
                log["dropped_rows"].append(live_idx[d])
            return len(drops)
    return 0

t0 = time.time()
for it in range(4):
    s = sweep_pass()
    d = drop_pass()
    log["iterations"].append({"iter": it, "sweep_ops": s, "drops": d})
    print(f"iteration {it}: sweep ops {s}, drops {d}  [{time.time()-t0:.0f}s]", flush=True)
    if s == 0 and d == 0:
        break

surv_rows = [r for i, r in enumerate(rows) if alive[i] and r]
allv = set()
for r in surv_rows:
    for m in r: allv.update(m)
print(f"FINAL: rows 4552 -> {len(surv_rows)}; vars 4973 -> {len(allv)}", flush=True)
mx = max(abs(c) for r in surv_rows for c in r.values())
print(f"max |row coeff| bits: {mx.bit_length()}", flush=True)

surv = sorted(allv)
remap = {v: i for i, v in enumerate(surv)}
new_rows = [[[c, [remap[x] for x in sorted(m)]] for m, c in sorted(r.items())] for r in surv_rows]
with gzip.open(f"{OUT}/stacked_residuals.json.gz", "wt") as f:
    json.dump(new_rows, f, separators=(",", ":"))
json.dump(log, open(f"{OUT}/stack_log.json", "w"))
print("saved stacked_residuals.json.gz", flush=True)

# ---------------- finalize ----------------
acc = collections.defaultdict(int)
degmax = 0
for row in new_rows:
    items = [(tuple(m), c) for c, m in row]
    degmax = max(degmax, max(len(m) for m, _ in items))
    for m1, c1 in items:
        for m2, c2 in items:
            acc[tuple(sorted(m1 + m2))] += c1 * c2
acc = {m: c for m, c in acc.items() if c}
degmax = max(len(m) for m in acc)
terms = sorted(acc.items(), key=lambda kv: kv[0])
used = sorted({v for m in acc for v in m})
print(f"Phi': monomials {len(acc)}, degree {degmax}, max coeff bits {max(abs(c) for c in acc.values()).bit_length()}, vars {len(used)} (contig {used == list(range(len(used)))})", flush=True)

outdir = Path(OUT) / "stacked"
outdir.mkdir(exist_ok=True)
tl = outdir / "phi_stacked.canonical.txt"
with tl.open("w") as f:
    f.write("# stacked variant (bounded elimination sweep + proved span drops): '<coeff> <var>:<exp> ...' sorted by sparse monomial key\n")
    for m, c in terms:
        f.write(f"{c} " + " ".join(f"{v}:{m.count(v)}" for v in sorted(set(m))) + "\n")
subprocess.run(["gzip", "-n", "-kf", str(tl)], check=True)
pkg = outdir / "package"
pkg.mkdir(exist_ok=True)
subprocess.run(["cp", f"{OUT}/stacked_residuals.json.gz", str(pkg / "residuals.json.gz")], check=True)
(pkg / "weights.json").write_text(json.dumps([1] * len(new_rows)))
(pkg / "variable-map.json").write_text(json.dumps(list(range(max(used) + 1))))
sha = hashlib.sha256(tl.with_suffix(tl.suffix + ".gz").read_bytes() if False else gzip.open(str(tl) + ".gz", "rb").read()).hexdigest()
print(f"term-list gz sha256: {sha}", flush=True)
print("RUN CHECKER:", flush=True)
r = subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "..", "artifact", "checker.py"),
                    "--package", str(pkg), "--termlist", str(tl) + ".gz"],
                   capture_output=True, text=True)
print(r.stdout[-2500:], flush=True)
print("checker exit:", r.returncode, flush=True)
