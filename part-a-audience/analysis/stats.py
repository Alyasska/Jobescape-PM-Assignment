#!/usr/bin/env python3
"""The few tests Part A needs, implemented directly (no scipy on this machine)."""
from math import erf, sqrt, log, exp


def wilson(k, n, z=1.96):
    """Wilson score interval — behaves at small n and near 0/1, unlike the normal approx."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def rate_ci(k, n):
    p, lo, hi = wilson(k, n)
    return f"{p:6.1%} [{lo:.1%}–{hi:.1%}]" if n else "—"


def _norm_cdf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def two_prop_z(k1, n1, k2, n2):
    """Two-proportion z-test. Returns (difference, z, two-sided p)."""
    if not n1 or not n2:
        return (0.0, 0.0, 1.0)
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return (p1 - p2, 0.0, 1.0)
    z = (p1 - p2) / se
    return (p1 - p2, z, 2 * (1 - _norm_cdf(abs(z))))


def _lower_gamma_reg(s, x):
    """Regularised lower incomplete gamma P(s, x), series expansion (good for x < s+1)."""
    if x <= 0:
        return 0.0
    total, term = 1.0 / s, 1.0 / s
    for n in range(1, 500):
        term *= x / (s + n)
        total += term
        if abs(term) < abs(total) * 1e-14:
            break
    return total * exp(-x + s * log(x) - _lgamma(s))


def _upper_gamma_reg(s, x):
    """Regularised upper incomplete gamma Q(s, x), continued fraction (good for x >= s+1)."""
    tiny = 1e-300
    b, c, d = x + 1 - s, 1 / tiny, 1 / (x + 1 - s)
    h = d
    for i in range(1, 500):
        an = -i * (i - s)
        b += 2
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-14:
            break
    return exp(-x + s * log(x) - _lgamma(s)) * h


def _lgamma(x):
    from math import lgamma
    return lgamma(x)


def chi2_sf(stat, df):
    """P(Chi2_df > stat) — the survival function, i.e. the p-value."""
    if stat <= 0 or df <= 0:
        return 1.0
    s, x = df / 2.0, stat / 2.0
    return 1.0 - _lower_gamma_reg(s, x) if x < s + 1 else _upper_gamma_reg(s, x)


def chi2_independence(table):
    """table: list of rows of counts. Returns (chi2, df, p, cramers_v)."""
    rows = len(table)
    cols = len(table[0])
    grand = sum(sum(r) for r in table)
    if grand == 0:
        return (0.0, 0, 1.0, 0.0)
    rt = [sum(r) for r in table]
    ct = [sum(table[i][j] for i in range(rows)) for j in range(cols)]
    chi2 = 0.0
    for i in range(rows):
        for j in range(cols):
            e = rt[i] * ct[j] / grand
            if e > 0:
                chi2 += (table[i][j] - e) ** 2 / e
    df = (rows - 1) * (cols - 1)
    v = sqrt(chi2 / (grand * min(rows - 1, cols - 1))) if grand and min(rows, cols) > 1 else 0.0
    return (chi2, df, chi2_sf(chi2, df), v)


def stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
