"""Exact-ish 2-adic arithmetic: Q2 (with tracked precision) and E = Q2(zeta), zeta^2+zeta+1=0.

Basis {1, zeta} is an integral basis of O_E over Z_2 (E/Q_2 unramified quadratic), so an
element (p,q) is integral iff p,q are; residues mod M_E are the pair (p mod 2, q mod 2) in
F_4 = F_2[t]/(t^2+t+1).

Everything is tracked mod 2^PREC.  Valuations are exact whenever v < PREC.
"""

PREC = 200
MOD = 1 << PREC


def v2(n):
    if n == 0:
        return None
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


class Q2:
    """x = 2^k * u mod 2^(k+p), u odd."""

    __slots__ = ("k", "u", "p")

    def __init__(self, k, u, p=PREC):
        u %= 1 << p
        if u == 0:
            self.k, self.u, self.p = k, 0, p
            return
        t = v2(u)
        self.k, self.u, self.p = k + t, u >> t, p - t

    # ---- constructors
    @staticmethod
    def Z(n):
        if n == 0:
            return Q2(0, 0)
        return Q2(0, int(n))

    @staticmethod
    def F(x, den=None):
        from fractions import Fraction

        x = Fraction(x) if den is None else Fraction(x, den)
        if x == 0:
            return Q2(0, 0)
        num, d = x.numerator, x.denominator
        e = v2(d)
        d >>= e
        return Q2(-e, num * pow(d, -1, MOD))

    # ---- predicates
    def is_zero_mod(self):
        return self.u == 0

    def val(self):
        """Exact 2-adic valuation, or None when only '>= k+p' is known."""
        return None if self.u == 0 else self.k

    def ge(self, n):
        """True iff v(x) >= n (proved)."""
        if self.u == 0:
            return True
        return self.k >= n

    # ---- arithmetic
    def __neg__(self):
        return Q2(self.k, (-self.u) % (1 << self.p) or 0, self.p)

    def __add__(self, o):
        o = _c(o)
        if self.u == 0:
            return Q2(o.k, o.u, o.p)
        if o.u == 0:
            return Q2(self.k, self.u, self.p)
        k = min(self.k, o.k)
        abs_prec = min(self.k + self.p, o.k + o.p)
        p = abs_prec - k
        m1 = (self.u * pow(2, self.k - k, 1 << p)) % (1 << p)
        m2 = (o.u * pow(2, o.k - k, 1 << p)) % (1 << p)
        return Q2(k, m1 + m2, p)

    def __sub__(self, o):
        return self + (-_c(o))

    def __mul__(self, o):
        o = _c(o)
        if self.u == 0 or o.u == 0:
            return Q2(0, 0)
        p = min(self.p, o.p)
        return Q2(self.k + o.k, (self.u * o.u) % (1 << p), p)

    def inv(self):
        assert self.u != 0
        return Q2(-self.k, pow(self.u, -1, 1 << self.p), self.p)

    def __truediv__(self, o):
        return self * _c(o).inv()

    def __eq__(self, o):
        o = _c(o)
        # compare where both known
        p = min(self.k + self.p, o.k + o.p) - min(self.k, o.k)
        k = min(self.k, o.k)
        if p <= 0:
            return True
        m1 = (self.u * pow(2, self.k - k, 1 << p)) % (1 << p) if self.u else 0
        m2 = (o.u * pow(2, o.k - k, 1 << p)) % (1 << p) if o.u else 0
        return m1 == m2

    def __repr__(self):
        if self.u == 0:
            return "0(>=%d)" % self.k
        return "2^%d*%d(mod 2^%d)" % (self.k, self.u, self.k + self.p)


def _e(x):
    return x if isinstance(x, E) else E.rat(_c(x))


def _c(x):
    if isinstance(x, Q2):
        return x
    if isinstance(x, int):
        return Q2.Z(x)
    return Q2.F(x)


