"""Shared loader + stats helpers for the Part C analysis. Pure stdlib (no pandas on this machine)."""
import csv
import os
from datetime import date, timedelta
from math import sqrt, erf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

COMPARISON_CSV = os.path.join(DATA, "bquxjob_4ff8f8f_19fa4473200.csv")   # query 13 — 9,956 subscribers
TAKERS_CSV = os.path.join(DATA, "bquxjob_19c43114_19fa424f5ce.csv")      # query 12 — 1,111 challenge takers

LAST_DATA_DATE = date(2026, 6, 25)   # max(DATE(timestamp)) in app_events — confirmed by the funnel query


def _d(s):
    return date(*map(int, s.split("-"))) if s else None


def _i(s):
    return int(s) if s not in ("", None) else 0


def _f(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def load():
    """One dict per subscriber, with the challenge-taker detail merged in."""
    takers = {}
    with open(TAKERS_CSV) as f:
        for r in csv.DictReader(f):
            takers[r["user_id"]] = r

    rows = []
    with open(COMPARISON_CSV) as f:
        for r in csv.DictReader(f):
            u = dict(r)
            for k in ("days_observed", "ch_lessons_started", "ch_lessons_completed",
                      "ch_completed_course", "ch_certificate", "ch_csat_n",
                      "lessons_completed_all", "active_days_total", "finished_onboarding",
                      "started_personal_plan", "saw_challenge_popup", "clicked_challenge_popup",
                      "viewed_any_challenge", "started_any_challenge",
                      "ret_d1", "ret_d3", "ret_d7", "fs_ret_d1", "fs_ret_d3", "fs_ret_d7",
                      "unsubscribed", "csat_n_all", "has_subscription"):
                u[k] = _i(r[k])
            u["ch_avg_csat"] = _f(r["ch_avg_csat"])
            u["avg_csat_all"] = _f(r["avg_csat_all"])
            u["first_seen"] = _d(r["first_seen"])
            u["anchor_date"] = _d(r["anchor_date"])
            u["ch_start_date"] = _d(r["ch_start_date"])

            # days observable from FIRST-SEEN (the common anchor); days_observed is from anchor_date
            u["fs_days_observed"] = (LAST_DATA_DATE - u["first_seen"]).days
            u["took"] = u["group_338"] == "took_338"
            u["days_to_challenge"] = ((u["ch_start_date"] - u["first_seen"]).days
                                      if u["ch_start_date"] else None)

            t = takers.get(r["user_id"])
            u["active_challenge_days"] = _i(t["active_challenge_days"]) if t else 0
            rows.append(u)
    return rows


# ---------------------------------------------------------------- stats
def wilson(k, n, z=1.96):
    """Wilson score interval — correct for small n and proportions near 0/1."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def _norm_cdf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def two_prop_z(k1, n1, k2, n2):
    """Two-sided z-test for a difference of proportions. Returns (diff, z, p)."""
    if n1 == 0 or n2 == 0:
        return (0.0, 0.0, 1.0)
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return (p1 - p2, 0.0, 1.0)
    z = (p1 - p2) / se
    return (p1 - p2, z, 2 * (1 - _norm_cdf(abs(z))))


def stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"


def pct(k, n):
    return f"{k/n:.1%}" if n else "—"


def rate_ci(k, n):
    p, lo, hi = wilson(k, n)
    return f"{p:.1%} [{lo:.1%}–{hi:.1%}]" if n else "—"


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None
