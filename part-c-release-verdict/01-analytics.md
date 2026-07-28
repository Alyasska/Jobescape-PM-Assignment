# Part C · Task 1 — Release Analytics

**Data:** BigQuery `persona-496908.sql_assessment` (`app_events` + `subscribe_events`), pulled 2026-07-27.
**Cohort:** all **9,956 paying subscribers** whose first app activity falls in **2026-06-12 → 2026-06-25** (14 days). Every user in `app_events` has a purchase row — the product sits entirely behind the paywall, so "user" = "payer" throughout.
**Feature:** `course_id = 338` — *7-Day Claude Challenge*, shipped in 6 languages. It is **99.7% of all challenge starts** in the window (1,111 of 1,114), so "the Challenge" and "338" are interchangeable here.
**Queries:** [`sql/13_comparison_groups.sql`](sql/13_comparison_groups.sql) (the one-row-per-user export) and [`sql/10`–`12`](sql/). **All calculations:** [`analysis/`](analysis/) — `02_main.py`, `03_supplement.py`, `04_loose_ends.py`. Every number below is reproducible by running those three files.

---

## The three findings, up front

1. **Reach — 89% of paying subscribers never start the Challenge.** Two-thirds (67.5%) never see a challenge surface at all.
2. **Effect — the target metric does not move.** Users who took the Challenge retain at **60.0% D1**; users who *looked at the Challenge and walked away* retain at **59.6%**. The difference is **+0.5 pts, p = 0.82.** The headline "+38 pt" gap is selection, not the feature.
3. **Mechanic — the gate is soft.** A warning appears if you start the next lesson early, then lets you through. Nothing enforces it and no event records it, so nothing gates the content to one lesson per day. **27% of finishers completed the whole "7-day" challenge in a single day**, 46% within two. The habit engine the hypothesis depends on was never actually shipped.

A fourth finding is the reason "just show it to more people" is the wrong response: **satisfaction falls as engagement rises** — CSAT goes 3.74 (never took it) → 3.53 (low) → 3.33 (high) → **3.10 (finished it)**.

---

## 1 · Where the audience goes — the exposure ladder

Before any retention question: how many payers reach the feature at all?

| Step | Users | % of all subscribers | Conversion from previous step |
|---|---:|---:|---:|
| Paying subscribers in the cohort | 9,956 | 100% | — |
| … saw the Challenge popup | 3,140 | 31.5% | **31.5%** |
| … clicked the popup | 2,970 | 29.8% | 94.6% |
| … viewed a Challenge page | 2,109 | 21.2% | 71.0% |
| … joined Challenge 338 | 1,341 | 13.5% | 63.6% |
| … **started** Challenge 338 | **1,111** | **11.2%** | 82.8% |
| … completed ≥1 challenge lesson | 612 | 6.1% | **55.1%** |
| … completed ≥3 lessons | 158 | 1.6% | 25.8% |
| … completed the whole challenge | 48 | 0.5% | 30.4% |
| … downloaded/shared the certificate | 23 | 0.2% | 47.9% |

**The single biggest leak is the very first step: 68.5% of payers never see the popup.** Once someone *does* see it, the funnel is healthy — 94.6% click it. This is a distribution problem, not a desirability problem.

Split of the whole cohort by how far they got:

| | Users | % |
|---|---:|---:|
| Never reached any challenge surface | 6,716 | 67.5% |
| Reached a surface, never started | 2,129 | 21.4% |
| Started the Challenge | 1,111 | 11.2% |

## 2 · Inside the Challenge — where starters die

The Challenge ships **8 lessons**, not 7 (every user flagged `course_completed` has exactly 8 completions — a naming/scope mismatch worth fixing on its own).

| Reached | Users | % of the 1,111 starters | Survived the previous step |
|---|---:|---:|---:|
| pressed Start | 1,111 | 100% | — |
| completed ≥1 lesson | 612 | 55.1% | **55.1%** |
| completed ≥2 | 308 | 27.7% | **50.3%** |
| completed ≥3 | 158 | 14.2% | 51.3% |
| completed ≥4 | 105 | 9.5% | 66.5% |
| completed ≥5 | 80 | 7.2% | 76.2% |
| completed ≥6 | 62 | 5.6% | 77.5% |
| completed ≥7 | 52 | 4.7% | 83.9% |
| completed all 8 | 47 | 4.2% | 90.4% |

**Two cliffs, both at the front.** 45% press Start and do nothing at all; half of those who do lesson 1 never do lesson 2. Past lesson 3 the drop-off almost stops — survival climbs from 51% to 90%. The content is not the problem for people who get in; **getting in is the problem.**

