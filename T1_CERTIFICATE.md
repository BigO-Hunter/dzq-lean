# T1_CERTIFICATE.md — no transform entry exists; refutation record

## Status: T1 aborted at precondition (task step 1). No certificate entry.

The 551-transform certificate language (`certificate.jsonl.gz`, checked by
`verify_certificate.py`) admits projection-preserving moves: invertible row
ops, eliminations modulo retained equations, definition eliminations, power
circuits, shears, block replacements. Every accepted move preserves the
solution set exactly (projection equality, machine-checked).

T1 would have needed a move of a kind the certificate does **not** contain and
cannot contain soundly: **variable identification** (identifying r_i := r_j
across conic instances). Identification preserves solution sets only when the
identified variables are already equal on the whole solution set (i.e. some
residual chain forces r_i = r_j). The measured system has:

- zero residuals with linear part r_i − r_j (+const) (0/4,552);
- no certificate row defining any two of {119, 137..172} to a common value;
- semantic forcing in the opposite direction: r_j = x(Q_j) with
  2Q_j = n_j·Pstar, {n_j} an arithmetic progression (contact_scale 47027,
  contact_shift 3, 37 positions) — pairwise distinct and non-opposite at every
  solution of the comparison system.

Hence a T1 identification row would change Φ's zero set (to ∅ — the merged
constraint is unsatisfiable), failing the iff `Φ'=0 ⇔ Φ=0` that
`verify_certificate.py` exists to guarantee. There is no reweighting, partial
class, or tree-reorganization variant that avoids this: all coincidence
classes are singletons, and each site's norm tree already collapses to one
root W_j feeding its own pole test.

A within-site certificate entry for T1 is likewise vacuous: the joint norm
tree per site is already the merged form (norm_tree → norm_root 78, 14→7→4→2
levels; first-norm denominator fusion already shipped in v4).

**Death certificate:** T1 = "share conics per root-point via joint norm tree"
is refuted by the variable map + construction map + residual support analysis.
The transform-certificate substrate is untouched; no new entry required.
