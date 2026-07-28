# New-chat handoff — read this first

You are continuing an **in-progress Product Manager take-home** for **Nomad Venture Studio / Jobescape**. I'm **Aliaskar** (the candidate). Work with me collaboratively: I do the human-only steps (BigQuery console, the paid product, sending things), you do the analysis, writing, and code.

> ⚠ A previous session's scratchpad does NOT carry over. Everything important lives in this repo — always work from the committed files.

## 1) Read these first (in order)

- `CLAUDE.md` — project context (auto-loaded)
- `BRIEF.md` — the verbatim assignment (source of truth; Parts A–D)
- `README.md` — status board + the thesis
- `deliverable/SUBMISSION.md` — **the compiled answer; this is the deliverable**
- `presentation/OUTLINE.md` — the deck storyboard (the current active task)
- Part answers: `part-a-audience/01-segments.md`, `02-product-gap.md` · `part-b-competitors/01-competitors.md`, `02-analysis.md`, `03-recommendations.md` · `part-c-release-verdict/01-analytics.md`, `02-verdict.md`, `03-whats-next.md` · `part-d-economics/01-ltv-model.md`, `02-ab-test-model.md`
- Part C evidence: `part-c-release-verdict/analysis/` (the scripts that produce every number), `data/SCHEMA.md`, `sql/`

## 2) Where we are — **all four parts are done**

**The thesis:** *Jobescape has built an excellent machine for selling a product it hasn't finished building.* Acquisition is strong, activation was never built, and the economics depend on the retention tail activation would protect. **50.2% of paying subscribers never complete a single lesson.**

- **Part A — done.** Segments sized twice: 39,826 quiz-takers (local compute) and 9,956 buyers (BigQuery). Audience is **~60% aged 45+, 59.7% male**, largest cell **men 55+ (21.3%)**. **Churn falls monotonically with age** (31.1% at 18–24 → 9.5% at 45–54). The income/hustle goals churn at 2.5–3.5× the "work faster / feel confident" core. Gap analysis backed by public reviews **plus my own paid walkthrough**.
- **Part B — done.** Direct/indirect map, teardowns, 5 prioritized steals with the order explained. Includes an explicit reconciliation with Part C on gamification ("take the rhythm, leave the confetti").
- **Part C — done, and it's the centre of the submission.** Verdict: **not a success.** Takers 60.0% D1 vs exposure-matched control 59.6% (**+0.5 pts, p = 0.82**). Reach is 11%. And **v1 never tested its own hypothesis** — no daily gate exists, so 27% of finishers did the whole "7-day" challenge in one sitting. Prototype rebuilt around **the daily gate**, published to the same URL.
- **Part D — done + validated.** Net LTV $60.42 / $123.70 / $162.15, blended $125.06; observed plan mix (10.2/64.6/25.1) reweights to $126.90. A/B break-even 4.9%.
- **Dossier PDF — rebuilt**, 17 pages, `deliverable/Jobescape-Research-Dossier.pdf`.

**Reproducibility:** `cd part-c-release-verdict/analysis && python3 05_qa.py` re-derives **88 documented numbers** straight from the CSVs and fails loudly on any drift. Run it after touching any figure.

## 3) What's left

1. **Build the presentation deck** — the active task. Storyboard is final in `presentation/OUTLINE.md`; pipeline is `presentation/build_slides.py` (SVGs import into Lunacy as editable layers). Slide 7 (the verdict reversal) is the money slide.
2. **Dry-run the demo** out loud once.
3. **Share the prototype artifact** from the page's share menu; confirm it opens logged-out.
4. **Send to @islam_s10** with the CV + dossier PDF (drafts in `00-context/messages-to-islam.md`).
5. **Request the refund — LAST.** Cancelling ends product *and* BigQuery access.

*Optional if a PM conversation happens:* questions are in `00-context/pm-questions.md`; the three that matter most are now listed at the end of `SUBMISSION.md`.

## 4) How we work (important)

- **Division of labour:** I do human-only things (BigQuery console, the paid product, sending). You write complete queries/scripts and do all analysis + writing. **BigQuery flow:** you give me ONE complete query → I run it and "Save results → CSV" into `part-c-release-verdict/data/` → you analyse locally in Python. Keep console instructions dead simple.
- **Be gentle on my laptop.** No heavy commands; stream big files (the quiz CSV is 210 MB). There is no pandas/numpy on this machine — the analysis scripts are pure stdlib on purpose.
- **One small step at a time**, and **explain findings in plain language** — I'm not a hardcore data person.
- **Honesty:** separate *measured* from *estimated*, show calculations, state assumptions. If a previous conclusion turns out wrong, say so and correct it — we already did this twice (the verdict, and the "bot-only cancellation" claim).
- **Language:** I'm Russian-speaking. Plain English is fine for work; some deliverables (like the PM questions) I want in natural Russian.
- Keep `README.md` and this file current.

## 5) Two things a new session gets wrong if nobody says it

1. **The verdict changed on 2026-07-27.** Earlier drafts said "fixable near-miss — the paywall-first funnel means there's no streak to protect on Day 1." The real data says something sharper: the streak mechanic *doesn't exist at all* (no daily gate), reach is 11%, and the effect is zero. Don't reintroduce the old framing — it's in git history and in `research/deep-03`, but it is superseded.
2. **Don't recommend "promote the Challenge to more users" as step one.** CSAT *falls* as engagement rises (3.74 → 3.10). Scaling reach on 3.25-star content scales refunds. The order is instrument → mechanic → first-ten-minutes → quality → **reach last**.
