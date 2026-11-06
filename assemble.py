"""Assemble the branch polynomials of F literally, in the artifact lane's sparse format.

Variables (indices used in the term lists):
  0 X   1 a   2 b   3 y   4 r   5 s   6 zeta   7 zeta'   8 b1   9 sigma   10 upsilon   11 iota

Branch objects emitted (all as sparse term lists, exact integers):
  phi        : F_Phi = (b*b1 - 1 - sigma*Pi)^2 + (a - u - upsilon*Pi)^2      [Pi = 2, u = 1]
  Phat_<tau> : P_hat_tau = delta(N^2 - A y^2 D^2) - 16 B (r^2 - A s^2) D^2 - 16 D^2
  P0_<tau>   : P0_tau   = -delta A y^2 - 16 B (r^2 - A s^2) - 16
  thetafac_<tau> : (delta zeta - 1)^2 + Phat^2 + ((D zeta' - 1) P0)^2
  patch2     : the p = 2 patch polynomial of G2_REDERIVATION.md 1
Term lists are sorted by the sparse monomial key, exactly like dzq-artifact's canonical form.
"""
import hashlib

from spoly import SPoly

NV = 12
X, A_, B_, Y, R, S, Z, ZP, B1, SG, UP, IO = range(NV)

PI = 2   # Pi_S
U = 1    # u


def A_poly():
    """A = 1 + 4a^2"""
    a = SPoly.var(NV, A_)
    return SPoly.const(NV, 1) + 4 * (a ** 2)


def G_poly():
    """G = 16 a^4 b^2 - (b-1)^4 (1+4a^2)"""
    a = SPoly.var(NV, A_)
    b = SPoly.var(NV, B_)
    return 16 * (a ** 4) * (b ** 2) - ((b - SPoly.const(NV, 1)) ** 4) * A_poly()


def N_poly():
    """N = a^2 z^2 G with z = iota^3.

    iota is the inversion witness (X*iota = 1): the polynomial defines (U m_w)^{-1}, i.e. the set
    Q \ Z, so the h-bridge variable x of Sun (9.1) is iota, not X.  See POLYNOMIAL_LITERAL.md 2.
    """
    a = SPoly.var(NV, A_)
    z = SPoly.var(NV, IO) ** 3
    return (a ** 2) * (z ** 2) * G_poly()


def D_poly():
    """D = (1+4a^2) b^2 (1 - z - a^2 z^2), z = iota^3"""
    a = SPoly.var(NV, A_)
    b = SPoly.var(NV, B_)
    z = SPoly.var(NV, IO) ** 3
    return A_poly() * (b ** 2) * (SPoly.const(NV, 1) - z - (a ** 2) * (z ** 2))


def Phat(tau):
    """P_hat_tau = delta(N^2 - A y^2 D^2) - 16*B*(r^2 - A s^2)*D^2 - 16*D^2,  B = 2b."""
    from fractions import Fraction as Fr

    A = A_poly()
    N = N_poly()
    D = D_poly()
    y = SPoly.var(NV, Y)
    r = SPoly.var(NV, R)
    s = SPoly.var(NV, S)
    delta = SPoly.const(NV, 1) - A * SPoly.const(NV, Fr(tau * tau))
    B = SPoly.const(NV, 2) * SPoly.var(NV, B_)  # B = b*pi = 2b
    D2 = D ** 2
    return delta * (N ** 2 - A * (y ** 2) * D2) - 16 * B * (r ** 2 - A * (s ** 2)) * D2 - 16 * D2


def P0(tau):
    from fractions import Fraction as Fr

    A = A_poly()
    y = SPoly.var(NV, Y)
    r = SPoly.var(NV, R)
    s = SPoly.var(NV, S)
    delta = SPoly.const(NV, 1) - A * SPoly.const(NV, Fr(tau * tau))
    B = SPoly.const(NV, 2) * SPoly.var(NV, B_)
    return -delta * A * (y ** 2) - 16 * B * (r ** 2 - A * (s ** 2)) - 16