## 3 · Engagement tiers — definition and calibration

The brief asks me to define high and low myself. I use **challenge lessons completed**, because it is the only effort measure that isn't circular with retention (see §5, Test C).

| Tier (brief) | My name | Rule | Users | % of subscribers |
|---|---|---|---:|---:|
| **HIGH** | Doers + Finishers | started, completed **≥3** of 8 lessons | **158** | 1.6% |
| **LOW** | No-shows + Samplers | started, completed **≤2** | **953** | 9.6% |
| **DIDN'T TAKE IT** | Never offered + Passed on it | never started 338 | **8,845** | 88.8% |

**Why the cut is at 3.** Three reasons, all checkable:
- It is where the D7 curve steps — 18% at ≤2 lessons, 39% at ≥3.
- It matches the product's own claim: "one day = one skill", so 3 lessons ≈ a 3-day habit.
- **It is not cherry-picked.** Sweeping the threshold across every possible value (`02_main.py` §4):

| High = ≥ k lessons | n high | D1 high | D1 low | D1 gap | unsub high | unsub low |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 612 | 61.4% | 58.3% | +3.1 | 12.7% | 9.8% |
| 2 | 308 | 63.3% | 58.8% | +4.5 | 13.0% | 10.8% |
| **3** | **158** | **69.6%** | **58.4%** | **+11.2** | 11.4% | 11.4% |
| 4 | 105 | 74.3% | 58.5% | +15.7 | 10.5% | 11.5% |
| 5 | 80 | 78.8% | 58.6% | +20.2 | 10.0% | 11.5% |
| 6 | 62 | 80.6% | 58.8% | +21.8 | 11.3% | 11.4% |
| 7 | 52 | 76.9% | 59.2% | +17.7 | 11.5% | 11.4% |
| 8 | 47 | 76.6% | 59.3% | +17.3 | 12.8% | 11.4% |

The retention gap grows monotonically with the cut — and **the unsubscribe gap is ~0 at every threshold.** Whatever separates high from low engagement, it does not show up in the metric that pays the bills.

## 4 · The headline comparison

All three groups anchored on **each user's first app day**, so they are on the same clock. (§5 Test B explains why this matters and what the team's own anchor does to the numbers.) Brackets are 95% Wilson intervals.

| Metric | HIGH (3+ lessons) | LOW (0–2 lessons) | DIDN'T TAKE IT |
|---|---|---|---|
| **D1 retention ★ target** | **69.6%** [62.1–76.3] | **58.4%** [55.3–61.5] | **21.7%** [20.9–22.6] |
| D3 retention | 57.0% [49.2–64.4] | 34.4% [31.5–37.5] | 10.0% [9.4–10.6] |
| D7 retention | 39.1% [31.2–47.6] | 18.0% [15.4–21.0] | 6.9% [6.3–7.5] |
| Unsubscribe rate | 11.4% [7.3–17.3] | 11.4% [9.6–13.6] | 14.3% [13.6–15.1] |
| *(D7 denominator)* | *133* | *737* | *6,345* |
| Avg lessons completed (all courses) | 19.28 | 6.38 | 1.81 |
| Avg active days in product | 5.37 | 3.46 | 1.76 |
| **Avg CSAT (1–5)** | **3.33** | **3.53** | **3.74** |
| *(CSAT raters)* | *158* | *845* | *3,740* |

Significance vs "didn't take it" (two-proportion z-test):

| Comparison | Diff | z | p | |
|---|---:|---:|---|---|
| HIGH — D1 | +47.9 pts | +14.27 | <1e-15 | *** |
| LOW — D1 | +36.7 pts | +24.76 | <1e-15 | *** |
| HIGH — D7 | +32.2 pts | +13.92 | <1e-15 | *** |
| HIGH — unsubscribe | −2.9 pts | −1.04 | 0.298 | ns |
| LOW — unsubscribe | −2.9 pts | −2.43 | 0.015 | * |

**Read literally, this table says the Challenge triples D1 retention.** It does not. §5 is the actual analysis.

## 5 · Is the gap causal? — four tests

An "engaged users retain better" result is what selection produces on its own: motivated users both take challenges *and* come back. Four ways to break the claim.

### Test A — exposure-matched control *(the decisive one)*

"Didn't take it" is not one group. Most of them were never offered the feature. The fair comparison is people who **reached the Challenge and chose not to engage**.

