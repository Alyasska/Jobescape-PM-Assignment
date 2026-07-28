#!/usr/bin/env python3
"""k-modes clustering for purely categorical data, plus the validity machinery.

Why k-modes and not k-means: every feature here is an unordered category (goal,
work status, gender). One-hot + Euclidean would impose a fake geometry — the
distance between "Freelancer" and "Student" would depend on how many categories
happen to exist. k-modes (Huang 1998) uses Hamming distance and modal centroids,
which is the honest metric for this data.

Nothing here is imported from a package: this machine has no numpy or sklearn,
so the algorithm, the silhouette, the Adjusted Rand Index and the null model are
all implemented directly.
"""
import random
from collections import Counter


# ─────────────────────────────── distance ───────────────────────────────

def hamming(a, b):
    """Number of attributes on which two records disagree."""
    return sum(1 for x, y in zip(a, b) if x != y)


# ─────────────────────────────── the algorithm ───────────────────────────────

def _init_modes(rows, k, rng):
    """Huang-style init: seed from the most frequent categories, then spread out.

    Picking k rows at random tends to seed two modes inside the same dense region.
    Instead: pick the first centre at random, then each subsequent centre is the
    row furthest (in Hamming terms) from the centres chosen so far — a categorical
    analogue of k-means++ that is deterministic given the seed.
    """
    modes = [list(rng.choice(rows))]
    while len(modes) < k:
        best, best_d = None, -1
        # sample for speed; exact furthest-point search is O(n*k) per centre
        for r in rng.sample(rows, min(len(rows), 2000)):
            d = min(hamming(r, m) for m in modes)
            if d > best_d:
                best, best_d = r, d
        modes.append(list(best))
    return modes


def _update_mode(members, n_attr):
    """The mode of a cluster is the per-attribute most common value."""
    out = []
    for j in range(n_attr):
        c = Counter(m[j] for m in members)
        out.append(c.most_common(1)[0][0])
    return out


def kmodes(rows, k, rng, max_iter=100):
    """Returns (labels, modes, cost). Cost = total Hamming distance to own mode."""
    n_attr = len(rows[0])
    modes = _init_modes(rows, k, rng)
    labels = [0] * len(rows)

    for _ in range(max_iter):
        moved = False
        for i, r in enumerate(rows):
            best, best_d = 0, None
            for c, m in enumerate(modes):
                d = hamming(r, m)
                if best_d is None or d < best_d:
                    best, best_d = c, d
            if labels[i] != best:
                labels[i] = best
                moved = True

        for c in range(k):
            members = [rows[i] for i, l in enumerate(labels) if l == c]
            if members:
                modes[c] = _update_mode(members, n_attr)
            else:
                modes[c] = list(rng.choice(rows))   # revive an empty cluster
                moved = True

        if not moved:
            break

    cost = sum(hamming(r, modes[labels[i]]) for i, r in enumerate(rows))
    return labels, modes, cost


def best_of(rows, k, restarts, seed):
    """Run k-modes several times and keep the lowest-cost solution."""
    best = None
    for s in range(restarts):
        rng = random.Random(seed * 1000 + s)
        labels, modes, cost = kmodes(rows, k, rng)
        if best is None or cost < best[2]:
            best = (labels, modes, cost)
    return best


# ─────────────────────────────── validity ───────────────────────────────

def silhouette(rows, labels, sample, rng):
    """Mean silhouette width on a random sample (full computation is O(n^2)).

    s = (b - a) / max(a, b) where a is the mean distance to one's own cluster and
    b the mean distance to the nearest other cluster. Near 0 means the clusters
    overlap; the data is one blob, not several groups.
    """
    idx = rng.sample(range(len(rows)), min(sample, len(rows)))
    by_c = {}
    for i, l in enumerate(labels):
        by_c.setdefault(l, []).append(rows[i])
    if len(by_c) < 2:
        return 0.0

    total, n = 0.0, 0
    for i in idx:
        own = labels[i]
        r = rows[i]
        a, b = None, None
        for c, members in by_c.items():
            pool = members if len(members) <= 400 else rng.sample(members, 400)
            if not pool:
                continue
            d = sum(hamming(r, m) for m in pool) / len(pool)
            if c == own:
                a = d
            elif b is None or d < b:
                b = d
        if a is None or b is None:
            continue
        denom = max(a, b)
        if denom > 0:
            total += (b - a) / denom
            n += 1
    return total / n if n else 0.0


def adjusted_rand(a, b):
    """Agreement between two labellings, corrected for chance. 0 = chance, 1 = identical."""
    pairs = Counter(zip(a, b))
    ra = Counter(a)
    rb = Counter(b)
    c2 = lambda x: x * (x - 1) / 2
    sij = sum(c2(v) for v in pairs.values())
    sa = sum(c2(v) for v in ra.values())
    sb = sum(c2(v) for v in rb.values())
    n = c2(len(a))
    exp = sa * sb / n if n else 0
    mx = (sa + sb) / 2
    return (sij - exp) / (mx - exp) if mx != exp else 0.0


def permute_null(rows, rng):
    """Shuffle every column independently.

    This destroys all association *between* variables while preserving each
    variable's marginal distribution exactly. Any clustering of the result is
    structure the algorithm manufactured, not structure the data contains — so it
    is the right yardstick for 'are these clusters real?'.
    """
    cols = list(zip(*rows))
    out = []
    for col in cols:
        c = list(col)
        rng.shuffle(c)
        out.append(c)
    return [list(r) for r in zip(*out)]
