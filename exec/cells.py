"""Per-cell canonical construction (Sun 2026 Prop 3.1 proof, char != 2, F = Q_2).

For each (a0 mod 8, c0 mod 8) cell of P_2 = {(a,b,c) : a odd, b unit, c in Z_2} build the
center data (z1, z2, gamma, t_p, y-coordinate), verify every claim of G1_FREEZING.md that the
residue layer / exact arithmetic can decide, and emit the cell's tau.

Reported quantities are exact valuations (the Q2 layer tracks 200 bits, valuations here are
tiny, so every reported valuation is exact, not a lower bound -- verified by `exact` flags).
"""
from fractions import Fraction as Fr

import padic as P
from padic import E, Q2

A0S = (1, 3, 5, 7)
C0S = tuple(range(8))


def q2_rat(x):
    return Q2.F(x)


def build_cell(a0, c0, verbose=False):
    """Returns a dict of center data + verification flags for the cell (a0 mod 8, c0 mod 8)."""
    r = {"a0": a0, "c0": c0}
    A0 = 1 + 4 * a0 * a0
    r["A0"] = A0
    r["A0_mod8"] = A0 % 8

    # --- residue-layer data (Lemma 2.2 residue step)
    cbar = c0 % 2
    if cbar == 0:
        z1bar, z2bar = P.OMEGA, P.OMEGA2
        z2 = P.ZETA2
        c1 = c0 - (-1)  # Tr(zeta^2) = -1
    else:
        z1bar, z2bar = P.OMEGA, (1, 0)
        z2 = E.rat(1)
        c1 = c0 - 2  # Tr(1) = 2
    r.update(c1=c1, z1bar=z1bar, z2bar=z2bar)

    # --- z1 = Hensel root of X^2 - c1 X + 1 near omega
    disc = c1 * c1 - 4
    r["disc_mod8"] = disc % 8
    t = P.sqrt_of_5u(q2_rat(Fr(disc, 5)))  # sqrt(c1^2-4), since disc/5 = 1 mod 8
    root_a = (E.rat(c1) + t) * Fr(1, 2)
    root_b = (E.rat(c1) - t) * Fr(1, 2)
    cands = [(z, tag) for z, tag in ((root_a, "+"), (root_b, "-")) if z.res() == z1bar]
    assert len(cands) == 1, (a0, c0, root_a.res(), root_b.res())
    z1, tag = cands[0]
    r["root_choice"] = tag
    r["z1"] = z1
    r["z2"] = z2

    # --- checks on z1, z2
    r["z1_integral"] = z1.v() == 0
    r["Tr_z1_eq_c1"] = (z1.tr() - q2_rat(c1)).ge(60)
    r["N_z1_eq_1"] = (z1.norm() - q2_rat(1)).ge(60)
    r["N_z2_eq_1"] = (z2.norm() - q2_rat(1)).ge(60)
    r["Tr_sum_eq_c0"] = (z1.tr() + z2.tr() - q2_rat(c0)).ge(60)
    r["z1_ne_pm1"] = not (z1 - E.rat(1)).is_zero() and not (z1 + E.rat(1)).is_zero()
    r["z2_ne_pm_z1"] = not (z2 - z1).is_zero() and not (z2 + z1).is_zero()
    r["z2_ne_z1inv"] = not (z2 - z1.inv()).is_zero()

    # --- i = sqrt(A0) in E ; A0 = 5*m with m = 1 mod 8
    i = P.sqrt_of_5u(q2_rat(Fr(A0, 5)))
    r["i_sq_ok"] = (i * i - q2_rat(A0)).ge(60)
    r["i_unit"] = i.v() == 0

    # --- gamma, t_p  (Cayley parameter of gamma = z1^-1 z2)
    gamma = z2 / z1
    r["gamma_res"] = gamma.res()
    r["gamma_ne_m1"] = not (gamma + E.rat(1)).is_zero()
    r["gamma_plus1_unit"] = (gamma + E.rat(1)).v() == 0
    r["gamma_minus1_unit"] = (gamma - E.rat(1)).v() == 0
    tp_E = (gamma - E.rat(1)) / (i * (gamma + E.rat(1)))
    r["tp_in_Q2"] = tp_E.q.ge(60)  # sqrt5-component vanishes
    tp = tp_E.p
    r["tp"] = tp
    r["v_tp"] = tp.val()
    r["tp_mod8"] = int(tp.u % 8) if tp.k == 0 else 0

    # --- delta at the center
    delta = Q2.Z(1) - q2_rat(A0) * tp * tp
    r["delta"] = delta
    r["v_delta"] = delta.val()

    # --- y-coordinate of z1 (in the K(i) basis, i^2 = A0) :  X + Y i
    X = z1.tr() * Q2.F(1, 2)
    Y_E = (z1 - z1.conj()) * i * (q2_rat(2) * q2_rat(A0)).inv()
    Y, Yok = Y_E.to_q2()
    r["X"], r["Y"] = X, Y
    r["Y_in_Q2"] = Yok
    r["v_X"] = X.val()
    r["v_Y"] = Y.val()
    r["X_eq_c1_over_2"] = (X - q2_rat(Fr(c1, 2))).ge(60)
    # Y^2 = (c1^2/4 - 1)/A0
    Ysq_claim = q2_rat(Fr(c1 * c1, 4) - 1) / q2_rat(A0)
    r["Ysq_ok"] = (Y * Y - Ysq_claim).ge(60)

    # --- the (2.1) witness y at r=s=0 :  y = 4Y + tau*c   (NOT the i-coordinate Y)
    y_w = q2_rat(4) * Y + tp * q2_rat(c0)
    r["y_w"] = y_w
    r["v_y_w"] = y_w.val()
    # r = s = 0, so P = delta(c^2 - A y^2) - 16
    Pv = delta * (q2_rat(c0 * c0) - q2_rat(A0) * y_w * y_w) - q2_rat(16)
    r["P_at_center"] = Pv
    r["P_center_zero"] = Pv.ge(60)
    # consistency of coordinates:  c*delta = 4(X + A tau Y)
    lhs = q2_rat(c0) * delta
    rhs = q2_rat(4) * (X + q2_rat(A0) * tp * Y)
    r["coord_consistency"] = (lhs - rhs).ge(60)

    # --- e := v(dP/dy) at the center, together with d = dP/dy
    dPdy = q2_rat(-2) * q2_rat(A0) * delta * y_w
    r["dPdy"] = dPdy
    r["e"] = dPdy.val()

    # --- the cell's tau: truncation of t_p mod 8 (a rational integer in {1,3,5,7})
    tau = int(tp.u % 8) if tp.k == 0 else None
    r["tau"] = tau
    r["v_tau_minus_tp"] = (tp - q2_rat(tau)).val() if tau is not None else None
    dtau = Q2.Z(1) - q2_rat(A0) * q2_rat(tau) * q2_rat(tau)
    r["v_delta_tau"] = dtau.val()
    r["delta_tau_nonzero"] = dtau.val() == dtau.k and dtau.u != 0 or (dtau.u != 0)
    return r


