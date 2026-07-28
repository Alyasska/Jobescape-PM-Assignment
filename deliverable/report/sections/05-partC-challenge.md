# Part C — The "Challenge" release

The Challenge delivers the course as a **7-day, one-skill-a-day** arc. Target metric: **D1 retention**, with unsubscribe, completion, D3, D7 and CSAT secondary.

**Data:** BigQuery `persona-496908.sql_assessment`, pulled 2026-07-27. **9,956 paying subscribers** whose first app activity falls in 2026-06-12 → 2026-06-25. The feature is `course_id = 338` (*7-Day Claude Challenge*, 6 languages), which accounts for **99.7% of all challenge starts**. Every figure below is reproduced by the scripts in `part-c-release-verdict/analysis/`.

## C.1 — Release analytics

**Engagement tiers, defined explicitly.** High = started and completed **≥3 of the 8** challenge lessons. Low = started, ≤2 lessons. Didn't take it = never started. The cut sits at 3 because that is where the D7 curve steps (18% → 39%), and sweeping every possible threshold shows the retention gap growing monotonically while the unsubscribe gap stays at zero — so the conclusion does not depend on where the line is drawn.

**The exposure ladder — the finding that reframes everything else:**

| Step | Users | % of all payers |
|---|---|---|
| Paying subscribers | 9,956 | 100% |
| … saw the Challenge popup | 3,140 | 31.5% |
| … viewed a Challenge page | 2,109 | 21.2% |
| … **started** Challenge 338 | 1,111 | **11.2%** |
| … completed ≥1 lesson | 612 | 6.1% |
| … completed all 8 | 48 | 0.5% |

**89% of paying subscribers never start it; 67.5% never see a challenge surface at all.** Once someone does see the popup, 94.6% click it — desire is not the constraint, distribution is.

**Inside the feature:** 45% of starters complete zero lessons. Half of those who finish lesson 1 never open lesson 2. Past lesson 3 the drop-off almost stops (survival climbs 51% → 90%).

**The headline comparison** (all groups anchored on their first app day, 95% Wilson intervals):

| Metric | HIGH (n=158) | LOW (n=953) | DIDN'T TAKE (n=8,845) |
|---|---|---|---|
| **D1 (target)** | 69.6% | 58.4% | 21.7% |
| D3 | 57.0% | 34.4% | 10.0% |
| D7 | 39.1% | 18.0% | 6.9% |
| Unsubscribe | 11.4% | 11.4% | 14.3% |
| CSAT | 3.33 | 3.53 | **3.74** |

Read literally this says the Challenge triples D1. It does not.

## C.2 — Verdict: No, the release was not a success

Four tests, and the feature fails all four.

**Exposure-matched control (decisive).** "Didn't take it" is mostly people never offered the feature. The fair control is people who reached the Challenge and declined it:

| Group | n | D1 |
|---|---|---|
| Started 338 | 1,111 | **60.0%** |
| Joined 338, never started | 230 | **60.4%** |
| Viewed 338, never joined | 764 | **59.3%** |

**Takers vs exposed-but-didn't-start: +0.5 pts, p = 0.82.** Holding total product activity constant, the effect stays at zero in four of five strata. Unsubscribe: −2.3 pts, p = 0.12, not significant.

**Immortal-time bias.** Only 24% of takers start on their first app day; the median starts on day +1 and 28% on day +3 or later. To start on day *k* you must already have survived to day *k*. Correcting for this alone cuts the apparent gap from +38 pts to +17.

**A non-tautological dose-response.** Among takers whose entire challenge activity happened on one day, a bigger day-0 dose predicts **worse** next-day retention (−9.2 pts, p = 0.048). Not flat — negative.

**The mechanic was never built.** The hypothesis needs daily gating. Nothing gates the content. **27% of the people who completed the "7-day" challenge did it in a single day; 46% within two.** Mean 1.46 lessons per active challenge day. Only 36.8% of starters who completed a lesson ever returned for a second challenge day.

> **v1 did not fail the hypothesis — it never tested it.** What shipped was a short course with "7-Day" in the title.