def sqrt_unit(a):
    """sqrt of a 2-adic unit a with a = 1 mod 8 (the root = 1 mod 4)."""
    a = _c(a)
    assert a.u != 0 and a.k == 0, a
    assert (a.u % 8) == 1, a.u % 8
    target = PREC // 2
    y = Q2.Z(1)
    for _ in range(24):
        d = a - y * y
        if d.u == 0 or d.val() >= target:
            return y
        y = (y + a * y.inv()) * Q2.F(1, 2)
    raise RuntimeError("sqrt_unit did not converge: %r" % (a,))


class E:
    """p + q*zeta in Q2(zeta), zeta^2 = -1 - zeta."""

    __slots__ = ("p", "q")

    def __init__(self, p, q):
        self.p, self.q = _c(p), _c(q)

    @staticmethod
    def rat(x):
        return E(_c(x), Q2.Z(0))

    def __add__(self, o):
        o = _e(o)
        return E(self.p + o.p, self.q + o.q)

    def __sub__(self, o):
        o = _e(o)
        return E(self.p - o.p, self.q - o.q)

    def __neg__(self):
        return E(-self.p, -self.q)

    def __mul__(self, o):
        if not isinstance(o, E):
            c = _c(o)
            return E(self.p * c, self.q * c)
        p1, q1, p2, q2 = self.p, self.q, o.p, o.q
        return E(p1 * p2 - q1 * q2, p1 * q2 + q1 * p2 - q1 * q2)

    def __rmul__(self, o):
        return self * o

    def conj(self):
        return E(self.p - self.q, -self.q)

    def norm(self):
        return self.p * self.p - self.p * self.q + self.q * self.q

    def inv(self):
        return E(self.conj().p / self.norm(), self.conj().q / self.norm())

    def __truediv__(self, o):
        if isinstance(o, E):
            return self * o.inv()
        c = _c(o)
        return E(self.p / c, self.q / c)

    def tr(self):
        return self.p * 2 - self.q

    def to_q2(self, tol=60):
        """(value, isInQ2): the zeta-coefficient must vanish."""
        return self.p, self.q.ge(tol)

    def res(self):
        """residue mod M_E as (a,b) in {0,1}^2 (element a + b*zeta of F_4)."""
        def r(x):
            return 0 if (x.u == 0 or x.k >= 1) else (x.u % 2)
        return (r(self.p), r(self.q))

    def v(self):
        vp, vq = self.p.val(), self.q.val()
        return min([v for v in (vp, vq) if v is not None], default=None)

    def is_zero(self):
        return self.p.is_zero_mod() and self.q.is_zero_mod()

    def ge(self, n):
        return self.p.ge(n) and self.q.ge(n)

    def zero_to(self, n):
        """True when z = 0 mod 2^n (proved)."""
        return self.p.ge(n) and self.q.ge(n)

    def __repr__(self):
        return "(%r) + (%r)*zeta" % (self.p, self.q)


# ---- the field constants for this lane ------------------------------------
# sqrt(5) = (2*zeta+1)/w with w = sqrt(-3/5) = 1 mod 4  (so that sqrt5 = 1 mod 2)
W = sqrt_unit(Q2.F(-3, 5))  # w^2 = -3/5,  w = 1 mod 4
INV_W = W.inv()
SQRT5 = E(INV_W, Q2.Z(2) * INV_W)  # sqrt5 = (2 zeta + 1)/w
ZETA = E(Q2.Z(0), Q2.Z(1))  # the generator; (-1 + w*sqrt5)/2 reduces to it exactly
ZETA2 = E(Q2.Z(-1), Q2.Z(-1))  # -1 - zeta
OMEGA = (0, 1)  # zeta  mod M
OMEGA2 = (1, 1)  # zeta^2 mod M


def sqrt_of_5u(u):
    """sqrt(5*m) for m = 1 mod 8 (2-adic unit).  Returns element of E."""
    m = _c(u)
    assert m.k == 0 and (m.u % 8) == 1, m
    return SQRT5 * E(sqrt_unit(m), Q2.Z(0))