| Exposure group | n | D1 | D3 | Unsubscribe |
|---|---:|---|---|---|
| **Started 338** | 1,111 | **60.0%** [57.1–62.9] | 37.6% | 11.4% |
| Joined 338, never started | 230 | **60.4%** [54.0–66.5] | 37.8% | 13.9% |
| Viewed 338, never joined | 764 | **59.3%** [55.8–62.7] | 36.6% | 13.6% |
| **↳ the two combined = the control** | **994** | **59.6%** | 36.9% | 13.7% |
| Saw the popup, never opened 338 | 1,132 | 44.9% [42.0–47.8] | 24.0% | **25.5%** |
| Never reached a challenge surface | 6,716 | 12.2% [11.4–13.0] | 3.7% | 12.5% |

> **Takers vs exposed-but-didn't-start: D1 diff +0.5 pts, z = +0.22, p = 0.823 (ns).**
> Unsubscribe diff −2.3 pts, p = 0.119 (ns).

People who joined the Challenge and never opened a lesson retain **exactly as well** as people who completed it. The predictive power sits entirely in *reaching the challenge surface* — i.e. in being an engaged user — not in the Challenge doing anything.

**Tightened further:** holding total product activity constant, the effect stays at zero (`04_loose_ends.py`).

| Active days in product | n takers | D1 takers | n control | D1 control | Diff | p |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 97 | 0.0% | 63 | 0.0% | +0.0 | 1.000 |
| 2 | 270 | 46.3% | 257 | 42.4% | +3.9 | 0.370 |
| 3–4 | 446 | 64.8% | 427 | 65.1% | −0.3 | 0.924 |
| 5–7 | 217 | 82.9% | 205 | 84.4% | −1.4 | 0.689 |
| 8+ | 81 | 90.1% | 42 | 76.2% | +13.9 | 0.038 |

Four of five strata are flat. The one significant cell is the smallest (n = 81 vs 42) and is one of five tests — it does not survive multiple comparisons.

### Test B — immortal-time bias

Only **24% of takers start the Challenge on their first app day**; the median taker starts on **day +1**, and 28% start on day +3 or later. To start on day *k* you must already have survived to day *k*. Takers are pre-selected survivors — the comparison is rigged before it begins.

| Group | n | D1 | D3 |
|---|---:|---|---|
| Takers who started on **day 0** | 266 | **39.1%** [33.4–45.1] | 22.6% |
| All takers (any start day) | 1,111 | 60.0% [57.1–62.9] | 37.6% |
| Never took it | 8,845 | 21.7% [20.9–22.6] | 10.0% |

Removing the survival head-start alone cuts the apparent gap from **+38 pts to +17 pts**. Test A removes the rest.

### Test C — a non-tautological dose-response

"More lessons → better retention" is partly circular: doing lesson 3 on day 3 *is* retention. The clean version: among the 816 takers whose entire challenge activity happened **on one day**, does a bigger day-0 dose predict coming back tomorrow? Nothing circular here.

| Lessons done on day 0 | n | D1 the next day | Unsubscribe |
|---:|---:|---|---|
| 0 | 429 | 55.7% [51.0–60.3] | 10.5% |
| 1 | 248 | 54.4% [48.2–60.5] | 12.5% |
| 2 | 99 | 50.5% [40.8–60.1] | 11.1% |
| 3 | 21 | 33.3% [17.2–54.6] | 23.8% |
| 4 | 5 | 0.0% | 20.0% |
| 8 (binged the whole thing) | 13 | 53.8% [29.1–76.8] | **38.5%** |

> **≥2 vs ≤1 day-0 lessons: D1 diff −9.2 pts, z = −1.98, p = 0.048.**

**The dose-response is flat-to-negative.** Consuming more Challenge content on day 0 does not make you come back — and the users who consumed *all* of it unsubscribed at 38.5%. Which is the mechanic problem:

### Test D — is it even a daily challenge?

The hypothesis was *"one day = one skill builds a habit of returning every day."* That only works if the content is gated to one lesson per day. It isn't.

- **48 users completed the whole challenge.** Days they took to do it: **1 day → 13 (27%)**, 2 days → 9, 3 days → 6, 4 → 4, 5 → 5, 6 → 2, 7 → 3, 8 → 3, 9 → 2, 10 → 1.
- **46% finished the "7-day" challenge in two days or fewer.**
- **Mean lessons per active challenge day: 1.46.**
- Of the 612 starters who completed at least one lesson, only **225 (36.8%) ever came back for a second challenge day.**

There is no daily gate, no scheduled unlock, and no reason to return tomorrow rather than finish tonight. **v1 did not test the hypothesis** — it shipped a short course with "7-Day" in the title.

