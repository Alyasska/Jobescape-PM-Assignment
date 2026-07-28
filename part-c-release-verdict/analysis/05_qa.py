"""QA: re-derive every load-bearing number in the write-ups straight from the CSVs and assert it.

If a number in the markdown ever drifts from the data, this fails loudly.
Run:  python3 05_qa.py
"""
import csv
import os
from collections import Counter
from lib import load, wilson, two_prop_z, DATA

rows = load()
N = len(rows)
takers = [r for r in rows if r["took"]]
nont = [r for r in rows if not r["took"]]
fails, checks = [], 0


def check(label, actual, expected, tol=0.0005):
    # NB tolerances are deliberately tight: a 0.001 tolerance once hid a 59.557 -> '59.5%' mis-rounding.
    """expected may be an int/float; tol is absolute."""
    global checks
    checks += 1
    ok = abs(actual - expected) <= tol
    if not ok:
        fails.append(f"{label}: computed {actual!r}, document says {expected!r}")
    print(f"  {'ok ' if ok else 'FAIL'} {label:<58} {actual:.4f}  (doc: {expected})")


def rate(g, k):
    return sum(r[k] for r in g) / len(g)


print("== cohort shape ==")
check("subscribers in cohort", N, 9956, 0)
check("challenge-338 starters", len(takers), 1111, 0)
check("non-takers", len(nont), 8845, 0)
check("all rows have a subscription", sum(r["has_subscription"] for r in rows), 9956, 0)

print("\n== exposure ladder (Part C §1) ==")
check("saw popup", sum(r["saw_challenge_popup"] for r in rows), 3140, 0)
check("saw popup %", sum(r["saw_challenge_popup"] for r in rows) / N, 0.315, 0.0005)
check("clicked popup", sum(r["clicked_challenge_popup"] for r in rows), 2970, 0)
check("viewed a challenge", sum(r["viewed_any_challenge"] for r in rows), 2109, 0)
check("started 338 %", len(takers) / N, 0.112, 0.0005)
check("never reached a surface",
      sum(1 for r in rows if not r["saw_challenge_popup"] and not r["viewed_any_challenge"]), 6716, 0)
check("never reached a surface %",
      sum(1 for r in rows if not r["saw_challenge_popup"] and not r["viewed_any_challenge"]) / N, 0.675, 0.0005)

print("\n== inside the challenge (Part C §2) ==")
for k, exp in [(1, 612), (2, 308), (3, 158), (8, 47)]:
    check(f"completed >= {k} lessons", sum(1 for r in takers if r["ch_lessons_completed"] >= k), exp, 0)
check("zero lessons %", sum(1 for r in takers if r["ch_lessons_completed"] == 0) / len(takers), 0.449, 0.0005)
check("lesson1->2 survival", 308 / 612, 0.503, 0.001)
check("completed the course", sum(r["ch_completed_course"] for r in takers), 48, 0)
check("certificate", sum(r["ch_certificate"] for r in takers), 23, 0)

print("\n== tiers + headline table (Part C §4) ==")
high = [r for r in takers if r["ch_lessons_completed"] >= 3]
low = [r for r in takers if r["ch_lessons_completed"] < 3]
check("HIGH n", len(high), 158, 0)
check("LOW n", len(low), 953, 0)
check("HIGH D1", rate(high, "fs_ret_d1"), 0.696, 0.001)
check("LOW D1", rate(low, "fs_ret_d1"), 0.584, 0.001)
check("DIDNT-TAKE D1", rate(nont, "fs_ret_d1"), 0.217, 0.001)
check("HIGH D3", rate(high, "fs_ret_d3"), 0.570, 0.001)
check("LOW D3", rate(low, "fs_ret_d3"), 0.344, 0.001)
check("DIDNT-TAKE D3", rate(nont, "fs_ret_d3"), 0.100, 0.001)
for label, g, exp, expn in [("HIGH", high, 0.391, 133), ("LOW", low, 0.180, 737), ("DIDNT-TAKE", nont, 0.069, 6345)]:
    obs = [r for r in g if r["fs_days_observed"] >= 7]
    check(f"{label} D7", rate(obs, "fs_ret_d7"), exp, 0.001)
    check(f"{label} D7 denominator", len(obs), expn, 0)