**The number that would have fooled the team.** On the brief's own metric definition — D1 measured from the challenge start day — the Challenge posts **39.8%** against a product baseline of **26.0%**. Any dashboard built to spec reports a +14-point win. It is an artifact of two different clocks and two different populations. And there is no hold-out anywhere in the data: the release went to 100% with no control arm, so everything above is an observational reconstruction that only worked because a large "looked and left" group happened to exist.

**A red flag that changes the recommendation:** satisfaction falls as engagement rises — 3.74 (never took it) → 3.53 → 3.33 → **3.10 (finished it)**. Challenge content rates 3.25 while the same users rate the rest of the product 3.45.

## C.3 — What's next: rebuild the mechanic, then run a real experiment

**The reframe.** The Challenge is treated as a retention feature. It should be the product's **activation path** — because **50.2% of paying subscribers never complete a single lesson anywhere**, and a finite, sequenced, one-thing-at-a-time path is exactly the right shape of on-ramp for a 45+ professional.

**The counter-intuitive call: reach is the LAST fix, not the first.** The obvious response to 11% reach is to promote it. But satisfaction falls with engagement, so scaling reach on 3.25-star content scales refunds — already 11.3% of unsubscribes are payment failures, chargebacks or disputes. Order: **instrument → mechanic → first ten minutes → quality → reach.**

| Phase | The work |
|---|---|
| **0 · Instrument** | 10–20% hold-out; redefine D1 as exposure-matched on a common clock; log day-unlock events; extend the window past first renewal |
| **1 · Mechanic** | **Gate the content to one day at a time** — this *is* the experiment. Plus a scheduled trigger at a user-chosen time, tomorrow named as a concrete task, and catch-up rather than punishment |
| **2 · First 10 min** | Find out what happens to the 45% who press Start and complete nothing (a bug hunt before a design task); guarantee a win inside 10 minutes on a pre-loaded example; bridge lesson 1 → 2 |
| **3 · Quality** | Mine the 3,601 exit-reason and 1,295 bug events already in the warehouse; re-aim framing at the real buyer — competence, not confetti |
| **4 · Reach** | Make it the default post-onboarding path — gated on CSAT reaching the 3.45 product baseline |

**Remove:** the "7-Day" name on an 8-lesson course; the certificate (23 downloads, 0.2%); any further gamification — the segment that responds to it is 9% of buyers and churns at 31%.

**Pre-registered bar:** exposure-matched D1 lift **≥ +5 pts** vs hold-out; starters completing ≥1 lesson 55% → 75%; guardrails on CSAT, refunds and total completions. Kill rule: if the daily gate ships with a proper hold-out and still shows no lift, kill the Challenge — the conclusion would be that this audience doesn't want a challenge, and activation needs a different shape.

## C.4 — Prototype (Task 4)

**Live:** https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/

A working React application built in Jobescape's own design system, so it reads as a feature of the product rather than a mockup of one. Five steps, each with its own URL and each annotated on the page with the finding that produced it: **Commit** (pick the daily time) → **Today** (one day open, tomorrow locked with a live countdown) → **The win** (pre-loaded real task → drafted result → save it) → **Done** (a kept result; tomorrow named as a work task) → **Tomorrow** (the reminder fires, the gate opens). State persists, so the gate survives a refresh — a gate that resets is not a gate.

It borrows Jobescape's **visual language** — the blue, the rounded cards, the staggered lesson path — but not its **streak mechanic**. The buyer is 59.7% male and ~60% aged 45+, and the under-25s who respond best to streaks unsubscribe at 31.1%; the slot where the product's streak pill sits now counts the days the product has opened for you. The reward is competence, not celebration. The visual argument is part of the product argument.

**How it improves the next release:** it turns the plan into something you can put in front of five 50-year-old professionals on a Tuesday and watch. It de-risks the three decisions that would otherwise be argued in a room — whether a locked day reads as helpful or as being shut out of something you paid for (the one real risk in Phase 1), whether the pre-loaded first task produces a genuine "that's useful" inside ten minutes, and whether competence framing beats streak framing for this audience. Each costs a day to test on the prototype and a sprint to discover in production.