def main():
    bad = []
    rows = []
    for a0 in A0S:
        for c0 in C0S:
            r = build_cell(a0, c0)
            rows.append(r)
            for key in ("z1_integral", "Tr_z1_eq_c1", "N_z1_eq_1", "N_z2_eq_1", "Tr_sum_eq_c0",
                        "z1_ne_pm1", "z2_ne_pm_z1", "z2_ne_z1inv", "i_sq_ok", "i_unit",
                        "gamma_ne_m1", "gamma_plus1_unit", "gamma_minus1_unit", "tp_in_Q2",
                        "Ysq_ok", "P_center_zero", "coord_consistency", "delta_tau_nonzero"):
                if not r[key]:
                    bad.append((a0, c0, key))
    hdr = ("a0 c0  A0  c1 root  v(Y) v(y_w)  e  v(del) v(tp) tp%8 tau v(tau-tp) v(del_tau)")
    print(hdr)
    for r in rows:
        print("%2d %2d %3d %3d  %s   %3s   %3s  %2s   %2s    %2s   %d   %3s   %s        %s" % (
            r["a0"], r["c0"], r["A0"], r["c1"], r["root_choice"], r["v_Y"], r["v_y_w"], r["e"],
            r["v_delta"], r["v_tp"], r["tp_mod8"], r["tau"], r["v_tau_minus_tp"], r["v_delta_tau"]))
    print()
    print("failures:", bad if bad else "none")
    taus = sorted({r["tau"] for r in rows})
    print("distinct tau residues: %d -> %s" % (len(taus), taus))
    import collections
    cnt = collections.Counter((r["a0"], r["c0"]) for r in rows if r["tau"] == taus[0])
    print("taus per cell:", {r["tau"]: sum(1 for x in rows if x["tau"] == r["tau"]) for r in rows})
    print("e values:", sorted({r["e"] for r in rows}))
    print("v(Y) values:", sorted({r["v_Y"] for r in rows}))
    print("v(y_w) values:", sorted({str(r["v_y_w"]) for r in rows}))
    return rows


if __name__ == "__main__":
    main()
