# Part C · Task 3 — What's Next · Task 4 — Prototype

**Verdict → action.** The Challenge produced no measurable D1 effect, but it also never tested its own hypothesis: it has no daily gate, so there was no habit mechanic to evaluate. The concept is right for this audience — a finite, guided, low-ambiguity path is exactly what a 45+ professional who feels behind at work needs. The build and the placement are wrong.

**Decision: rebuild the mechanic, then re-run it as a real experiment. Do not scale reach yet.**

---

## The reframe

Today the Challenge is a **retention feature** bolted to the side of the product, reached through a popup, taken by 11% of payers.

It should be the product's **activation path**. The evidence:

- **50.2% of paying subscribers never complete a single lesson anywhere.** The product has no on-ramp; people pay and then face an open-ended catalogue.
- The Challenge is already the right *shape* of on-ramp — finite, sequenced, one skill at a time.
- Where it is offered, people want it: **94.6% of everyone who saw the popup clicked it.** Desire is not the constraint.

So the job of v2 is not "make the challenge stickier for the people who take it." It is **"make the challenge the thing that turns a payer into a user."**

## The counter-intuitive part: reach is the LAST fix, not the first

The obvious response to "only 11% see it" is "promote it." That would be a mistake, and the data says why:

**Satisfaction falls as engagement rises** — CSAT 3.74 (never took it) → 3.53 (low) → 3.33 (high) → **3.10 (finished it)**. Challenge content rates **3.25** while the same users rate the rest of the product **3.45**.

Driving 9,000 payers into 3.25-star content would scale complaints, refunds and chargebacks — which are already 11.3% of unsubscribes in this cohort — and Part D shows refund/regulatory exposure is the biggest threat to the economics. **Fix the thing before you point the firehose at it.**

Order of operations: **instrument → first-10-minutes → mechanic → quality → reach.**

> **This order changed after the PM conversation** ([notes](../00-context/pm-conversation.md)).
> I originally put the day gate before the first-ten-minutes fix, because the gate is the untested
> hypothesis. But the team's primary metrics are **gross profit, unsub % 12h/24h, rebill 0→1 and
> 1→2, and LTV** — D1 is explicitly secondary. Fixing the first ten minutes attacks **unsub 12h/24h
> directly**, which is a primary metric and the cheapest item in the plan. The day gate's nearest
> primary-metric effect — surviving to the day-28 rebill decision — is one step further out. So the
> cheap primary-metric fix goes first.

**Which metric each phase is actually for:**

| Phase | Moves | Tier |
|---|---|---|
| 0 · Instrument | Makes "which initiatives win or lose" answerable at all | *enables everything* |
| 1 · First ten minutes | **Unsub % 12h / 24h** → gross profit | **primary** |
| 2 · Mechanic (the day gate) | Survival to the day-28 decision → **rebill 0→1** | **primary**, one step out |
| 3 · Quality | CSAT, session depth | secondary |
| 4 · Reach | Multiplies whatever phases 1–3 achieve | *multiplier* |

The team already ships features to **specific cohorts**, so a hold-out is not new machinery — it is
how they already work. That removes the only real objection to Phase 0.

---

## Phase 0 — Make the next release measurable *(before any feature work)*

The single most expensive thing about v1 is not that it didn't work; it's that **we can't prove whether it did.** 100% rollout, no hold-out, no pre/post. Everything in Task 1 is an observational reconstruction that only worked because a large "looked and left" group happened to exist as a natural control.

| # | Change | Why |
|---|---|---|
| 0.1 | **10–20% hold-out arm** on the next release | The only design that answers the question. Non-negotiable. |
| 0.2 | **Redefine the target metric**: exposure-matched D1 on a common clock | The current definition reports 39.8% vs a 26.0% baseline — a +14pt "win" that is entirely an artifact. |
| 0.3 | Log `challenge_day_unlocked` / `challenge_day_missed` | Without them the daily gate is unmeasurable, which is how v1 got here. |
| 0.4 | Extend the analysis window past the first renewal | A 14-day window structurally cannot see a 4-week subscriber's renewal decision. |

## Phase 1 — Fix the first ten minutes

**45% of the people who press Start complete zero lessons.** That is 499 users in two weeks, at the single highest-intent moment in the feature — they clicked a popup, opened a page, joined, and pressed a button. Nearly half then got nothing.

| # | Change | Moves | Effort |
|---|---|---|---|
| 1.1 | **Find out what happens on that screen first.** Is it a load failure, an auth wall, an app-download step, a long intro? This is a bug hunt before it is a design task. | activation | XS |
| 1.2 | **Guaranteed win inside 10 minutes** on a **pre-loaded** example — the blank page is the enemy for this audience | D1, CSAT | M |
| 1.3 | **Bridge lesson 1 → 2** (a 50% drop): end lesson 1 with tomorrow's task already loaded | D1 | S |

1.1 is the highest expected value in the entire plan, costs an afternoon, and lands on a **primary** metric.

## Phase 2 — Build the mechanic that was missing

| # | Change | Moves | Effort |
|---|---|---|---|
| 2.1 | **Gate the content to one day at a time.** Tomorrow's skill unlocks tomorrow. | **D1**, D3 | S |
| 2.2 | **Wire the reminder channel that already exists to the Challenge** — anchored to a user-chosen time, with escalating D1/D3/D7 copy | **D1** | XS |
| 2.3 | **Name tomorrow as a concrete work task,** not a topic — "Tomorrow: turn a 40-page PDF into a one-page brief" | D1 | XS |
| 2.4 | **Catch-up, not punishment** — a missed day can be recovered the next day without losing progress | D3, unsub | S |

