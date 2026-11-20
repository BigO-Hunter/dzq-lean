# R_COINCIDENCE.md — T1 precondition verdict: **REFUTED**

T1 ("share conics per root-point via joint norm tree", est −960) required that
some of the 37 contact sites' conic parameters `r` coincide — statically (same
variable) or semantically (forced equal at every solution). Both are false.

## What the conic `r` actually is

`q_conic{13,10,6}` input layout is `r;A0;B0;...` (source/modules/q_conic13.json:
`input_layout`). Construction-map: the first argument of every conic
instantiation is a **distinct** variable:

| conic | instances | first-arg (r) values |
|---|---|---|
| q_conic13 | 13 | 137, 119, 138, 139, 140, 157–164 |
| q_conic10 | 16 | 142–156, 165–172 |
| q_conic6 | 8 | 141 and two others in 141–148 range |

Resolve via Z_definition (first_local 27) log names: 137 = "affine numerator",
138–172 = **"ordinary contact"** (one variable per contact position 0–36),
119 = arithmetic carrier. 37 sites → 37 distinct r-variables. Zero static
sharing. `Z_definition` exposes `contact_scale=47027`, `contact_shift=3`,
`contact_W=25878772920`, `ordinary_contact_count=37` — the contacts sit at 37
distinct multiples (arithmetic progression), not ~13 shared roots.

In `q_compare4` the r enters the joint chart as `K=(A−r)·p` (construction_log,
5×), i.e. r is the site root point Q_j's chart parameter with
`2Q_j = n_j·Pstar`, `n_j` distinct per contact (root_index_semantics,
root_source_contract). Distinct positive n_j ⟹ Q_i ≠ ±Q_j ⟹ r_i ≠ r_j **at
every solution** (x(P)=x(Q) ⟺ P=±Q over the base field).

## Residual-level sealing (measured, residuals.json.gz, 4,552 rows)

- Site local spans (compare+conic+pole subtree per site): **0 overlaps**.
- Residuals containing ≥2 r-vars exist (42, in lucas/full compare blocks at
  sites 19, 20, 23, 24 — the "shared target" comparisons), but each is a
  quadratic relation in 2–3 r's **plus fresh aux variables**
  (e.g. resid 1998: −11·r137² + 24·r137·r138 − 22·r138² + w1574 = 0). None is
  a linear r_i − r_j (+const) relation: **0 hits**.
- No pair of r's is therefore forced equal or proportional anywhere in the
  source or the 551-transform certificate output.

## Consequence for T1

The coincidence classes are 37 singletons. "One conic per root point" with a
shared r would ADD constraints r_i = r_j between distinct contact points —
unsatisfiable (n_i + n_j > 0, n_i ≠ n_j), so Φ′ would have an **empty** zero
set where Φ has the integer inputs. Solution-set preservation (the iff) fails
in both readings of "root point" (contact carrier and A/S/T/Z/J chart — the
conic r is neither; those live at Z_definition locals 2–21 / 193–238 and are
not conic inputs). The "−960" estimate assumed 37→~13 collapse; measured
collapse is 37→37. Within a site the norm tree is already fully merged
(norm_root = 1 variable per site, pole_inputs = [r, θ, W]) — there is no
within-site slack left for the tree to absorb either.

**T1 is dead. Not forced, not salvageable by reweighting or partial classes
(all classes are size 1). This is the clean refutation the lane asked for.**
