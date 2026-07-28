"""Diagnostics that must be settled BEFORE choosing the engagement-tier cut.

Questions:
  Q1  When do takers start the challenge relative to first_seen? (does the anchor choice matter?)
  Q2  What does the lesson-completion histogram really look like? (the >7 spike)
  Q3  Where does the retention curve actually break by lesson count? (let the data pick the cut)
  Q4  How much observation window do we have? (D7 censoring)
  Q5  Is challenge 338 == "the Challenge feature"? (coverage check)
"""
from collections import Counter, defaultdict
from lib import load, rate_ci, wilson, LAST_DATA_DATE

rows = load()
takers = [r for r in rows if r["took"]]
print(f"subscribers: {len(rows)}   ·   challenge-338 takers: {len(takers)}")

# ---------------------------------------------------------------- Q1
print("\n" + "=" * 78)
print("Q1 · lag between first app day and challenge start (days)")
print("=" * 78)
lag = Counter(r["days_to_challenge"] for r in takers)
cum = 0
for k in sorted(lag):
    cum += lag[k]
    print(f"  +{k:2d} days: {lag[k]:5d}  ({lag[k]/len(takers):6.1%})  cum {cum/len(takers):6.1%}")
same = lag.get(0, 0)
med = sorted(r["days_to_challenge"] for r in takers)[len(takers) // 2]
print(f"\n  → Only {same/len(takers):.1%} of takers start the challenge on their FIRST app day;")
print(f"    the median taker starts on day +{med}, and "
      f"{sum(v for k,v in lag.items() if k>=3)/len(takers):.0%} start on day +3 or later.")
print("    CONSEQUENCE: the two anchors are NOT interchangeable, and takers are pre-selected")
print("    survivors — to start on day k you must have survived to day k (immortal-time bias).")
print("    So: use the first-seen anchor for all cross-group comparisons, and treat even that")
print("    as favourable to takers. See 02_main.py §4 Test B.")

# ---------------------------------------------------------------- Q2
print("\n" + "=" * 78)
print("Q2 · challenge lessons STARTED vs COMPLETED (the >7 spike)")
print("=" * 78)
print("  completed:", dict(sorted(Counter(r['ch_lessons_completed'] for r in takers).items())))
print("  started:  ", dict(sorted(Counter(r['ch_lessons_started'] for r in takers).items())))
gt7 = [r for r in takers if r["ch_lessons_completed"] > 7]
print(f"\n  users with >7 completions: {len(gt7)}")
if gt7:
    print("  their completed-course flag:", Counter(r["ch_completed_course"] for r in gt7))
    print("  their certificate flag:     ", Counter(r["ch_certificate"] for r in gt7))
    print("  their active_challenge_days:", dict(sorted(Counter(r["active_challenge_days"] for r in gt7).items())))
    print("  their lessons_started:      ", dict(sorted(Counter(r["ch_lessons_started"] for r in gt7).items())))
print("\n  cross-check — completed_course flag by completion count:")
by = defaultdict(lambda: [0, 0])
for r in takers:
    b = min(r["ch_lessons_completed"], 9)
    by[b][0] += r["ch_completed_course"]
    by[b][1] += 1
for k in sorted(by):
    print(f"    {k} lessons: course_completed {by[k][0]:4d}/{by[k][1]:4d}")

# ---------------------------------------------------------------- Q3
print("\n" + "=" * 78)
print("Q3 · DOSE-RESPONSE: outcome by exact number of challenge lessons completed")
print("     (retention anchored on first_seen so it is comparable across everyone)")
print("=" * 78)
hdr = f"  {'lessons':>8} {'n':>5} | {'D1':>20} {'D3':>20} {'D7 (n obs)':>26} | {'unsub':>18}"
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for k in sorted(set(min(r["ch_lessons_completed"], 8) for r in takers)):
    g = [r for r in takers if min(r["ch_lessons_completed"], 8) == k]
    n = len(g)
    d7obs = [r for r in g if r["fs_days_observed"] >= 7]
    print(f"  {k:>8} {n:>5} | {rate_ci(sum(r['fs_ret_d1'] for r in g), n):>20}"
          f" {rate_ci(sum(r['fs_ret_d3'] for r in g), n):>20}"
          f" {rate_ci(sum(r['fs_ret_d7'] for r in d7obs), len(d7obs)):>20} ({len(d7obs):>3})"
          f" | {rate_ci(sum(r['unsubscribed'] for r in g), n):>18}")

print("\n  same, by ACTIVE CHALLENGE DAYS (the mechanic's own unit: 1 day = 1 skill)")
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for k in sorted(set(min(r["active_challenge_days"], 7) for r in takers)):
    g = [r for r in takers if min(r["active_challenge_days"], 7) == k]
    n = len(g)
    d7obs = [r for r in g if r["fs_days_observed"] >= 7]
    print(f"  {k:>8} {n:>5} | {rate_ci(sum(r['fs_ret_d1'] for r in g), n):>20}"
          f" {rate_ci(sum(r['fs_ret_d3'] for r in g), n):>20}"
          f" {rate_ci(sum(r['fs_ret_d7'] for r in d7obs), len(d7obs)):>20} ({len(d7obs):>3})"
          f" | {rate_ci(sum(r['unsubscribed'] for r in g), n):>18}")

# ---------------------------------------------------------------- Q4
print("\n" + "=" * 78)
print("Q4 · observation window / censoring")
print("=" * 78)
print(f"  last data date: {LAST_DATA_DATE}")
print("  days from first_seen to last data date:")
c = Counter(r["fs_days_observed"] for r in rows)
for k in sorted(c):
    print(f"    {k:2d} days: {c[k]:5d}")
for h in (1, 3, 7):
    n = sum(1 for r in rows if r["fs_days_observed"] >= h)
    print(f"  D{h} observable for {n}/{len(rows)} ({n/len(rows):.1%}) of subscribers")

# ---------------------------------------------------------------- Q5
print("\n" + "=" * 78)
print("Q5 · is challenge 338 effectively THE Challenge feature?")
print("=" * 78)
print("  started_any_challenge:", sum(r["started_any_challenge"] for r in rows))
print("  group_338 == took_338:", len(takers))
print("  took_other_challenge :", sum(1 for r in rows if r["group_338"] == "took_other_challenge"))
print("  → 338 covers %.1f%% of all challenge starters." %
      (100 * len(takers) / max(1, sum(r["started_any_challenge"] for r in rows))))
