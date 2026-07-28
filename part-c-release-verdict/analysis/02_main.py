"""Part C · Task 1 — the full release analysis. Every number in 01-analytics.md comes from here.

Sections
  §1  The exposure ladder — how many paying subscribers ever reach the Challenge at all
  §2  Engagement-tier definition + calibration (why the cut sits where it sits)
  §3  The headline comparison: high / low / didn't take it  × D1, D3, D7, unsub, completion, CSAT
  §4  Confound control — three tests of whether the tier gap is causal or selection
  §5  The mechanic check — is it actually a *daily* challenge?
  §6  Segments — age, gender, goal, work status, plan
  §7  Unsubscribes — who and why
"""
from collections import Counter, defaultdict
from lib import load, wilson, two_prop_z, stars, rate_ci, mean

rows = load()
N = len(rows)
takers = [r for r in rows if r["took"]]


def line(c="-", n=100):
    print(c * n)


def head(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)


# ═══════════════════════════════════════════════════════════ §1
head("§1 · THE EXPOSURE LADDER — of every paying subscriber, who ever reaches the Challenge?")

ladder = [
    ("Paying subscribers in the cohort", lambda r: True),
    ("… saw the Challenge popup",        lambda r: r["saw_challenge_popup"]),
    ("… clicked the popup",              lambda r: r["clicked_challenge_popup"]),
    ("… viewed a Challenge page",        lambda r: r["viewed_any_challenge"]),
    ("… joined Challenge 338",           lambda r: r["group_338"] in ("took_338", "joined_338_never_started")),
    ("… STARTED Challenge 338",          lambda r: r["took"]),
    ("… completed ≥1 challenge lesson",  lambda r: r["ch_lessons_completed"] >= 1),
    ("… completed ≥3 challenge lessons", lambda r: r["ch_lessons_completed"] >= 3),
    ("… completed the whole challenge",  lambda r: r["ch_completed_course"] == 1),
    ("… took the certificate",           lambda r: r["ch_certificate"] == 1),
]
prev = None
print(f"  {'step':<36} {'n':>6} {'% of cohort':>13} {'step conv.':>12}")
line()
for label, fn in ladder:
    n = sum(1 for r in rows if fn(r))
    conv = f"{n/prev:.1%}" if prev else "—"
    print(f"  {label:<36} {n:>6} {n/N:>12.1%} {conv:>12}")
    prev = n

print("\n  Where the audience is lost (share of the whole paying cohort):")
never_saw = sum(1 for r in rows if not r["saw_challenge_popup"] and not r["viewed_any_challenge"])
print(f"    never reached any challenge surface : {never_saw:>6}  ({never_saw/N:.1%})")
print(f"    reached a surface, never started 338: {N - never_saw - len(takers):>6}  "
      f"({(N-never_saw-len(takers))/N:.1%})")
print(f"    started 338                        : {len(takers):>6}  ({len(takers)/N:.1%})")

# ═══════════════════════════════════════════════════════════ §2
head("§2 · ENGAGEMENT TIERS — definition and calibration")

print("""  The Challenge ships 8 lessons (confirmed: every user flagged `course_completed`
  has exactly 8 completions). So 'finished' = 8, and the day-3 content sits at lesson 3.

  Tier rule (stated up front, applied everywhere below):
    HIGH        started 338 AND completed >= 3 of the 8 lessons  (got past the Day-2 cliff)
    LOW         started 338 AND completed <= 2 lessons
    DIDN'T TAKE never started 338
  The cut is at 3 because that is where the D7 curve steps (18% -> 39%) and it matches the
  product's own claim ('one day = one skill' -> 3 lessons = a 3-day habit). §4 tests it for
  robustness at every other threshold.""")

hist = Counter(r["ch_lessons_completed"] for r in takers)
print(f"\n  Challenge-lesson completion histogram (n={len(takers)} starters):")
cum = 0
for k in sorted(hist):
    cum += hist[k]
    bar = "█" * round(hist[k] / len(takers) * 60)
    print(f"    {k} lessons {hist[k]:>4} {hist[k]/len(takers):>7.1%}  cum {cum/len(takers):>6.1%}  {bar}")


