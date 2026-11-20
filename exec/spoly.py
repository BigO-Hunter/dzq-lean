"""Sparse multivariate rational/integer polynomials: dict[(exp tuple)] -> Fraction/int.

Used to emit the literal term lists of the assembly's branches.
"""
from fractions import Fraction


class SPoly:
    __slots__ = ("d", "nv")

    def __init__(self, nv, terms=None):
        self.nv = nv
        self.d = {}
        if terms:
            for k, v in terms.items():
                if v:
                    self.d[k] = v

    @staticmethod
    def const(nv, c):
        return SPoly(nv, {tuple([0] * nv): c}) if c else SPoly(nv)

    @staticmethod
    def var(nv, i):
        e = [0] * nv
        e[i] = 1
        return SPoly(nv, {tuple(e): 1})

    def __add__(self, o):
        if isinstance(o, (int, Fraction)):
            o = SPoly.const(self.nv, o)
        r = dict(self.d)
        for k, v in o.d.items():
            r[k] = r.get(k, 0) + v
            if r[k] == 0:
                del r[k]
        return SPoly(self.nv, r)

    def __sub__(self, o):
        return self + (-o)

    def __neg__(self):
        return SPoly(self.nv, {k: -v for k, v in self.d.items()})

    def __mul__(self, o):
        if isinstance(o, (int, Fraction)):
            return SPoly(self.nv, {k: v * o for k, v in self.d.items()})
        r = {}
        for k1, v1 in self.d.items():
            for k2, v2 in o.d.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                r[k] = r.get(k, 0) + v1 * v2
        return SPoly(self.nv, {k: v for k, v in r.items() if v != 0})

    def __rmul__(self, o):
        return self * o

    def __pow__(self, n):
        r = SPoly.const(self.nv, 1)
        for _ in range(n):
            r = r * self
        return r

    def nterms(self):
        return len(self.d)

    def deg(self, i):
        return max((k[i] for k in self.d), default=0)

    def degs(self):
        return [self.deg(i) for i in range(self.nv)]

    def as_int(self):
        out = {}
        for k, v in self.d.items():
            assert Fraction(v).denominator == 1, (k, v)
            out[k] = int(v)
        return out
