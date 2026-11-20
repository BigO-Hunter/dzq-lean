"""Hilbert symbols over Q and the ramification set of a quaternion algebra.

(a,b)_v for v = odd prime p, v = 2, v = infinity.  Conventions as in Serre, Local Fields III.1.
Control arm: (5,2) must ramify at exactly {2,5} (the constant choice of the derivation lane for
p = 2), and (a,b)_v = 1 whenever a or b is a square at v.
"""
from fractions import Fraction as Fr


def _vp(n, p):
    """(valuation, unit) of a non-zero integer at p."""
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v, n


def _leg(a, p):
    """Legendre symbol of an integer a not divisible by p (p an odd prime)."""
    a %= p
    if a == 0:
        raise ValueError("leg with p | a")
    ls = pow(a, (p - 1) // 2, p)
    return 1 if ls == 1 else -1


def hilbert(a, b, place):
    """(a,b)_place for non-zero rationals a,b; place is 2, an odd prime, or 'inf'."""
    a, b = Fr(a), Fr(b)
    if a == 0 or b == 0:
        return 1
    if place == "inf":
        return -1 if (a < 0 and b < 0) else 1
    p = place
    if p == 2:
        # write a = 2^al * u, b = 2^be * v with u,v odd integers
        def parts(x):
            s = -1 if x < 0 else 1
            x = abs(x)
            num, den = x.numerator, x.denominator
            vn, un = _vp(num, 2)
            vd, ud = _vp(den, 2)
            return vn - vd, s * un * pow(ud, -1, 1 << 8)
        al, u = parts(a)
        be, v = parts(b)
        eu = (u - 1) // 2 % 2
        ev = (v - 1) // 2 % 2
        ou = ((u * u - 1) // 8) % 2
        ov = ((v * v - 1) // 8) % 2
        return -1 if (eu * ev + al * ov + be * ou) % 2 else 1
    # odd prime
    num_a, den_a = a.numerator, a.denominator
    num_b, den_b = b.numerator, b.denominator
    va1, ua1 = _vp(abs(num_a), p)
    va2, ua2 = _vp(den_a, p)
    vb1, ub1 = _vp(abs(num_b), p)
    vb2, ub2 = _vp(den_b, p)
    al = va1 - va2
    be = vb1 - vb2
    ua = (-1 if num_a < 0 else 1) * ua1 * pow(ua2, -1, p)
    ub = (-1 if num_b < 0 else 1) * ub1 * pow(ub2, -1, p)
    s = 1
    if (al * be * (p - 1) // 2) % 2:
        s = -s
    if be % 2 and _leg(ua, p) == -1:
        s = -s
    if al % 2 and _leg(ub, p) == -1:
        s = -s
    return s


def ramified_primes(A, B):
    """Delta of the quaternion algebra (A,B) over Q: the places where (A,B)_v = -1."""
    cands = {2, "inf"}
    for x in (A, B):
        x = Fr(x)
        for n in (x.numerator, x.denominator):
            n = abs(n)
            d = 2
            while d * d <= n:
                while n % d == 0:
                    cands.add(d)
                    n //= d
                d += 1
            if n > 1:
                cands.add(n)
    return frozenset(v for v in cands if hilbert(A, B, v) == -1)


def is_square_at(x, place):
    """is the non-zero rational x a square in Q_place?"""
    x = Fr(x)
    if place == "inf":
        return x > 0
    if place == 2:
        vn, un = _vp(abs(x.numerator), 2)
        vd, ud = _vp(x.denominator, 2)
        v = vn - vd
        if v % 2:
            return False
        u = (-1 if x < 0 else 1) * un * pow(ud, -1, 8)
        return u % 8 == 1
    p = place
    vn, un = _vp(abs(x.numerator), p)
    vd, ud = _vp(x.denominator, p)
    if (vn - vd) % 2:
        return False
    u = (-1 if x < 0 else 1) * un * pow(ud, -1, p)
    return _leg(u, p) == 1


def squarefree_part(n):
    n = abs(int(n))
    out = 1
    d = 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e % 2:
            out *= d
        d += 1
    if n > 1:
        out *= n
    return out


def selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + name)
        ok = ok and cond

    chk("(5,2) ramifies at {2,5}", ramified_primes(5, 2) == frozenset({2, 5}))
    # [A,B) in the char-independent notation IS (1+4A, B) in char != 2
    chk("[1,2) == (5,2): ramifies at {2,5}", ramified_primes(1 + 4 * 1, 2) == frozenset({2, 5}))
    chk("(1,2) alone is split (A=1 is a square)", ramified_primes(1, 2) == frozenset())
    chk("(-1,-1) ramifies at {2,inf}", ramified_primes(-1, -1) == frozenset({2, "inf"}))
    chk("(2,3) splits somewhere even? |Delta| even", len(ramified_primes(2, 3)) % 2 == 0)
    chk("(a,b) with a a square is split", ramified_primes(9, 5) == frozenset())
    chk("(5,2)_2 = -1", hilbert(5, 2, 2) == -1)
    chk("(5,2)_5 = -1", hilbert(5, 2, 5) == -1)
    chk("(5,2)_inf = +1", hilbert(5, 2, "inf") == 1)
    chk("(5,2)_3 = +1", hilbert(5, 2, 3) == 1)
    chk("33 square at 2?", is_square_at(33, 2) is True)      # 33 = 1 mod 8
    chk("33 nonsquare at 5", is_square_at(33, 5) is False)   # 33 = 3 mod 5
    chk("5 square at 2? no", is_square_at(5, 2) is False)
    chk("4*1/9 square everywhere", is_square_at(Fr(4, 9), 2) and is_square_at(Fr(4, 9), 7))
    chk("sf(2/165) parts", squarefree_part(2 * 165) == 2 * 3 * 5 * 11)
    print("hilbert selftest:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
