# Part C · Task 2 — Verdict

## The verdict

**No. The release was not a success.** On its own stated target metric — D1 retention — the Challenge produced **no measurable effect**. Users who took it retain at 60.0% D1; users who reached the same screen and walked away retain at 59.6% (**+0.5 pts, p = 0.82**). Holding product activity constant, the effect stays at zero in four of five strata. It also did not move unsubscribes (−2.3 pts, p = 0.12).

**But "not a success" is not the same as "the idea is wrong," and the distinction is the whole decision.** v1 never actually tested its own hypothesis:

> *The hypothesis was "one day = one skill builds a habit of returning every day." Nothing in the shipped feature gates content to one lesson per day. 27% of the people who finished the "7-day" challenge finished it in a single day; 46% within two. The mean is 1.46 lessons per active challenge day.*

You cannot fail a daily-habit test with a feature that has no days in it. What shipped was a short course with "7-Day" in the title.

**Decision: do not scale it, do not kill it. Rebuild the mechanic and re-run it as a real experiment.** The sequencing — and why reach is the *last* fix, not the first — is [Task 3](03-whats-next.md).

---

## The number that would have fooled us

This matters more than the verdict itself.

On the team's own definition — *"D1 = retention the day after the challenge started"* — the Challenge posts **39.8% D1** against a product-wide baseline of **26.0%**. That reads as a **+14-point win**, and any dashboard built to the brief's spec would have reported it as one.

It is an artifact of two mistakes stacked on top of each other:

1. **Different clocks.** Takers are measured from the day they started the challenge; everyone else from their first day in the app. Only 24% of takers start on day 0 — the median starts on day +1, and 28% start on day +3 or later. To start on day *k* you must already have survived to day *k*. That survivorship is baked into the metric.
2. **Different populations.** "Everyone else" is 88.8% of the book, two-thirds of whom never even reached a challenge surface. Comparing an opt-in group to a base that includes people who barely opened the app measures who opted in, not what they opted into.

Correct for the first and the gap falls from +38 pts to +17. Correct for the second and it falls to **+0.5 pts**.

**The process lesson is bigger than this feature: the release shipped to 100% with no hold-out.** There is no control arm and no pre/post period anywhere in the data. Everything above is an observational reconstruction of an experiment that should have been run properly the first time — and it only worked because there happened to be a large "looked and left" group to use as a natural control. Next time there may not be.

## The release was scored against a secondary metric

*Added after speaking with a Jobescape PM on 2026-07-28 ([notes](../00-context/pm-conversation.md)).*

The brief names **D1 retention** as the Challenge's target. The team's actual hierarchy is:

| | Metrics |
|---|---|
| **Primary** | Gross profit · unsub % at **12h / 24h** · rebill rate **0→1** and **1→2** · LTV |
| **Secondary** | D1 / D3 / D7 retention · session time · session depth · CSAT |

> *"Gross profit is the first priority; retention is the second."* — and on LTV: *"it's very
> insensitive, it rarely reacts to anything except the obvious."*

**So the feature was scoped against a second-order outcome before a line of it was written.** That is
a resource-allocation finding, not an analytics one, and it makes the verdict firmer rather than
softer: the Challenge missed its stated secondary target **and** shows no effect on the nearest
primary-metric proxy the data allows — unsubscribe, −2.3 pts, p = 0.12.

**What this dataset can and cannot see**, checked rather than assumed:

| Primary metric | Observable here? |
|---|---|
| Gross profit | **No** — no revenue, cost or refund-amount fields in either table |
| Unsub % at 12h / 24h | **Not in my pull** — needs the unsubscribe timestamp; the query is written and ready ([`sql/14_unsub_timing.sql`](sql/14_unsub_timing.sql)) |
| Rebill 0→1, 1→2 | **No** — `pr_webapp_subscription_renewed` fires **17 times** across 9,956 subscribers; a 4-week plan's first rebill lands at day 28, outside the 14-day window |
| LTV | **Modelled, not observed** — and by the team's own read, too insensitive to detect a single feature |
| Unsubscribe, any time in window | **Yes** — and it does not move |

I would rather say that plainly than quietly substitute D1 for gross profit and let the deck imply
I measured the thing that matters.

**And on LTV's insensitivity — here is the size of it,** computed from the company's own plan table
([`ltv_sensitivity.py`](../part-d-economics/model/ltv_sensitivity.py)): a **one-point** gain in
rebill 0→1 moves blended net LTV by **$1.31 (≈1%)**. On a single cohort that is inside the noise —
yet at 1,000 signups a day the same point is worth about **$478,000 a year**. The money is large and
the signal is faint simultaneously. That is the argument for reading a Challenge v2 on **unsub
12h/24h and rebill 0→1**, and using LTV only to price the result afterwards.

## Which metrics I relied on, and how I read them