**2.1 is the whole experiment.** Everything else in this document is optional next to it: the hypothesis is that daily pacing builds a return habit, and the shipped feature paced nothing.

> **Most of Phase 2 is already built — it just isn't connected.** Walking the paid product myself
> ([`walkthrough/observations.md`](../part-a-audience/materials/walkthrough/observations.md)), the
> Automation tab already ships an **active WhatsApp agent**, **"Motivational messages"** and
> **"Study progress reminders"**, and both Challenges and Academy already render a **streak counter
> and a Mon–Sun weekly tracker**. The streak displays **0**. So this is not "add a habit system" —
> it is *"connect the habit system you already shipped to the feature that needs it."* That is why
> 1.2 is XS effort rather than S, and it makes Phase 2 a wiring job more than a build.

*The obvious objection — "gating reduces consumption" — is answered by the data:* finishers who binged in ≤2 days unsubscribe at **22.7%**; finishers who spread it over 3+ days unsubscribe at **3.8%** (n = 22 / 26, so directional, not conclusive). Bingeing does not look like the behaviour worth protecting. Guardrail: measure total lesson completions in the test arm and stop if it collapses.

## Phase 3 — Fix what people are actually rating 3.25

| # | Change | Moves | Effort |
|---|---|---|---|
| 3.1 | **Mine the exit-reason and bug events** — `lesson_exit_reason_click` (3,601 events), `lesson_bug_click` (1,295), `lesson_bug_text_submitted` (475). A free qualitative dataset on exactly why people quit, already in the warehouse, unanalysed. | CSAT | XS |
| 3.2 | **Re-aim the framing at the real buyer.** 59.7% male, 58–60% aged 45+, largest single cell men 55+. Competence and dignity, not streaks and confetti: "you will never fear a spreadsheet again," not "🔥 3-day streak!" | CSAT, D3 | S |
| 3.3 | **Make the AI tutor the practice surface** — type your real work task, get a usable draft, save it. This is the one thing free ChatGPT doesn't give this user: scaffolding and a worked example for *their* task. | CSAT, D7 | M |

## Phase 4 — Only now, reach

| # | Change | Gate |
|---|---|---|
| 4.1 | Make the Challenge the **default post-onboarding path** for new subscribers rather than a popup | Ship only once challenge CSAT ≥ 3.45 (the product baseline) |
| 4.2 | Retire the popup as the primary entry point | After 4.1 proves out in the hold-out test |

## What to remove

- **The "7-Day" name on an 8-lesson course.** The promise and the payload are off by one before anyone opens it.
- **The certificate** — 23 downloads across the entire cohort (0.2%). It is not the reward this audience wants, and it costs build and screen space.
- **More gamification.** The audience that responds to it (18–24) churns at 31.1% and is 9% of the book.

## Pre-registered success criteria for v2

Stated before the test so the result can't be reinterpreted afterwards:

| | Metric | Bar |
|---|---|---|
| **Primary** | **Unsub % at 12h / 24h**, test vs hold-out | the metric the business runs on |
| **Primary** | **Rebill 0→1**, test vs hold-out | worth ~$1.31 of blended LTV per point |
| Secondary | Exposure-matched D1 lift | **≥ +5 pts** |
| Secondary | Starters completing ≥1 lesson | 55% → **75%** |
| Secondary | Starters reaching ≥3 lessons | 14% → **30%** |
| **Guardrail** | Challenge CSAT | **≥ 3.45**, must not fall |
| **Guardrail** | Refund / chargeback rate | must not rise |
| **Guardrail** | Total lessons completed per starter | must not fall (gating risk) |

**And the kill rule:** if the daily gate ships with a proper hold-out and still shows no lift, kill the Challenge. The conclusion would then be that this audience does not want a challenge, and the activation problem needs a different shape entirely. Naming that in advance is the point — v1's real failure was being unfalsifiable.

---

# Task 4 — the prototype

**▶ Live link:** *(published below — see `prototype/`)*

A mobile-web prototype of the v2 flow, built to make the **riskiest hypothesis testable before eng commits a sprint**: that daily pacing plus a guaranteed early win converts a payer into a returning user.

**Five screens, each tied to a finding in Task 1:**

| Screen | The finding it answers |
|---|---|
| **1 · Commit** — pick your daily time, echo back the goal from the quiz | 1.2 — there is currently no scheduled return trigger at all |
| **2 · Today** — one unlocked day, tomorrow visibly **locked** with a countdown | 1.1 — the missing daily gate; 27% of finishers binged the whole "7-day" challenge in a day |
| **3 · The win** — pre-loaded real work task → AI draft → save to your library | 2.2 / 3.3 — 45% of starters complete zero lessons; blank page is the enemy |
| **4 · Done for today** — result you can use, named next task, gate closes | 2.3 — half of lesson-1 finishers never open lesson 2 |
| **5 · Tomorrow** — the return trigger firing, and the locked day opening | 1.3 — a concrete reason to come back rather than a badge |

**How it improves the next release.** It turns the v2 from a document into something you can put in front of five 50-year-old professionals on a Tuesday and watch. Specifically it de-risks three decisions that would otherwise be argued in a room: whether the **daily gate reads as helpful or as being locked out of something you paid for** (the one real risk in Phase 1); whether the **pre-loaded first task** produces a genuine "oh, that's useful" inside ten minutes; and whether **competence framing beats streak framing** for a 45+ audience. Each is a copy/UX question that costs a day to test on the prototype and a sprint to discover in production.

*The AI responses are simulated — a sandboxed page can't call a model API. The source marks exactly where a live call drops in. See [`prototype/README.md`](prototype/README.md).*
