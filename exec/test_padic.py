"""Sanity tests for padic.py: field laws, sqrt correctness, zeta identities."""
from fractions import Fraction as Fr

import padic as P
from padic import E, Q2


def val_ge(x, n):
    """x is a Q2 with |x| <= 2^-n proven."""
    return x.u == 0 or x.val() >= n


def chk(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    assert cond, name


def main():
    # Q2 basics
    a = Q2.Z(6)
    chk("v(6)=1", a.val() == 1)
    s = P.sqrt_unit(Q2.F(-5, 3))
    chk("s^2 = -5/3", val_ge(s * s - Q2.F(-5, 3), 60))
    chk("v(s)=0", s.val() == 0)
    s2 = P.sqrt_unit(Q2.F(33))
    chk("s2^2=33", val_ge(s2 * s2 - Q2.Z(33), 60))

    # zeta is a primitive cube root of unity, integral, trace -1, norm 1
    z = P.ZETA
    chk("zeta^2+zeta+1=0", (z * z + z + E.rat(1)).is_zero())
    chk("Tr(zeta)=-1", (z.tr() + Q2.Z(1)).is_zero_mod())
    chk("N(zeta)=1", (z.norm() + Q2.Z(-1)).is_zero_mod())
    chk("zeta integral", z.v() == 0)
    chk("zeta res = omega", z.res() == P.OMEGA)
    chk("zeta^-1 res = omega^2", z.inv().res() == P.OMEGA2)
    chk("Tr(zeta^2)=-1", (P.ZETA2.tr() + Q2.Z(1)).is_zero_mod())
    chk("zeta^2 res", P.ZETA2.res() == P.OMEGA2)

    # sqrt5
    sq = P.SQRT5
    chk("sqrt5^2=5", (sq * sq + E.rat(-5)).zero_to(60))
    chk("sqrt5 res = 1", sq.res() == (1, 0))
    chk("conj(sqrt5)=-sqrt5", (sq.conj() + sq).is_zero())

    # sqrt(5*m) for m=1 mod 8
    m = P.sqrt_of_5u(Q2.F(33))
    chk("sqrt(165)^2=165", (m * m + E.rat(-165)).zero_to(40))

    # conjugation is the nontrivial automorphism: fixes Q2, sends zeta->zeta^2
    chk("conj(zeta)=zeta^2", (z.conj() - P.ZETA2).is_zero())
    chk("(2zeta+1)^2 = -3", ((E(Q2.Z(1), Q2.Z(2)) * E(Q2.Z(1), Q2.Z(2))) + E.rat(3)).zero_to(60))

    # trace additivity / norm multiplicativity on a random element
    x = E(Q2.F(3, 5), Q2.F(7, 3))
    chk("N(x)=x*conj(x)", (x * x.conj()).q.is_zero_mod() and
        ((x * x.conj()).p - x.norm()).ge(60))
    chk("Tr(x)=x+conj(x)", (x + x.conj()).q.is_zero_mod() and
        ((x + x.conj()).p - x.tr()).ge(60))

    print("all padic sanity checks passed")


if __name__ == "__main__":
    main()
