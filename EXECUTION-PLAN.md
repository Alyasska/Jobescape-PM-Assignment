# Execution Plan — Final TA build (self-paced)

**Situation:** the demo/backbone is done. Now we build the real, *presentable* answer.
**Deliver:** written submission **+** a live presentation.
**Access (all confirmed):** paid product · BigQuery · a Jobescape PM · the 3 Drive folders.

> **STATUS 2026-07-27 (late):** Stages 0–3 are complete. All four parts are final, the dossier PDF is
> rebuilt (17 pp), and every Part C/D figure is asserted by `part-c-release-verdict/analysis/05_qa.py`
> (91 checks, all passing). **What's left is Stage 4 (the deck) and Stage 5 (submit + refund).**
> Note: 3.1/3.2 (the PM conversation) did not happen — the three questions that would have gone to a PM
> are instead stated openly at the end of `deliverable/SUBMISSION.md`, which is a fair substitute.

**Pace:** yours. This is ordered by dependency, not by calendar — do one box, check it, move on.

> **The mindset that kills the overwhelm:** you are never starting from a blank page. Every part already has a complete, defensible answer written. Your job now is to **replace estimates with evidence** and **tighten** — one small box at a time. Don't look at the whole mountain; look at the next box.

---

## Use the backbone (start here every time)

**Nothing gets written from scratch.** Each task = *open the file that already exists → swap the estimate/hypothesis for your captured evidence → keep or sharpen the reasoning → done.* You are **editing, not authoring.**

What's already in place, per part:

| Part | Already written (the backbone) | What "final" adds |
|---|---|---|
| **A** | [`01-segments.md`](part-a-audience/01-segments.md) (6 segments + *estimated* sizing) · [`02-product-gap.md`](part-a-audience/02-product-gap.md) (gap from public reviews) · [`materials/quiz-map.md`](part-a-audience/materials/quiz-map.md) (full quiz decode) | real sizing from Drive data; the gap confirmed with *your own eyes* |
| **B** | [`01-competitors.md`](part-b-competitors/01-competitors.md) · [`02-analysis.md`](part-b-competitors/02-analysis.md) · [`03-recommendations.md`](part-b-competitors/03-recommendations.md) (map + teardowns + prioritized steals) | 2–3 teardowns deepened first-hand (screenshots) |
| **C** | [`01-analytics.md`](part-c-release-verdict/01-analytics.md) (plan + *modeled* expectation) · [`02-verdict.md`](part-c-release-verdict/02-verdict.md) (explicit verdict) · [`03-whats-next.md`](part-c-release-verdict/03-whats-next.md) (v2) · live **prototype** · [`sql/`](part-c-release-verdict/sql/) (queries ready) | real metrics from BigQuery; verdict on actual numbers; v2 matched to the live feature |
| **D** | [`01-ltv-model.md`](part-d-economics/01-ltv-model.md) · [`02-ab-test-model.md`](part-d-economics/02-ab-test-model.md) · [`model/ltv_model.py`](part-d-economics/model/ltv_model.py) | **already final** — just validate assumptions against real churn + the PM |
| **all** | [`research/`](research/) (10 sourced reports) · [`deliverable/SUBMISSION.md`](deliverable/SUBMISSION.md) · the 15-page dossier PDF | fold evidence in, rebuild PDF, add the deck |

So for any task below: the sentence "update `X.md`" always means *upgrade the draft that's already there*, never *write it fresh*.

---

## The ONE rule that must not be broken
**Capture all perishable access before you refund the subscription.** BigQuery + product access die when you cancel, and re-doing it is painful. So Stage 0 (capture) happens *before* Stage 5 (refund), no matter your pace. Screen-record the product; export BQ to CSV; download the Drive files — then analyze from the saved copies.

## Order & dependencies (no dates — just what unlocks what)
`Stage 0 (capture) → unlocks everything` → `Stage 1 (A + C evidence)` → `Stage 2 (verdict, v2, competitors)` → `Stage 3 (PM + synthesis)` → `Stage 4 (presentation)` → `Stage 5 (submit + refund LAST)`.
Two things run in the background from the start: **book the PM early** (their calendar has lead time) and **you** do the human-only capture while **I** run the analysis.