## 6 · The target metric as the team defined it

The brief defines D1 as *"retention the day after the challenge started."* That anchor produces a very different number:

| Measure | n | Rate |
|---|---:|---|
| Takers · D1 anchored on challenge-start **(team's definition)** | 1,111 | **39.8%** [36.9–42.7] |
| Takers · D3 anchored on challenge-start | 982 | 25.9% |
| Takers · D7 anchored on challenge-start | 606 | 14.7% |
| Takers · D1 anchored on first app day | 1,111 | 60.0% |
| **Whole cohort · D1, first app day** | 9,953 | **26.0%** |

**This is how the release gets misread.** On the team's own dashboard the Challenge shows **39.8% D1** against a product baseline of **26.0%** — a apparent +14-point win. But those are different clocks *and* different populations. Put on the same clock and matched on exposure, the effect is zero.

## 7 · Segments

### Age — and the one place I'd push back on the team's own read

| Age | Subscribers | % | Take rate | D1 (all) | **Unsubscribe** |
|---|---:|---:|---:|---:|---:|
| 55+ | 3,200 | 32.1% | 10.2% | 25.4% | **9.7%** |
| 45–54 | 2,551 | 25.6% | 10.9% | 26.9% | **9.5%** |
| 35–44 | 1,887 | 19.0% | 12.0% | 27.8% | 14.5% |
| 25–34 | 1,117 | 11.2% | 12.4% | 24.4% | 19.7% |
| 18–24 | 913 | 9.2% | 10.3% | 21.9% | **31.1%** |

**Unsubscribe falls monotonically with age. The oldest buyers are the best buyers** — 45+ churn at roughly a third the rate of under-25s, and they are the majority of the book.

Age × gender (paying subscribers):

| Age | Male | Female | Other/NA | Total | % |
|---|---:|---:|---:|---:|---:|
| 18–24 | 602 | 310 | 1 | 913 | 9.2% |
| 25–34 | 613 | 493 | 11 | 1,117 | 11.2% |
| 35–44 | 1,040 | 815 | 32 | 1,887 | 19.0% |
| 45–54 | 1,444 | 1,065 | 42 | 2,551 | 25.6% |
| **55+** | **2,120** | 1,035 | 45 | **3,200** | **32.1%** |
| **Total** | **5,948 (59.7%)** | **3,824 (38.4%)** | | 9,956 | |

> **On "our core market is 40–50-year-old men":** the gender half is right — **59.7% of buyers are men.** The age half understates it. **58–60% of paying subscribers are 45+**, and the single largest cell in the entire book is **men aged 55+ (2,120 users, 21.3% of all buyers)** — larger than men 35–54 combined (2,484, 24.9%) relative to any other single cell. This matches Part A's independent finding from the quiz export: of the 39,070 respondents who answered the age question (out of 49,528 total), **61.6% are 45+**.
>
> **Why it matters for this release:** a gamified streak-and-badge mechanic is designed for the audience Jobescape *doesn't* have. The buyer is a 55-year-old man who wants to stop feeling behind at work — competence and dignity framing, not confetti. It also matters commercially: the 45+ majority is the low-churn, high-LTV core, and the under-25s who respond best to gamification churn at 31%.

### Goal — the ads that sell the worst customers

| Stated goal | Subscribers | % | **Unsubscribe** |
|---|---:|---:|---:|
| Work faster | 3,015 | 30.3% | **10.9%** |
| Feel more confident with AI | 1,992 | 20.0% | **10.7%** |
| Start my own business | 1,161 | 11.7% | 10.9% |
| Earn more | 830 | 8.3% | 10.7% |
| Get a promotion / better job | 636 | 6.4% | 14.0% |
| Gain flexibility or work remotely | 492 | 4.9% | **27.4%** |
| Get a quick side hustle | 368 | 3.7% | **37.2%** |
| Unlock better income opportunities | 347 | 3.5% | **25.4%** |

The "get-rich-quick" intents churn at **2.5–3.5×** the core. They are only ~12% of the book, but they are a disproportionate share of refunds and disputes. This is Part A's positioning finding showing up as money.

### Plan

| Plan | Subscribers | % | **Unsubscribe** |
|---|---:|---:|---:|
| 4-Week | 6,341 | 63.7% | 12.2% |
| 12-Week | 2,495 | 25.1% | 10.6% |
| **1-Week** | **1,014** | **10.2%** | **34.6%** [31.8–37.6] |
| 4-Week special | 90 | 0.9% | 3.3% |

The 1-week plan churns at **3× everything else** — inside a 14-day window, i.e. mostly before or at its first renewal.

*Useful cross-check for Part D:* the real plan mix is **10.2% / 64.6% / 25.1%** against the brief's assumed **10% / 70% / 20%** — close enough to validate the LTV model, with a mild skew toward the 12-week plan that would nudge blended LTV slightly **up**.

### Work status

Full-time employee 33.6% (unsub 11.8%) · Business owner 18.3% (9.4%) · Freelancer/self-employed 14.9% (10.5%) · Exploring options 8.5% (18.6%) · Between jobs 5.8% (13.8%) · Student 1.8% (**37.1%**).

### Country

US 37.7% · GB 10.2% · AU 6.9% · CA 5.3% · IT 3.8% · AE 2.6% · DE 2.6% · FR 2.5% · SG 2.4% · ES 2.3%. Tier-1 English-speaking is ~60% of the book, consistent with the brief's stated market.

## 8 · Unsubscribes and satisfaction

**14.0% of the cohort unsubscribed inside 14 days** (1,393 of 9,956). Because the window is only 14 days, no 4-week subscriber can even reach a renewal decision — **every unsubscribe rate in this document is a floor, not a final value.**

Stated reasons (recorded for 37% of unsubscribes):

| Reason | n | % of unsubs |
|---|---:|---:|
| *(none recorded)* | 873 | 62.7% |
| Support request | 310 | 22.3% |
| hard_decline | 84 | 6.0% |
| account_deletion | 31 | 2.2% |
| Mastercard Alert | 30 | 2.2% |
| general | 22 | 1.6% |
| dispute / paypal_refund / Visa CDRN / fraud / Merchanto / payment_refunded / fraud_reported | 43 | 3.1% |

**157 of 1,393 unsubscribes (11.3%) are payment failures, chargebacks or refund disputes** — 1.6% of the whole paying cohort in two weeks. That is the Part A/Part D risk showing up in the event log.

### The satisfaction inversion

| Group | Raters | Mean CSAT | % rating 4–5 | % rating 1–2 |
|---|---:|---:|---:|---:|
| Never took the challenge | 3,740 | **3.74** | 59.8% | 17.5% |
| LOW (0–2 lessons) | 845 | 3.53 | 53.0% | 20.6% |
| HIGH (3+ lessons) | 158 | 3.33 | 38.6% | 19.6% |
| **Completed the whole challenge** | 48 | **3.10** | 37.5% | 22.9% |

Challenge-338 content specifically rates **3.25** (583 raters); the *same users* rate the rest of the product **3.45**. **The more of this feature someone consumes, the less they like the product.** Any plan that starts with "drive more traffic into the Challenge" would push more people down this curve.

### Does completion protect revenue? No.

Part A found (from public reviews) that finishing the course is the money-back gate. If completion were genuinely valuable we'd expect finishers to churn least; if it's a refund gate we'd expect the opposite. The data says **neither — completion is simply uncorrelated with churn**: finishers 12.5% vs non-finishers 11.4% (p = 0.812, ns).

One signal inside it: finishers who **binged in ≤2 days unsubscribe at 22.7%** (n = 22) while those who **spread it over 3+ days unsubscribe at 3.8%** (n = 26). Small numbers, so I hold this loosely — but it is consistent with everything above: *pace* is what matters, and the feature does nothing to control pace.

## 9 · What I'd flag before anyone acts on this

1. **There is no hold-out group.** Challenge starts occur on every single day of the window; there is no pre/post period and no control arm. Every causal statement here is an observational correction, not an experiment. **This is the #1 process fix, and it belongs *before* the next release, not after.**
2. **The window is 14 days.** D7 is unobservable for 27.5% of the cohort (denominators are stated everywhere). All unsubscribe rates are floors.
3. **Two quiz vocabularies are pooled in one cohort.** `status = "Full-time worker"` (n = 731) churns at **28.5%** while `status = "Full-time employee"` (n = 3,341) churns at **11.8%** — the same concept in different words, from what must be a different funnel or traffic source. Likewise a stray `age = "45+"` bucket (n = 235) alongside `45-54`/`55+`. These cannot be pooled blindly, and someone should find out which funnel variant produces the 28.5% cohort.
4. **The popup carries no challenge identifier,** so "saw the popup" means exposure to any challenge. Since 338 is 99.7% of starts, the practical impact is negligible.
5. **"7-Day Challenge" ships 8 lessons.** Minor, but it means the product's own promise and its content are off by one before anyone even opens it.

---

**→ [Task 2 — the verdict](02-verdict.md)**