| Metric | Weight | How I read it |
|---|---|---|
| **D1 retention** (target) | Primary | Right metric, wrong denominator. Only meaningful against an exposure-matched control — which shows no effect. |
| **Unsubscribe** | Primary (economic) | The metric that actually pays. No significant movement at any engagement threshold. Right-censored by the 14-day window, so all values are floors. |
| **D3 / D7** | Supporting | Move with engagement, but circularly — completing lesson 3 on day 3 *is* retention. Treated as descriptive, not evidential. |
| **Lesson completion** | Diagnostic | The most useful thing in the dataset: it locates the failure (55% of starters never finish lesson 1) rather than just sizing it. |
| **CSAT** | Diagnostic, and a red flag | 3.25 for challenge content vs 3.45 for the same users elsewhere, and it *falls* as engagement rises: 3.74 → 3.53 → 3.33 → 3.10 (finishers). |

The decision rule I set before looking: **a real success is a smooth dose-response that survives an exposure-matched comparison.** It failed both. The exposure-matched gap is zero, and the one non-circular dose-response test — among users whose entire challenge activity happened on one day, does a bigger day-0 dose predict returning tomorrow? — comes back **flat-to-negative** (−9.2 pts, p = 0.048).

## Why it turned out this way

Four mechanism-level causes, in order of how much they explain.

### 1. The habit engine was never switched on

The whole theory rests on daily gating: today's skill is available today, tomorrow's tomorrow, and the gap between them is what builds the return habit. The shipped feature has no gate, no scheduled unlock, and no reason to come back tomorrow instead of finishing tonight. So the behaviour it produced is the behaviour you'd predict from an ungated course: people either binge it or abandon it. **Only 36.8% of the starters who completed a lesson ever came back for a second challenge day.**

This is why the honest verdict is "untested," not "disproven."

### 2. It was aimed at the wrong layer of the funnel

The Challenge was built as a **retention** feature. The product's constraint at that moment is **activation**:

- **50.2% of paying subscribers never complete a single lesson anywhere in the product.**
- Mean active days in the product: **1.98**. Cohort D1: 26.0%. D7: 8.6%.
- **89% of payers never start the Challenge**; 67.5% never see a challenge surface at all.

A feature reaching 11% of payers cannot move a company-level metric. Even granting the entire (non-causal) raw gap, the arithmetic ceiling is **+4.3 points of cohort D1**. The real effect is indistinguishable from zero, so the realised contribution is ~0.

### 3. The content doesn't earn the second visit

**45% of the people who press Start complete zero lessons.** That is the moment of highest intent in the entire feature — they clicked a popup, opened the page, joined, and pressed a button — and nearly half get nothing out of it. Then half of those who *do* finish lesson 1 never open lesson 2.

And satisfaction moves the wrong way: the more of this feature someone consumes, the lower they rate the product (3.74 → 3.10). This is the finding that makes "just promote it harder" actively dangerous — **scaling reach on 3.25-star content scales refunds**, and 11.3% of unsubscribes in this cohort are already payment failures, chargebacks or refund disputes.

### 4. The mechanic is designed for an audience Jobescape doesn't have

Streaks, badges and daily challenges are built for the demographic that responds to gamification. Jobescape's buyer is not that person:

- **59.7% of paying subscribers are men; 58–60% are 45 or older.** The single largest cell in the book is **men aged 55+ (21.3%)**.
- **Unsubscribe falls monotonically with age** — 31.1% (18–24) → 9.5% (45–54) → 9.7% (55+). The older majority is the loyal, high-LTV core; the under-25s who respond best to gamified mechanics churn at three times the rate.

A 55-year-old professional who bought this because they feel behind at work is not chasing a streak. They want to stop feeling behind — competence and dignity, not confetti. The v2 has to carry the same *structure* the Challenge provides while changing what it rewards.

*(This is also the one place I'd gently push back on the team's own read of the audience: "40–50-year-old men" is right on gender and understates age by about a decade. Same conclusion, sharper aim.)*

## What would change my mind

I would revise to "success" on any one of these:

- A **hold-out cohort** showing a D1 lift for the exposed arm — the only evidence that settles this properly, and the reason Task 3 leads with instrumentation.
- A **positive dose-response that survives exposure matching**, i.e. the effect I looked for and did not find.
- Evidence that the Challenge's job was never D1 at all — e.g. it was shipped as a **refund-gate or support-deflection** device, in which case it should be judged against refunds and ticket volume, not retention. (Worth asking: the data neither confirms nor refutes it — completion is simply uncorrelated with churn, p = 0.81.)
- A **longer window.** 14 days cannot see a 4-week subscriber's first renewal. If the Challenge's benefit is a 30-day effect, this dataset structurally cannot detect it.

## What this verdict does *not* say

To be fair to the team that shipped it: the concept is sound and the audience needs exactly this kind of structure — a finite, guided, low-ambiguity path is the right shape of product for a 45+ professional who feels behind. The people who *did* reach it converted through the funnel at 94.6% from popup to click, which says the offer is attractive. **The failure is in the build and the placement, not the idea.** That is why the recommendation is a rebuild rather than a kill — and why the first thing to fix is the ability to know whether the next one worked.

---

**→ [Task 3 — what's next + Task 4 — prototype](03-whats-next.md)**