check("HIGH unsub", rate(high, "unsubscribed"), 0.114, 0.001)
check("LOW unsub", rate(low, "unsubscribed"), 0.114, 0.001)
check("DIDNT-TAKE unsub", rate(nont, "unsubscribed"), 0.143, 0.001)

print("\n== the decisive test (Part C §5 Test A) ==")
ctrl = [r for r in rows if r["group_338"] in ("joined_338_never_started", "viewed_338_never_joined")]
check("takers D1", rate(takers, "fs_ret_d1"), 0.600, 0.001)
check("control n", len(ctrl), 994, 0)
check("control D1 (the 59.6%)", rate(ctrl, "fs_ret_d1"), 0.596, 0.0005)
d, z, p = two_prop_z(sum(r["fs_ret_d1"] for r in takers), len(takers),
                     sum(r["fs_ret_d1"] for r in ctrl), len(ctrl))
check("D1 effect (pts)", d, 0.005, 0.001)
check("D1 effect p-value", p, 0.823, 0.005)
d2, _, p2 = two_prop_z(sum(r["unsubscribed"] for r in takers), len(takers),
                       sum(r["unsubscribed"] for r in ctrl), len(ctrl))
check("unsub effect (pts)", d2, -0.023, 0.001)
check("unsub effect p-value", p2, 0.119, 0.005)
check("joined-never-started D1", rate([r for r in rows if r["group_338"] == "joined_338_never_started"], "fs_ret_d1"), 0.604, 0.001)
check("viewed-never-joined D1", rate([r for r in rows if r["group_338"] == "viewed_338_never_joined"], "fs_ret_d1"), 0.593, 0.001)

print("\n== immortal time + dose-response (Test B / C) ==")
lag = Counter(r["days_to_challenge"] for r in takers)
check("start on day 0 %", lag[0] / len(takers), 0.239, 0.001)
oneday = [r for r in takers if r["active_challenge_days"] == 1]
hi = [r for r in oneday if r["ch_lessons_completed"] >= 2]
lo = [r for r in oneday if r["ch_lessons_completed"] <= 1]
d3, _, p3 = two_prop_z(sum(r["fs_ret_d1"] for r in hi), len(hi),
                       sum(r["fs_ret_d1"] for r in lo), len(lo))
check("day-0 dose effect (pts, negative)", d3, -0.092, 0.001)
check("day-0 dose p-value", p3, 0.048, 0.002)

print("\n== the mechanic (Test D) ==")
fin = [r for r in takers if r["ch_completed_course"] == 1]
check("finished in 1 day", sum(1 for r in fin if r["active_challenge_days"] == 1), 13, 0)
check("finished in 1 day %", sum(1 for r in fin if r["active_challenge_days"] == 1) / len(fin), 0.271, 0.001)
check("finished in <=2 days %", sum(1 for r in fin if r["active_challenge_days"] <= 2) / len(fin), 0.458, 0.001)
did = [r for r in takers if r["ch_lessons_completed"] >= 1]
check("returned for a 2nd challenge day %",
      sum(1 for r in did if r["active_challenge_days"] >= 2) / len(did), 0.368, 0.001)
check("mean lessons per active challenge day",
      sum(r["ch_lessons_completed"] / max(1, r["active_challenge_days"]) for r in did) / len(did), 1.46, 0.005)

print("\n== the metric that would have fooled the team (§6) ==")
check("takers D1, challenge-anchored", rate(takers, "ret_d1"), 0.398, 0.001)
check("cohort D1, first-app-day", rate([r for r in rows if r["fs_days_observed"] >= 1], "fs_ret_d1"), 0.260, 0.001)

print("\n== CSAT inversion (§8) ==")


def csat(g):
    v = [r["avg_csat_all"] for r in g if r["csat_n_all"] > 0]
    return sum(v) / len(v), len(v)


for label, g, exp in [("never took", nont, 3.74), ("LOW", low, 3.53), ("HIGH", high, 3.33), ("finishers", fin, 3.10)]:
    m, n = csat(g)
    check(f"CSAT {label}", m, exp, 0.005)
chr_ = [r for r in takers if r["ch_csat_n"] > 0]
check("CSAT of challenge-338 content", sum(r["ch_avg_csat"] for r in chr_) / len(chr_), 3.25, 0.005)
check("same users, all content", sum(r["avg_csat_all"] for r in chr_ if r["csat_n_all"] > 0) /
      len([r for r in chr_ if r["csat_n_all"] > 0]), 3.45, 0.005)