def phi_poly():
    b = SPoly.var(NV, B_)
    a = SPoly.var(NV, A_)
    b1 = SPoly.var(NV, B1)
    sg = SPoly.var(NV, SG)
    up = SPoly.var(NV, UP)
    f1 = b * b1 - SPoly.const(NV, 1) - PI * sg
    f2 = a - SPoly.const(NV, U) - PI * up
    return f1 ** 2 + f2 ** 2


def theta_factor(tau):
    """(delta zeta - 1)^2 + Phat^2 + ((D zeta' - 1) P0)^2"""
    from fractions import Fraction as Fr

    A = A_poly()
    D = D_poly()
    delta = SPoly.const(NV, 1) - A * SPoly.const(NV, Fr(tau * tau))
    z = SPoly.var(NV, Z)
    zp = SPoly.var(NV, ZP)
    p1 = delta * z - SPoly.const(NV, 1)
    p3 = D * zp - SPoly.const(NV, 1)
    return p1 ** 2 + Phat(tau) ** 2 + (p3 * P0(tau)) ** 2


def patch2():
    """x in Z_(2)  <=>  x = 0 or 10x^2(7 + 5x1 - 5x1^2 - 2x2^2 - 2x2x3 + 2x3^2) - 1 = 0.
       Emitted with (X, y, r, s) as (x, x1, x2, x3): 10X^2*(...)-1."""
    x = SPoly.var(NV, X)
    q1 = SPoly.var(NV, Y)
    q2 = SPoly.var(NV, R)
    q3 = SPoly.var(NV, S)
    form = (SPoly.const(NV, 7) + 5 * q1 - 5 * (q1 ** 2) - 2 * (q2 ** 2)
            - 2 * q2 * q3 + 2 * (q3 ** 2))
    return 10 * (x ** 2) * form - SPoly.const(NV, 1)


# ---------------------------------------------------------------- emit
def canon_key(k):
    return tuple(k)


def write_termlist(path, name, p, header_extra=""):
    terms = p.as_int()
    items = sorted(terms.items())
    lines = ["# %s (sparse term list, '<coeff> <var>:<exp> ...'), sorted by monomial key" % name,
             "# vars: 0=X 1=a 2=b 3=y 4=r 5=s 6=zeta 7=zeta' 8=b1 9=sigma 10=upsilon 11=iota",
             "# terms: %d   degrees: %s%s" % (len(items), p.degs(), header_extra)]
    for k, c in items:
        parts = [str(c)]
        for i, e in enumerate(k):
            if e:
                parts.append("%d:%d" % (i, e))
        lines.append(" ".join(parts))
    data = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(data)
    h = hashlib.sha256(data.encode()).hexdigest()
    return len(items), h


def main():
    import json

    out = {}
    print("%-14s %8s %6s %s" % ("object", "terms", "sha256", "degrees"))
    objs = [("phi", phi_poly()), ("patch2", patch2())]
    for tau in (1, 3):
        objs.append(("Phat_tau%d" % tau, Phat(tau)))
        objs.append(("P0_tau%d" % tau, P0(tau)))
    for name, p in objs:
        n, h = write_termlist("%s.terms.txt" % name, name, p)
        out[name] = {"terms": n, "sha256": h, "degrees": p.degs()}
        print("%-14s %8d %6s %s" % (name, n, h[:16], p.degs()))
    # theta factors are big; measure before writing
    for tau in (1, 3):
        p = theta_factor(tau)
        n, h = write_termlist("thetafac_tau%d.terms.txt" % tau, "thetafac_tau%d" % tau, p)
        out["thetafac_tau%d" % tau] = {"terms": n, "sha256": h, "degrees": p.degs()}
        print("%-14s %8d %6s %s" % ("thetafac_tau%d" % tau, n, h[:16], p.degs()))
    with open("branches.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