print("\n  Lesson-by-lesson survival INSIDE the challenge (of the 1,111 who pressed start):")
print(f"    {'reached lesson':<18}{'n':>7}{'% of starters':>16}{'survived prev. step':>22}")
line()
prev = len(takers)
for k in range(1, 9):
    n = sum(1 for r in takers if r["ch_lessons_completed"] >= k)
    print(f"    completed >= {k:<6}{n:>7}{n/len(takers):>16.1%}{n/prev:>22.1%}")
    prev = n


def tier(r):
    if not r["took"]:
        return "didnt_take"
    return "high" if r["ch_lessons_completed"] >= 3 else "low"


for r in rows:
    r["tier"] = tier(r)

TIERS = ["high", "low", "didnt_take"]
LABEL = {"high": "HIGH (3+ lessons)", "low": "LOW (0–2 lessons)", "didnt_take": "DIDN'T TAKE IT"}
G = {t: [r for r in rows if r["tier"] == t] for t in TIERS}
print("\n  Tier sizes:")
for t in TIERS:
    print(f"    {LABEL[t]:<22} {len(G[t]):>6}  ({len(G[t])/N:.1%} of subscribers)")

# ═══════════════════════════════════════════════════════════ §3
head("§3 · THE HEADLINE COMPARISON  (retention anchored on each user's FIRST APP DAY for all "
     "three groups,\n     so the groups are on the same clock — see §4 for why this matters)")


def metrics(g):
    n = len(g)
    d7 = [r for r in g if r["fs_days_observed"] >= 7]
    csat_vals = [r["avg_csat_all"] for r in g if r["csat_n_all"] > 0]
    return {
        "n": n,
        "d1": (sum(r["fs_ret_d1"] for r in g), n),
        "d3": (sum(r["fs_ret_d3"] for r in g), n),
        "d7": (sum(r["fs_ret_d7"] for r in d7), len(d7)),
        "unsub": (sum(r["unsubscribed"] for r in g), n),
        "lessons_all": mean([r["lessons_completed_all"] for r in g]),
        "active_days": mean([r["active_days_total"] for r in g]),
        "csat": mean(csat_vals),
        "csat_n": len(csat_vals),
    }


M = {t: metrics(G[t]) for t in TIERS}
print(f"  {'metric':<28}" + "".join(f"{LABEL[t]:>26}" for t in TIERS))
line()
for key, name in [("d1", "D1 retention  ★TARGET"), ("d3", "D3 retention"), ("d7", "D7 retention"),
                  ("unsub", "Unsubscribe rate")]:
    print(f"  {name:<28}" + "".join(f"{rate_ci(*M[t][key]):>26}" for t in TIERS))
print(f"  {'  (D7 denominator)':<28}" + "".join(f"{M[t]['d7'][1]:>26}" for t in TIERS))
line()
print(f"  {'Avg lessons completed (all)':<28}" + "".join(f"{M[t]['lessons_all']:>26.2f}" for t in TIERS))
print(f"  {'Avg active days in product':<28}" + "".join(f"{M[t]['active_days']:>26.2f}" for t in TIERS))
print(f"  {'Avg CSAT (1–5)':<28}" + "".join(
    f"{(f'{M[t]['csat']:.2f}' if M[t]['csat'] else '—'):>26}" for t in TIERS))
print(f"  {'  (CSAT raters)':<28}" + "".join(f"{M[t]['csat_n']:>26}" for t in TIERS))

print("\n  Significance vs 'didn't take it':")
for t in ("high", "low"):
    for key, name in [("d1", "D1"), ("d3", "D3"), ("d7", "D7"), ("unsub", "unsub")]:
        k1, n1 = M[t][key]
        k2, n2 = M["didnt_take"][key]
        d, z, p = two_prop_z(k1, n1, k2, n2)
        print(f"    {LABEL[t]:<20} {name:<6} diff {d:+7.1%}  z={z:+6.2f}  p={p:.2e}  {stars(p)}")

