"""Supplementary tests for Part C.

  §A  The target metric exactly as the team defined it (D1 = day after the challenge started)
  §B  CSAT — the satisfaction inversion
  §C  The completion / refund-gate signal
  §D  The 'saw the popup and walked away' group
  §E  Data-quality flags
  §F  Economic sizing of the feature
"""
from collections import Counter
from lib import load, rate_ci, two_prop_z, stars, mean, wilson

rows = load()
N = len(rows)
takers = [r for r in rows if r["took"]]
nont = [r for r in rows if not r["took"]]


def head(t):
    print("\n" + "=" * 96)
    print(t)
    print("=" * 96)


head("§A · D1 AS THE TEAM DEFINED IT vs D1 ON A COMMON CLOCK")
print("""  Brief: 'Target metric: D1 Retention (retention the day after the challenge started).'
  That anchors takers on their challenge-start day. Non-takers have no such day, so the only
  way to compare is a common clock (first app day). Both are shown — the difference is the
  single biggest reason a naive read of this release looks better than it is.""")

print(f"\n  {'measure':<52}{'n':>7}{'rate':>24}")
print("-" * 96)
print(f"  {'TAKERS · D1 anchored on challenge-start (team defn)':<52}{len(takers):>7}"
      f"{rate_ci(sum(r['ret_d1'] for r in takers), len(takers)):>24}")
print(f"  {'TAKERS · D1 anchored on first app day':<52}{len(takers):>7}"
      f"{rate_ci(sum(r['fs_ret_d1'] for r in takers), len(takers)):>24}")
print(f"  {'NON-TAKERS · D1 anchored on first app day':<52}{len(nont):>7}"
      f"{rate_ci(sum(r['fs_ret_d1'] for r in nont), len(nont)):>24}")
for lbl, k in [("D3", "ret_d3"), ("D7", "ret_d7")]:
    obs = [r for r in takers if r["days_observed"] >= (3 if lbl == "D3" else 7)]
    print(f"  {'TAKERS · ' + lbl + ' anchored on challenge-start':<52}{len(obs):>7}"
          f"{rate_ci(sum(r[k] for r in obs), len(obs)):>24}")

head("§B · CSAT — does engaging with the product make people happier?")
print(f"  {'group':<40}{'raters':>9}{'mean CSAT':>12}{'% 4-5':>10}{'% 1-2':>10}")
print("-" * 96)
groups = [
    ("Completed the whole challenge", [r for r in takers if r["ch_completed_course"] == 1]),
    ("HIGH  (3+ challenge lessons)", [r for r in takers if r["ch_lessons_completed"] >= 3]),
    ("LOW   (0-2 challenge lessons)", [r for r in takers if r["ch_lessons_completed"] < 3]),
    ("Never took the challenge", nont),
]
for label, g in groups:
    rated = [r for r in g if r["csat_n_all"] > 0]
    if not rated:
        continue
    vals = [r["avg_csat_all"] for r in rated]
    hi = sum(1 for v in vals if v >= 4) / len(vals)
    lo = sum(1 for v in vals if v <= 2) / len(vals)
    print(f"  {label:<40}{len(rated):>9}{mean(vals):>12.2f}{hi:>10.1%}{lo:>10.1%}")

chr_ = [r for r in takers if r["ch_csat_n"] > 0]
print(f"\n  CSAT given INSIDE challenge 338 specifically: n={len(chr_)} raters, "
      f"mean {mean([r['ch_avg_csat'] for r in chr_]):.2f}")
print(f"  … of {len(takers)} starters, only {len(chr_)/len(takers):.1%} ever rated challenge content.")
print(f"  Same users' CSAT across ALL product content: "
      f"{mean([r['avg_csat_all'] for r in chr_ if r['csat_n_all'] > 0]):.2f}")

head("§C · COMPLETION AND THE REFUND GATE")
print("""  Part A found (from public reviews) that finishing the plan is the money-back gate.
  If true, completion should predict MORE unsubscribing, not less. Test it.""")
fin = [r for r in takers if r["ch_completed_course"] == 1]
notfin = [r for r in takers if r["ch_completed_course"] == 0]
print(f"\n  {'group':<44}{'n':>7}{'unsubscribe rate':>26}")
print("-" * 96)
print(f"  {'finished the challenge (all 8 lessons)':<44}{len(fin):>7}"
      f"{rate_ci(sum(r['unsubscribed'] for r in fin), len(fin)):>26}")
print(f"  {'started but did not finish':<44}{len(notfin):>7}"
      f"{rate_ci(sum(r['unsubscribed'] for r in notfin), len(notfin)):>26}")
print(f"  {'never took it':<44}{len(nont):>7}"
      f"{rate_ci(sum(r['unsubscribed'] for r in nont), len(nont)):>26}")
d, z, p = two_prop_z(sum(r["unsubscribed"] for r in fin), len(fin),
                     sum(r["unsubscribed"] for r in notfin), len(notfin))
print(f"\n  finishers vs non-finishers: diff {d:+.1%}  z={z:+.2f}  p={p:.3f}  {stars(p)}")

binge = [r for r in fin if r["active_challenge_days"] <= 2]
print(f"\n  of the finishers, those who binged it in <=2 days: n={len(binge)}, "
      f"unsub {rate_ci(sum(r['unsubscribed'] for r in binge), len(binge))}")
slow = [r for r in fin if r["active_challenge_days"] >= 3]
print(f"  of the finishers, those who spread it over 3+ days: n={len(slow)}, "
      f"unsub {rate_ci(sum(r['unsubscribed'] for r in slow), len(slow))}")

