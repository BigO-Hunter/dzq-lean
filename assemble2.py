"""Assembly with the complete patch set: Lambda = 8 parameters (2 local classes x 4 lifts),
E_exc = {3,5,7,11,13,17,19,23} with per-prime Prop-4.2 constants.

Emits, in the artifact lane's sparse format, every leaf:
  F_Phi                                   phi2.terms.txt
  Phat_tau, P0_tau, thetafac_tau (x8)     Phat_tau*.terms.txt, P0_tau*.terms.txt, thetafac_tau*.terms.txt
  F_p for p in E_exc  (x8)                patch_p*.terms.txt
Note the patch polynomial is  pi_p*X^2*G_p(s1,s2,s3) - p^2 : the argument of the O_(p) formula is
X/p (m_p = p.O_p), so the cleared constant term is p^2, NOT 1.
"""
import hashlib
import json

from spoly import SPoly
from assemble import NV, X, Y, R, S, phi_poly, Phat, P0, theta_factor, A_poly, D_poly, G_poly

TAUS = [1, 17, 33, 49, 3, 11, 19, 27]


def patch_poly(A_q, B_q, a_q, pi_q, p):
    """pi_p * G_p(s1,s2,s3) - p^2 X^2.

    The condition encoded is X not in Z_(p), i.e. 1/X in m_p: the O_(p) formula is applied to the
    argument x = (1/X)/p, so pi x^2 G = 1 becomes pi G = p^2 X^2.  (The alternative pi X^2 G - p^2
    encodes X in m_p instead, which is the wrong side of the duality -- see POLYNOMIAL_LITERAL.md.)
    """
    s1 = SPoly.var(NV, Y)
    s2 = SPoly.var(NV, R)
    s3 = SPoly.var(NV, S)
    D = 1 + 4 * A_q
    bracket = (D * (s1 - s1 ** 2) + (a_q - A_q)
               - B_q * (s2 ** 2 + s2 * s3 - A_q * (s3 ** 2)))
    return pi_q * bracket - SPoly.const(NV, p * p) * (SPoly.var(NV, X) ** 2)


def write_termlist(path, name, p, extra=""):
    terms = p.as_int()
    items = sorted(terms.items())
    lines = ["# %s (sparse term list, '<coeff> <var>:<exp> ...'), sorted by monomial key" % name,
             "# vars: 0=X 1=a 2=b 3=y 4=r 5=s 6=zeta 7=zeta' 8=b1 9=sigma 10=upsilon 11=iota",
             "# terms: %d   degrees: %s%s" % (len(items), p.degs(), extra)]
    for k, c in items:
        parts = [str(c)]
        for i, e in enumerate(k):
            if e:
                parts.append("%d:%d" % (i, e))
        lines.append(" ".join(parts))
    data = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(data)
    return len(items), hashlib.sha256(data.encode()).hexdigest()


def main():
    with open("perprime.json") as f:
        pp = json.load(f)
    out = {}
    print("%-18s %8s  %s" % ("object", "terms", "sha256"))
    n, h = write_termlist("phi2.terms.txt", "phi (F_Phi)", phi_poly())
    out["phi"] = {"terms": n, "sha256": h, "file": "phi2.terms.txt"}

    for tau in TAUS:
        for name, poly in (("Phat_tau%d" % tau, Phat(tau)), ("P0_tau%d" % tau, P0(tau))):
            fname = ("Phat_tau%d.terms.txt" if name.startswith("Phat") else "P0_tau%d.terms.txt") % tau
            n, h = write_termlist(fname, name, poly)
            out[name] = {"terms": n, "sha256": h, "file": fname}
    for tau in TAUS:
        n, h = write_termlist("thetafac_tau%d.terms.txt" % tau, "thetafac_tau%d" % tau,
                              theta_factor(tau))
        out["thetafac_tau%d" % tau] = {"terms": n, "sha256": h,
                                       "file": "thetafac_tau%d.terms.txt" % tau}
        print("%-18s %8d  %s" % ("thetafac_tau%d" % tau, n, h[:32]))

    for pkey in sorted(pp, key=int):
        p = int(pkey)
        e = pp[pkey]
        poly = patch_poly(e["A"], e["B"], e["a"], e["pi"], p)
        fname = "patch_p%d.terms.txt" % p
        n, h = write_termlist(fname, "patch_p%d" % p, poly,
                              extra="   (pi=%d, A=%d, B=%d, a=%d)" % (e["pi"], e["A"], e["B"], e["a"]))
        out["patch_p%d" % p] = {"terms": n, "sha256": h, "file": fname,
                                "constants": {"pi": e["pi"], "A": e["A"], "B": e["B"],
                                              "a": e["a"], "d": e["d"], "q": e["q"],
                                              "Delta": e["Delta"]}}
        print("%-18s %8d  %s" % ("patch_p%d" % p, n, h[:32]))

    with open("branches2.json", "w") as f:
        json.dump({"Lambda": TAUS, "objects": out}, f, indent=1, sort_keys=True)
    print("\nbranches2.json written (%d objects)" % len(out))


if __name__ == "__main__":
    main()
