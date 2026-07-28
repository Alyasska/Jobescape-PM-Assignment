"""Loose ends: confound checks + cohort-level baselines quoted in the writeup."""
from collections import Counter
from lib import load, rate_ci, mean, two_prop_z, stars

rows = load()
N = len(rows)
takers = [r for r in rows if r["took"]]

print("== cohort-level baselines (all 9,956 paying subscribers, first-app-day anchor) ==")
for lbl, k, need in [("D1", "fs_ret_d1", 1), ("D3", "fs_ret_d3", 3), ("D7", "fs_ret_d7", 7)]:
    g = [r for r in rows if r["fs_days_observed"] >= need]
    print(f"  {lbl}: {rate_ci(sum(r[k] for r in g), len(g))}   (n={len(g)})")
print(f"  unsubscribed within the 14-day window: {rate_ci(sum(r['unsubscribed'] for r in rows), N)}")
print(f"  mean lessons completed (any course): {mean([r['lessons_completed_all'] for r in rows]):.2f}")
print(f"  mean active days in product: {mean([r['active_days_total'] for r in rows]):.2f}")
print(f"  never completed a single lesson anywhere: "
      f"{sum(1 for r in rows if r['lessons_completed_all'] == 0)/N:.1%}")
print(f"  finished onboarding: {sum(r['finished_onboarding'] for r in rows)/N:.1%}")

print("\n== CONFOUND CHECK for §D: is 'saw the popup' just a proxy for time-in-product? ==")
grp = [
    ("took 338", [r for r in rows if r["took"]]),
    ("saw popup, never opened", [r for r in rows if r["group_338"] == "no_challenge" and r["saw_challenge_popup"]]),
    ("never reached a surface", [r for r in rows if r["group_338"] == "no_challenge"
                                 and not r["saw_challenge_popup"] and not r["viewed_any_challenge"]]),
]
print(f"  {'group':<28}{'n':>7}{'mean active days':>18}{'mean days observed':>20}{'unsub':>10}")
for lbl, g in grp:
    print(f"  {lbl:<28}{len(g):>7}{mean([r['active_days_total'] for r in g]):>18.2f}"
          f"{mean([r['fs_days_observed'] for r in g]):>20.2f}"
          f"{sum(r['unsubscribed'] for r in g)/len(g):>10.1%}")

print("\n  Same three groups, holding ACTIVE DAYS roughly constant (users with 3-6 active days):")
print(f"  {'group':<28}{'n':>7}{'D1':>20}{'unsub':>20}")
for lbl, g in grp:
    s = [r for r in g if 3 <= r["active_days_total"] <= 6]
    if len(s) < 30:
        print(f"  {lbl:<28}{len(s):>7}{'(too few)':>20}")
        continue
    print(f"  {lbl:<28}{len(s):>7}{rate_ci(sum(r['fs_ret_d1'] for r in s), len(s)):>20}"
          f"{rate_ci(sum(r['unsubscribed'] for r in s), len(s)):>20}")

print("\n== TAKERS vs EXPOSED-CONTROL, holding active days constant (the tightest test I can run) ==")
ctrl = [r for r in rows if r["group_338"] in ("joined_338_never_started", "viewed_338_never_joined")]
print(f"  {'active days':<14}{'n takers':>10}{'D1 takers':>14}{'n control':>11}{'D1 control':>14}{'diff':>9}{'p':>9}")
for lo, hi, lbl in [(1, 1, "1"), (2, 2, "2"), (3, 4, "3-4"), (5, 7, "5-7"), (8, 99, "8+")]:
    t = [r for r in takers if lo <= r["active_days_total"] <= hi]
    c = [r for r in ctrl if lo <= r["active_days_total"] <= hi]
    if len(t) < 20 or len(c) < 20:
        continue
    kt, kc = sum(r["fs_ret_d1"] for r in t), sum(r["fs_ret_d1"] for r in c)
    d, z, p = two_prop_z(kt, len(t), kc, len(c))
    print(f"  {lbl:<14}{len(t):>10}{kt/len(t):>14.1%}{len(c):>11}{kc/len(c):>14.1%}{d:>+9.1%}{p:>9.3f}")

print("\n== was the Challenge live for the whole observation window? ==")
cs = Counter(r["ch_start_date"] for r in takers if r["ch_start_date"])
for d in sorted(cs):
    print(f"  {d}: {cs[d]:>4} starts")

print("\n== plan mix: real cohort vs the plans.csv assumption used in Part D ==")
real = Counter(r["plan"] for r in rows)
tot4 = real["4Week"] + real["4Week_special"]
print(f"  1Week : {real['1Week']/N:>6.1%}   (plans.csv assumes 10%)")
print(f"  4Week : {tot4/N:>6.1%}   (plans.csv assumes 70%)")
print(f"  12Week: {real['12Week']/N:>6.1%}   (plans.csv assumes 20%)")