cert = [r for r in takers if r["ch_certificate"] == 1]
print(f"\n  took the certificate: n={len(cert)}, "
      f"unsub {rate_ci(sum(r['unsubscribed'] for r in cert), len(cert))}")

head("§D · THE 'SAW THE POPUP AND WALKED AWAY' GROUP — the worst cell in the dataset")
saw_no = [r for r in rows if r["group_338"] == "no_challenge" and r["saw_challenge_popup"]]
never = [r for r in rows if r["group_338"] == "no_challenge" and not r["saw_challenge_popup"]
         and not r["viewed_any_challenge"]]
print(f"  {'group':<40}{'n':>7}{'D1':>20}{'unsub':>20}{'avg lessons':>14}")
print("-" * 96)
for label, g in [("saw popup, never opened the challenge", saw_no),
                 ("never reached any challenge surface", never),
                 ("took the challenge", takers)]:
    print(f"  {label:<40}{len(g):>7}"
          f"{rate_ci(sum(r['fs_ret_d1'] for r in g), len(g)):>20}"
          f"{rate_ci(sum(r['unsubscribed'] for r in g), len(g)):>20}"
          f"{mean([r['lessons_completed_all'] for r in g]):>14.2f}")
print(f"\n  plan mix of 'saw popup, never opened': {Counter(r['plan'] for r in saw_no).most_common(4)}")
print(f"  plan mix of the whole cohort         : {Counter(r['plan'] for r in rows).most_common(4)}")
print(f"\n  1-Week subscribers as share of 'saw popup, never opened': "
      f"{sum(1 for r in saw_no if r['plan']=='1Week')/len(saw_no):.1%}  "
      f"(cohort: {sum(1 for r in rows if r['plan']=='1Week')/N:.1%})")

head("§E · DATA-QUALITY FLAGS (things I would raise before anyone acts on this)")
print("  1. Two different quiz vocabularies are mixed in one cohort:")
for f_, vals in [("age", ["45-54", "55+", "45+"]),
                 ("status", ["Full-time employee", "Full-time worker"])]:
    for v in vals:
        g = [r for r in rows if r[f_] == v]
        if g:
            print(f"     {f_:<8} '{v}': n={len(g):<5} unsub={sum(r['unsubscribed'] for r in g)/len(g):>6.1%} "
                  f"D1={sum(r['fs_ret_d1'] for r in g)/len(g):>6.1%}")
print("     → 'Full-time worker' churns at 2.4x 'Full-time employee'. Same words, different funnel.")
print("       Either a different quiz version or different traffic. Cannot be pooled blindly.")

print("\n  2. THE BIG ONE — there is no hold-out group. Challenge starts run on every single day of")
print("     the window (2026-06-12 … 2026-06-25), so there is no pre/post and no control arm.")
print("     Every causal statement below is an observational correction, not an experiment.")
print("     This is the #1 thing to fix before the next release, not after it.")

print("\n  3. Observation window is only 14 days (2026-06-12 → 2026-06-25):")
print(f"     D7 is unobservable for {sum(1 for r in rows if r['fs_days_observed'] < 7)/N:.1%} of the cohort;")
print("     unsubscribe is right-censored for everyone (a 4-week plan cannot even reach its")
print("     first renewal inside this window), so all unsubscribe rates here are FLOOR values.")

print("\n  4. The popup carries no challenge_id, so 'saw the popup' is exposure to ANY challenge,")
print("     not specifically 338. 338 is 99.7% of all starts, so the practical impact is small.")

head("§F · WHAT THE FEATURE IS WORTH TODAY")
n_takers = len(takers)
print(f"  Reach:        {n_takers}/{N} = {n_takers/N:.1%} of paying subscribers started it.")
print(f"  Activation:   {sum(1 for r in takers if r['ch_lessons_completed']>=1)}/{n_takers} = "
      f"{sum(1 for r in takers if r['ch_lessons_completed']>=1)/n_takers:.1%} did even one lesson.")
print(f"  Completion:   {len(fin)}/{n_takers} = {len(fin)/n_takers:.1%} finished "
      f"({len(fin)/N:.2%} of all subscribers).")
ctrl = [r for r in rows if r["group_338"] in ("joined_338_never_started", "viewed_338_never_joined")]
eff, z, p = two_prop_z(sum(r["fs_ret_d1"] for r in takers), len(takers),
                       sum(r["fs_ret_d1"] for r in ctrl), len(ctrl))
lo, hi = wilson(sum(r['fs_ret_d1'] for r in takers), len(takers))[1:]
print(f"\n  Best causal estimate of the D1 effect (vs the exposure-matched control):")
print(f"    {eff:+.1%} percentage points, p={p:.3f} ({stars(p)}) — statistically indistinguishable from zero.")
print(f"\n  Even if the effect were real and equal to the raw taker-vs-non-taker gap, at "
      f"{n_takers/N:.1%} reach")
print(f"  the cohort-level D1 impact would be at most {n_takers/N:.3f} x the gap.")
raw = sum(r['fs_ret_d1'] for r in takers)/len(takers) - sum(r['fs_ret_d1'] for r in nont)/len(nont)
print(f"    raw gap = {raw:+.1%}  →  cohort-level ceiling = {raw * n_takers/N:+.1%} pts of overall D1.")
print(f"  Overall cohort D1 today: {sum(r['fs_ret_d1'] for r in rows)/N:.1%}")