Legend: **[YOU]** only you can do · **[AGENT]** hand to me · **[MUST]** core · **[NICE]** if time.

---

## STAGE 0 — Capture perishable access  *(do first, ~2–3 focused hrs)*

- [ ] **0.1 [YOU][MUST] Book the PM (5 min, first thing).** Depends on someone else's calendar → fire it now. Draft in §PM. Ask for 20–30 min.
- [x] **0.2 [YOU][MUST] Download the 3 Drive folders** → `part-a-audience/materials/` (creatives, quiz-answers) + `part-c-release-verdict/` (events convention). Keep original filenames.
- [x] **0.3 [YOU][MUST] Walk + record the whole journey.** Ad/landing → quiz (take it **twice**, as two different segments, e.g. "anxious catch-up" then "climber") → paywall → **pay** → product → open the **Challenge and do Day 1**. **Screen-record all of it** + screenshot every key screen (paywall, upsells, Challenge home, a lesson, the AI chatbot, the cancel/refund flow). Save to `part-a-audience/materials/walkthrough/`.
- [x] **0.4 [YOU][MUST] Pull BigQuery to CSV.** Run [`sql/00_explore_schema.sql`](part-c-release-verdict/sql/00_explore_schema.sql) → write down the **real table/column/event names**. Then export the Challenge-related `app_events` + `subscribe_events` to CSV → `part-c-release-verdict/data/`. Note row counts.
- [x] **0.5 [YOU→AGENT] Handoff note:** paste the real event/column names + where you saved everything → I adapt the SQL and start.

**Done when:** Drive files in, walkthrough recorded, CSVs on disk, PM meeting requested.

---

## STAGE 1 — Turn estimates into evidence: Part A + Part C data

- [x] **1.1 [AGENT][MUST]** Fix the SQL to the real schema (from 0.5) and dry-run it.
- [x] **1.2 [AGENT][MUST] Real segment sizes** — run [`segment_sizer.py`](part-a-audience/segment_sizer.py) on the real quiz export → replace the estimated ranges in `01-segments.md` with actuals.
- [x] **1.3 [YOU+AGENT][MUST] Real A2 gap** — from your recording: confirm/correct the review-based findings (surprise billing? refund-gating? bot cancel? positioning?) and drop in **your own screenshots**. Upgrade `02-product-gap.md`. *Highest-credibility move: "I paid, walked it, here's what I saw."*
- [ ] **1.4 [AGENT][NICE] Creatives analysis** — what the ads actually promise vs. what the product delivers; tie each to a segment.
- [x] **1.5 [AGENT][MUST] Part C tier analysis on real data** — run the tier + metrics queries → real **D1/D3/D7/unsubscribe/completion by high/low/didn't-take**, calcs shown. Replace the modeled table in `01-analytics.md` with measured numbers.

---

## STAGE 2 — Verdict, v2, prototype, competitors