# ═══════════════════════════════════════════════════════════ §4
head("§4 · IS THE GAP CAUSAL? — three tests")

print("""  TEST A — EXPOSURE-MATCHED CONTROL.
  'Didn't take it' is not one group: most of them were never offered the Challenge.
  The fair control is people who DID reach the Challenge and chose not to engage.""")

EXP = [
    ("started 338 (takers)",        lambda r: r["took"]),
    ("joined 338, never started",   lambda r: r["group_338"] == "joined_338_never_started"),
    ("viewed 338, never joined",    lambda r: r["group_338"] == "viewed_338_never_joined"),
    ("saw popup, never opened 338", lambda r: r["group_338"] == "no_challenge" and r["saw_challenge_popup"]),
    ("never reached a surface",     lambda r: r["group_338"] == "no_challenge" and not r["saw_challenge_popup"]
                                              and not r["viewed_any_challenge"]),
]
print(f"\n  {'exposure group':<32}{'n':>7}{'D1':>22}{'D3':>22}{'unsub':>20}")
line()
for label, fn in EXP:
    g = [r for r in rows if fn(r)]
    if not g:
        continue
    n = len(g)
    print(f"  {label:<32}{n:>7}"
          f"{rate_ci(sum(r['fs_ret_d1'] for r in g), n):>22}"
          f"{rate_ci(sum(r['fs_ret_d3'] for r in g), n):>22}"
          f"{rate_ci(sum(r['unsubscribed'] for r in g), n):>20}")

ctrl = [r for r in rows if r["group_338"] in ("joined_338_never_started", "viewed_338_never_joined")]
d, z, p = two_prop_z(sum(r["fs_ret_d1"] for r in takers), len(takers),
                     sum(r["fs_ret_d1"] for r in ctrl), len(ctrl))
print(f"\n  takers vs exposed-but-didn't-start:  D1 diff {d:+.1%}  z={z:+.2f}  p={p:.3f}  {stars(p)}")
d, z, p = two_prop_z(sum(r["unsubscribed"] for r in takers), len(takers),
                     sum(r["unsubscribed"] for r in ctrl), len(ctrl))
print(f"  takers vs exposed-but-didn't-start:  unsub diff {d:+.1%}  z={z:+.2f}  p={p:.3f}  {stars(p)}")

print("""

  TEST B — IMMORTAL-TIME BIAS.
  Only 24% of takers start on their first app day; the median taker starts on day +1.
  To start on day +k you must already have survived to day k — so takers are pre-selected
  survivors. The clean read is the 'day-0 starters' who had no survival head start.""")

lag = Counter(r["days_to_challenge"] for r in takers)
print(f"\n  taker start-day lag: day0 {lag.get(0,0)} ({lag.get(0,0)/len(takers):.0%}), "
      f"day+1 {lag.get(1,0)} ({lag.get(1,0)/len(takers):.0%}), "
      f"day+2 {lag.get(2,0)} ({lag.get(2,0)/len(takers):.0%}), "
      f"day+3 or later {sum(v for k,v in lag.items() if k>=3)} "
      f"({sum(v for k,v in lag.items() if k>=3)/len(takers):.0%})")

d0 = [r for r in takers if r["days_to_challenge"] == 0]
nt = G["didnt_take"]
print(f"\n  {'group':<40}{'n':>7}{'D1':>22}{'D3':>22}")
line()
print(f"  {'takers who started on day 0':<40}{len(d0):>7}"
      f"{rate_ci(sum(r['fs_ret_d1'] for r in d0), len(d0)):>22}"
      f"{rate_ci(sum(r['fs_ret_d3'] for r in d0), len(d0)):>22}")
