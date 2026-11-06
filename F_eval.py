"""The assembled polynomial as a self-contained straight-line evaluator (exact, Fractions).

This is F = (F_main * F_patch)^2 + (X*iota - 1)^2 with the constants of this lane:
  S = {2}, u = 1, pi = 2, Lambda = (1, 3)   [verified local cover]
  F_patch = F_2 only  --  the other E_exc primes are the NAMED BLOCKER (see POLYNOMIAL_LITERAL.md)

evaluate(X, witness) returns a Fraction.  F == 0 means "witness found".

Usage:  python3 F_eval.py            # runs the built-in self-checks
"""
from fractions import Fraction as Q

PI = 2
U = 1
LAMBDA = (1, 3)


def _A(a):
    return 1 + 4 * a * a


def _G(a, b):
    return 16 * a ** 4 * b ** 2 - (b - 1) ** 4 * (1 + 4 * a * a)


def _N(a, b, X):
    z = X ** 3
    return a * a * z * z * _G(a, b)


def _D(a, b, X):
    z = X ** 3
    return _A(a) * b * b * (1 - z - a * a * z * z)


def _delta(a, tau):
    return 1 - _A(a) * (tau * tau)


def _Phat(a, b, X, tau, y, r, s):
    A = _A(a)
    N = _N(a, b, X)
    D = _D(a, b, X)
    d = _delta(a, tau)
    B = b * PI
    return d * (N * N - A * y * y * D * D) - 16 * B * (r * r - A * s * s) * D * D - 16 * D * D


def _P0(a, b, X, tau, y, r, s):
    A = _A(a)
    D = _D(a, b, X)
    d = _delta(a, tau)
    B = b * PI
    return -d * A * y * y - 16 * B * (r * r - A * s * s) - 16


def _F_Phi(a, b, b1, sigma, upsilon):
    return (b * b1 - 1 - sigma * PI) ** 2 + (a - U - upsilon * PI) ** 2


def _F_Theta(a, b, X, y, r, s, zeta, zetap):
    acc = Q(1)
    for tau in LAMBDA:
        d = _delta(a, tau)
        D = _D(a, b, X)
        p1 = d * zeta - 1
        p3 = D * zetap - 1
        acc *= p1 * p1 + _Phat(a, b, X, tau, y, r, s) ** 2 + (p3 * _P0(a, b, X, tau, y, r, s)) ** 2
    return acc


def _F_patch_p2(X, y, r, s):
    """x in Z_(2) <=> x = 0 or 10x^2(7 + 5x1 - 5x1^2 - 2x2^2 - 2x2x3 + 2x3^2) = 1 ; witnesses (y,r,s)."""
    form = 7 + 5 * y - 5 * y * y - 2 * r * r - 2 * r * s + 2 * s * s
    return 10 * X * X * form - 1


def evaluate(X, w):
    """w = dict(a,b,y,r,s,zeta,zetap,b1,sigma,upsilon,iota)."""
    X = Q(X)
    a, b, y, r, s = (Q(w["a"]), Q(w["b"]), Q(w["y"]), Q(w["r"]), Q(w["s"]))
    zeta, zetap = Q(w["zeta"]), Q(w["zetap"])
    b1, sigma, upsilon, iota = Q(w["b1"]), Q(w["sigma"]), Q(w["upsilon"]), Q(w["iota"])
    f_phi = _F_Phi(a, b, b1, sigma, upsilon)
    f_theta = _F_Theta(a, b, X, y, r, s, zeta, zetap)
    f_main = f_phi ** 2 + f_theta ** 2
    f_patch = _F_patch_p2(X, y, r, s)          # only p = 2 ; BLOCKER: the other E_exc primes
    return (f_main * f_patch) ** 2 + (X * iota - 1) ** 2


def selftest():
    from assemble import Phat, P0, phi_poly, theta_factor, patch2
    import random
    from fractions import Fraction as F
    rng = random.Random(3)
    # the evaluator must agree with the sparse term lists of assemble.py
    checks = {"phi": (phi_poly(), lambda w: _F_Phi(Q(w["a"]), Q(w["b"]), Q(w["b1"]),
                                                  Q(w["sigma"]), Q(w["upsilon"]))),
              "patch2": (patch2(), lambda w: _F_patch_p2(Q(w["X"]), Q(w["y"]), Q(w["r"]), Q(w["s"])))}
    for tau in LAMBDA:
        checks["Phat%d" % tau] = (Phat(tau), (lambda t: lambda w: _Phat(
            Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"])))(tau))
        checks["P0%d" % tau] = (P0(tau), (lambda t: lambda w: _P0(
            Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"])))(tau))
        checks["thetafac%d" % tau] = (theta_factor(tau), (lambda t: lambda w: (
            (_delta(Q(w["a"]), t) * Q(w["zeta"]) - 1) ** 2
            + _Phat(Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"])) ** 2
            + ((_D(Q(w["a"]), Q(w["b"]), Q(w["X"])) * Q(w["zetap"]) - 1)
               * _P0(Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"]))) ** 2))(tau))
    for name, (p, fn) in checks.items():
        for _ in range(20):
            w = {k: F(rng.randrange(-6, 7), rng.choice([1, 1, 2, 3])) for k in
                 ("X", "a", "b", "y", "r", "s", "zeta", "zetap", "b1", "sigma", "upsilon", "iota")}
            v1 = p_eval(p, w)
            v2 = fn(w)
            assert v1 == v2, (name, w, v1, v2)
        print("ok   evaluator == sparse term list for", name)
    # F reproduces the fold structure
    w = {k: F(0) for k in ("a", "b", "y", "r", "s", "zeta", "zetap", "b1", "sigma", "upsilon", "iota")}
    w["X"] = F(3, 2)
    w["iota"] = F(2, 3)
    val = evaluate(F(3, 2), w)
    print("sample evaluation at a degenerate witness, F =", val)


def p_eval(p, w):
    names = ["X", "a", "b", "y", "r", "s", "zeta", "zetap", "b1", "sigma", "upsilon", "iota"]
    vals = [Q(w[n]) for n in names]
    tot = Q(0)
    for k, c in p.d.items():
        term = Q(c)
        for i, e in enumerate(k):
            if e:
                term *= vals[i] ** e
        tot += term
    return tot


if __name__ == "__main__":
    selftest()