- [x] **2.1 [YOU+AGENT][MUST] Real verdict** — from the actual D1 number + the dose-response. State success / not plainly, with numbers. Upgrade `02-verdict.md`.
- [x] **2.2 [AGENT][MUST] Refine v2** — adjust the 8 mechanics to what you *actually saw* live (what exists, what's missing). Upgrade `03-whats-next.md`.
- [x] **2.3 [AGENT][NICE] Polish the prototype** — wire the real Claude API call, match the real product's look, redeploy the artifact.
- [ ] **2.4 [YOU+AGENT][NICE] Deepen 2–3 competitor teardowns** first-hand (trial/screenshot Coursiv + one other). Upgrade `part-b-competitors/02-analysis.md`.
- [x] **2.5 [AGENT][MUST] Validate Part D** — cross-check the given C-curve vs. actual retention from BQ; flag the horizon question for the PM.

---

## STAGE 3 — Insider validation + synthesis

- [ ] **3.1 [YOU][MUST] PM conversation** — use §PM. Focus on what BQ *can't* tell you: causal design, success bar, what's been tried, constraints, their own #1 problem.
- [ ] **3.2 [AGENT][MUST] Fold in PM answers** — resolve the Part D horizon; correct anything flagged; **spotlight where an insider confirms a finding you reached independently**.
- [x] **3.3 [AGENT][MUST] Final synthesis + consistency pass** — tighten every part around the one thesis; re-run the number sweep; rebuild the dossier PDF; finalize `SUBMISSION.md`.

---

## STAGE 4 — Build the presentation  *(you chose "Both")*

- [ ] **4.1 [AGENT][MUST] Slide deck** (artifact or PDF): arc = the one thesis → one slide per part, *punchline first*, then evidence. ~10–12 slides.
- [ ] **4.2 [AGENT][MUST] Demo script + talking points** — a 3–4 min prototype walk tied to the verdict + anticipated Q&A ("why not just fix content?", "how confident is the D1 read?", "what ships first?").
- [ ] **4.3 [YOU][MUST] Dry-run once** — present out loud, run the demo end-to-end, fix what's clunky.

---

## STAGE 5 — Submit + refund

- [ ] **5.1 Pre-submit checklist** (in SUBMISSION.md): every sub-question answered; calcs shown; prototype link opens in a private window; CV attached; no BQ password anywhere.
- [ ] **5.2 Send to @islam_s10** + CV + deck/demo link (draft in [`00-context/messages-to-islam.md`](00-context/messages-to-islam.md)).
- [ ] **5.3 Request the refund — LAST**, only after everything is submitted.

---

## §PM — the insider conversation (your scarcest resource)

**Rule:** don't ask what BigQuery can tell you (retention, plan mix — pull those yourself). Ask what only an insider knows. Prioritized:

1. **Was the Challenge a controlled A/B test or a 100% rollout — is there a hold-out cohort?** *(Decides whether any lift is causal or selection — most important for the verdict.)*
2. **What D1 number would the team have called "success"?** *(Judge your verdict against their bar.)*
3. **What have you already tried to lift D1 / early retention?** *(So the v2 is new, not something they killed.)*
4. **What does the team consider the product's #1 problem right now?** *(Aligns your recs with their priorities.)*
5. **Is completion *deliberately* the refund gate, and do you see the billing/refund complaints internally?** *(Sensitive — ask gently.)*
6. **Blended CAC & payback period?** *(Sizes the economics.)*
7. **Which LTV horizon do you model — full curve or 1 calendar year?** *(Resolves the Part D question.)*
8. **Positioning: "AI at work" vs "freelancing income" — intentional or drift?**
9. **Eng/roadmap constraint — what could realistically ship next?**

*Close with:* "Can I reference these in my submission?" + offer to share your findings back.

**Draft booking message:**
> Hi Islam — I'm going deep on the assignment and want to make it genuinely useful, not just correct. Could I grab **20–30 min with a PM** in the next couple of days to sanity-check a few things only someone inside would know (nothing confidential — mostly context on the Challenge release and how you think about success)? I've done my own analysis first, so it'll be tight and specific. Any slot works around your team's availability.

---

## Senior-PM notes
- **Lead with the POV, support with evidence.** One thesis: *fear-sale up front → slow habit product; cash-now vs value-later.* Say it in the first 30 seconds; let every part ladder to it.
- **"I paid and walked it myself" is your credibility multiplier.** Wherever you can say "I saw X in the product," say it.
- **When the insider confirms what you found independently, spotlight it** — that's the "quality of thinking" they grade.
- **Timebox every box.** If one takes 2× its estimate, ship what you have and move on — a complete B+ beats a perfect half (the brief says this outright).
- **Don't over-rely on insider info** — the evaluation is about *your* thinking; use the PM to validate, not to source.
- **Protect the presentation.** With "Both," the deck+demo wins the room — leave real time for Stage 4; don't let analysis eat it.