print(f"  {'all takers (any start day)':<40}{len(takers):>7}"
      f"{rate_ci(sum(r['fs_ret_d1'] for r in takers), len(takers)):>22}"
      f"{rate_ci(sum(r['fs_ret_d3'] for r in takers), len(takers)):>22}")
print(f"  {'never took it':<40}{len(nt):>7}"
      f"{rate_ci(sum(r['fs_ret_d1'] for r in nt), len(nt)):>22}"
      f"{rate_ci(sum(r['fs_ret_d3'] for r in nt), len(nt)):>22}")
d, z, p = two_prop_z(sum(r["fs_ret_d1"] for r in d0), len(d0),
                     sum(r["fs_ret_d1"] for r in nt), len(nt))
print(f"\n  day-0 takers vs never-took:  D1 diff {d:+.1%}  z={z:+.2f}  p={p:.2e}  {stars(p)}")

print("""

  TEST C — A NON-TAUTOLOGICAL DOSE-RESPONSE.
  'More lessons -> better retention' is partly circular: doing lesson 3 on day 3 IS retention.
  The clean version: among users whose challenge activity happened on ONE day only, does a
  bigger DAY-0 dose predict coming back tomorrow? Nothing circular here.""")

oneday = [r for r in takers if r["active_challenge_days"] == 1]
print(f"\n  n = {len(oneday)} takers with all challenge activity on a single day")
print(f"  {'day-0 lessons':<16}{'n':>7}{'D1 next day':>24}{'unsub':>20}")
line()
for k in range(0, 9):
    g = [r for r in oneday if r["ch_lessons_completed"] == k]
    if len(g) < 5:
        continue
    print(f"  {k:<16}{len(g):>7}"
          f"{rate_ci(sum(r['fs_ret_d1'] for r in g), len(g)):>24}"
          f"{rate_ci(sum(r['unsubscribed'] for r in g), len(g)):>20}")
lo = [r for r in oneday if r["ch_lessons_completed"] <= 1]
hi = [r for r in oneday if r["ch_lessons_completed"] >= 2]
d, z, p = two_prop_z(sum(r["fs_ret_d1"] for r in hi), len(hi),
                     sum(r["fs_ret_d1"] for r in lo), len(lo))
print(f"\n  >=2 vs <=1 day-0 lessons:  D1 diff {d:+.1%}  z={z:+.2f}  p={p:.3f}  {stars(p)}")

print("\n\n  THRESHOLD ROBUSTNESS — the 'high' cut at every possible value:")
print(f"  {'high = >= k lessons':<22}{'n high':>8}{'D1 high':>12}{'D1 low':>12}{'D1 gap':>10}"
      f"{'unsub high':>13}{'unsub low':>12}")
line()
for k in range(1, 9):
    hg = [r for r in takers if r["ch_lessons_completed"] >= k]
    lg = [r for r in takers if r["ch_lessons_completed"] < k]
    if not hg or not lg:
        continue
    h1, l1 = sum(r["fs_ret_d1"] for r in hg) / len(hg), sum(r["fs_ret_d1"] for r in lg) / len(lg)
    hu, lu = sum(r["unsubscribed"] for r in hg) / len(hg), sum(r["unsubscribed"] for r in lg) / len(lg)
    print(f"  {k:<22}{len(hg):>8}{h1:>12.1%}{l1:>12.1%}{h1-l1:>+10.1%}{hu:>13.1%}{lu:>12.1%}")

# ═══════════════════════════════════════════════════════════ §5
head("§5 · THE MECHANIC CHECK — is this actually a DAILY challenge?")

print("""  The hypothesis was 'one day = one skill builds a daily habit'. That only works if the
  content is gated to one lesson per day. Test: how many lessons do people do per active day?""")

finishers = [r for r in takers if r["ch_completed_course"] == 1]
print(f"\n  Users who completed the whole 8-lesson challenge: {len(finishers)} "
      f"({len(finishers)/len(takers):.1%} of starters, {len(finishers)/N:.2%} of subscribers)")
