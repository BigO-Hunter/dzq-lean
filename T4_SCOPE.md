# T4_SCOPE.md — pole-into-conic fusion (−250): stackability after T1's death

## Verdict: stackable is moot — T4 never depended on T1. It stands alone.

T4 fuses each site's `q_linearnormalpole` (10 locals × 37 = 370) into its
conic block's equations. The measured interface confirms the anatomy's read:

- `q_linearnormalpole` inputs are exactly `[r, theta, W]` (pole_inputs) — all
  three already live in the owning site's conic block (r = the site's input
  arg, θ = conic_private.theta local, W = norm_root local). No other site's
  variables are involved, so **no r-coincidence is needed anywhere in T4**.
- The fusion is row reorganization in one site's variable block at a time:
  fold the 8 pole residuals into the conic module's equation list and drop
  the 10 locals via the certificate's existing definition-elimination /
  elimination-modulo-retained-equation move classes. Projection-preserving,
  solution set untouched — the same certificate language as the 551 shipped
  moves.

Estimated −250 (anatomy) assumes the 10 locals compress to ~3 per site
(θ, s, S already exist; W and its tree rows absorb the pole rows). Exact
savings need a per-site elimination probe — the T5 sweep machinery on the
pole variables is the right tool. Ordering note: T4 composes with T5 and with
any arithmetic-lane win; with T1 dead it is the **largest remaining
certificate-class lever** (−250 of the ~−400 non-arithmetic total).

T2 (o8-height arithmetic surface) remains out of this lane's scope, as
instructed.