print("\n== product-wide baselines (the thesis number) ==")
check("never completed a lesson anywhere %",
      sum(1 for r in rows if r["lessons_completed_all"] == 0) / N, 0.502, 0.001)
check("cohort unsubscribe %", rate(rows, "unsubscribed"), 0.140, 0.001)

print("\n== demographics (Part A + the PM's claim) ==")
check("male %", sum(1 for r in rows if r["gender"] == "Male") / N, 0.597, 0.001)
check("female %", sum(1 for r in rows if r["gender"] == "Female") / N, 0.384, 0.001)
check("aged 45+ (clean buckets) %", sum(1 for r in rows if r["age"] in ("45-54", "55+")) / N, 0.578, 0.001)
check("aged 45+ incl. legacy bucket %",
      sum(1 for r in rows if r["age"] in ("45-54", "55+", "45+")) / N, 0.601, 0.001)
check("men 55+ count", sum(1 for r in rows if r["gender"] == "Male" and r["age"] == "55+"), 2120, 0)
check("men 55+ %", sum(1 for r in rows if r["gender"] == "Male" and r["age"] == "55+") / N, 0.213, 0.001)
check("men 35-54 %", sum(1 for r in rows if r["gender"] == "Male" and r["age"] in ("35-44", "45-54")) / N, 0.249, 0.001)
for a, exp in [("18-24", 0.311), ("25-34", 0.197), ("35-44", 0.145), ("45-54", 0.095), ("55+", 0.097)]:
    check(f"unsub, age {a}", rate([r for r in rows if r["age"] == a], "unsubscribed"), exp, 0.001)
for gl, exp in [("Work faster", 0.109), ("Feel more confident with AI", 0.107), ("Get a quick side hustle", 0.372)]:
    check(f"unsub, goal '{gl}'", rate([r for r in rows if r["goal"] == gl], "unsubscribed"), exp, 0.001)

print("\n== plans (Part D validation) ==")
pc = Counter(r["plan"] for r in rows)
check("1Week share", pc["1Week"] / N, 0.102, 0.001)
check("4Week share incl. special", (pc["4Week"] + pc["4Week_special"]) / N, 0.646, 0.001)
check("12Week share", pc["12Week"] / N, 0.251, 0.001)
check("1Week unsub", rate([r for r in rows if r["plan"] == "1Week"], "unsubscribed"), 0.346, 0.001)
check("4Week unsub", rate([r for r in rows if r["plan"] == "4Week"], "unsubscribed"), 0.122, 0.001)
check("12Week unsub", rate([r for r in rows if r["plan"] == "12Week"], "unsubscribed"), 0.106, 0.001)
blended = (0.102 * 60.42 + 0.646 * 123.70 + 0.251 * 162.15) / 0.999
check("observed-mix blended net LTV", blended, 126.90, 0.02)

print("\n== unsubscribe reasons (§8) ==")
uns = [r for r in rows if r["unsubscribed"]]
check("total unsubscribed", len(uns), 1393, 0)
invol = {"hard_decline", "Mastercard Alert", "dispute", "paypal_refund", "Visa CDRN",
         "fraud", "Merchanto visa", "payment_refunded", "fraud_reported"}
ni = sum(1 for r in uns if r["unsub_reason"] in invol)
check("payment/chargeback/dispute unsubs", ni, 157, 0)
check("… as % of unsubs", ni / len(uns), 0.113, 0.001)

print("\n== event catalogue (the 'not observable here' claim) ==")
# The verdict rests on primary metrics being uncomputable from this dataset. That is a claim
# about the event catalogue, not about the user table, so it needs its own check or it would
# be the one published number nothing re-derives.
CAT = os.path.join(DATA, "script_job_ee3720964a3e4c3ac51fe64306b65890_0.csv")
cat = {r["event_name"]: int(r["n"]) for r in csv.DictReader(open(CAT))}
check("event catalogue rows (file integrity)", len(cat), 67, 0)
check("subscription_renewed events", cat.get("pr_webapp_subscription_renewed", 0), 17, 0)
check("… per subscriber", cat.get("pr_webapp_subscription_renewed", 0) / N, 0.0017, 0.0001)

print("\n" + "=" * 70)
if fails:
    print(f"{len(fails)} of {checks} CHECKS FAILED:")
    for f in fails:
        print("   -", f)
    raise SystemExit(1)
print(f"All {checks} checks passed — every documented number matches the data.")