fd = Counter(r["active_challenge_days"] for r in finishers)
print("\n  … and how many DAYS they took to do it:")
cum = 0
for k in sorted(fd):
    cum += fd[k]
    bar = "█" * round(fd[k] / len(finishers) * 50)
    print(f"    {k:>2} day(s): {fd[k]:>3}  ({fd[k]/len(finishers):>6.1%})  cum {cum/len(finishers):>6.1%}  {bar}")
in1 = sum(v for k, v in fd.items() if k == 1)
in2 = sum(v for k, v in fd.items() if k <= 2)
print(f"\n  → {in1}/{len(finishers)} ({in1/len(finishers):.0%}) finished the '7-day' challenge in ONE day.")
print(f"  → {in2}/{len(finishers)} ({in2/len(finishers):.0%}) finished it in two days or fewer.")

print("\n  Lessons completed per active challenge day (all takers who did >=1 lesson):")
did = [r for r in takers if r["ch_lessons_completed"] >= 1]
rate = Counter(round(r["ch_lessons_completed"] / max(1, r["active_challenge_days"]), 0) for r in did)
for k in sorted(rate):
    print(f"    ~{int(k)} lessons/day: {rate[k]:>4}  ({rate[k]/len(did):.1%})")
print(f"\n  mean lessons per active challenge day: "
      f"{mean([r['ch_lessons_completed']/max(1,r['active_challenge_days']) for r in did]):.2f}")

print("\n  Return behaviour: of takers who did >=1 lesson, how many ever came back for a 2nd challenge day?")
back = sum(1 for r in did if r["active_challenge_days"] >= 2)
print(f"    {back}/{len(did)} = {back/len(did):.1%}")

# ═══════════════════════════════════════════════════════════ §6
head("§6 · SEGMENTS")


def seg_table(field, title, min_n=30):
    print(f"\n  ── {title} ──")
    print(f"  {'segment':<34}{'subs':>7}{'% cohort':>10}{'take rate':>12}"
          f"{'D1 (all)':>12}{'unsub':>10}{'D1 takers':>12}{'D1 non-tk':>12}")
    line()
    vals = Counter(r[field] or "(unknown)" for r in rows)
    for v, cnt in sorted(vals.items(), key=lambda x: -x[1]):
        if cnt < min_n:
            continue
        g = [r for r in rows if (r[field] or "(unknown)") == v]
        tk = [r for r in g if r["took"]]
        ntk = [r for r in g if not r["took"]]
        print(f"  {str(v)[:33]:<34}{cnt:>7}{cnt/N:>10.1%}{len(tk)/cnt:>12.1%}"
              f"{sum(r['fs_ret_d1'] for r in g)/cnt:>12.1%}"
              f"{sum(r['unsubscribed'] for r in g)/cnt:>10.1%}"
              f"{(sum(r['fs_ret_d1'] for r in tk)/len(tk) if tk else 0):>12.1%}"
              f"{(sum(r['fs_ret_d1'] for r in ntk)/len(ntk) if ntk else 0):>12.1%}")


seg_table("age", "AGE")
seg_table("gender", "GENDER")
seg_table("plan", "PLAN")
seg_table("status", "WORK STATUS", min_n=150)
seg_table("goal", "GOAL", min_n=150)
seg_table("country_code", "COUNTRY", min_n=150)

print("\n  ── AGE × GENDER (the PM's claim: 'our main market is 40–50 y.o. men') ──")
ages = ["18-24", "25-34", "35-44", "45-54", "55+"]
genders = ["Male", "Female"]
print(f"  {'age':<10}" + "".join(f"{g:>12}" for g in genders) + f"{'other/NA':>12}{'row total':>12}{'row %':>9}")
line()
colt = defaultdict(int)
for a in ages:
    ga = [r for r in rows if r["age"] == a]
    if not ga:
        continue
    cells = []
    for g in genders:
        c = sum(1 for r in ga if r["gender"] == g)
        cells.append(c)
        colt[g] += c
    other = len(ga) - sum(cells)
    colt["other"] += other
    print(f"  {a:<10}" + "".join(f"{c:>12}" for c in cells) +
          f"{other:>12}{len(ga):>12}{len(ga)/N:>9.1%}")
