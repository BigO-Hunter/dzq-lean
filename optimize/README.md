# LANE A3 — Score-Optimization Engine (dzq-optimize)

Board: "Z is Diophantine in Q" (dropped 2026-11-06). Score = k+1 free variables of
P(q, w_1..w_k) over Z with q in Q: q in Z IFF exists w in Q^k: P(q,w)=0.
Incumbents: 2.9e11 / 2.1e11 (CLAIMED, sorry in Lean). Tie order: variables > degree >
nonzero terms > max |coef|.

Deliverables (drafts for coordinator, nothing posted):
- OPTIMIZATION_MACHINERY.md — the compression calculus (techniques, costs, legality)
- PACKING_BOUNDARY.md — exactly which tuple-packing tricks are polynomially legal, + proved lower bound
- LIT_NOTES.md — citations; unfetchable = GAP

Status: in progress. Restart-resilient: commit early/often.