print(f"  {'TOTAL':<10}" + "".join(f"{colt[g]:>12}" for g in genders) +
      f"{colt['other']:>12}{N:>12}")
print("  " + " " * 8 + "".join(f"{colt[g]/N:>12.1%}" for g in genders))

m4054 = sum(1 for r in rows if r["gender"] == "Male" and r["age"] in ("35-44", "45-54"))
a4054 = sum(1 for r in rows if r["age"] in ("35-44", "45-54"))
print(f"\n  Men aged 35–54            : {m4054:>6}  ({m4054/N:.1%} of paying subscribers)")
print(f"  Everyone aged 35–54       : {a4054:>6}  ({a4054/N:.1%})")
print(f"  All men                   : {colt['Male']:>6}  ({colt['Male']/N:.1%})")
print(f"  All women                 : {colt['Female']:>6}  ({colt['Female']/N:.1%})")
print(f"  Aged 45+                  : {sum(1 for r in rows if r['age'] in ('45-54','55+')):>6} "
      f"({sum(1 for r in rows if r['age'] in ('45-54','55+'))/N:.1%})")

# ═══════════════════════════════════════════════════════════ §7
head("§7 · UNSUBSCRIBES")

uns = [r for r in rows if r["unsubscribed"]]
print(f"  total unsubscribed in cohort: {len(uns)} / {N} = {len(uns)/N:.1%}")
print(f"\n  {'plan':<16}{'subs':>8}{'unsub':>8}{'rate':>22}")
line()
for p, c in Counter(r["plan"] for r in rows).most_common():
    if c < 50:
        continue
    g = [r for r in rows if r["plan"] == p]
    print(f"  {p:<16}{c:>8}{sum(r['unsubscribed'] for r in g):>8}"
          f"{rate_ci(sum(r['unsubscribed'] for r in g), c):>22}")

print(f"\n  {'tier':<24}{'n':>8}{'unsub':>8}{'rate':>22}")
line()
for t in TIERS:
    g = G[t]
    print(f"  {LABEL[t]:<24}{len(g):>8}{sum(r['unsubscribed'] for r in g):>8}"
          f"{rate_ci(sum(r['unsubscribed'] for r in g), len(g)):>22}")

print("\n  Stated reason (only recorded for some unsubscribes):")
rc = Counter(r["unsub_reason"] or "(none recorded)" for r in uns)
for k, v in rc.most_common():
    print(f"    {k:<28}{v:>6}  ({v/len(uns):.1%} of unsubs)")
invol = {"hard_decline", "Mastercard Alert", "dispute", "paypal_refund", "Visa CDRN",
         "fraud", "Merchanto visa", "payment_refunded", "fraud_reported"}
ni = sum(v for k, v in rc.items() if k in invol)
print(f"\n  → payment-failure / chargeback / refund-dispute reasons: {ni} "
      f"({ni/len(uns):.1%} of unsubs, {ni/N:.1%} of the cohort)")

print("\n  Do challenge takers unsubscribe less? (raw, uncontrolled)")
for label, g in [("takers", takers), ("non-takers", G["didnt_take"])]:
    print(f"    {label:<14}{sum(r['unsubscribed'] for r in g):>6}/{len(g):<6} "
          f"= {rate_ci(sum(r['unsubscribed'] for r in g), len(g))}")
d, z, p = two_prop_z(sum(r["unsubscribed"] for r in takers), len(takers),
                     sum(r["unsubscribed"] for r in G["didnt_take"]), len(G["didnt_take"]))
print(f"    diff {d:+.1%}  z={z:+.2f}  p={p:.3f}  {stars(p)}")
