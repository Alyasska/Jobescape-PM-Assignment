# CLAUDE.md — context for AI agents working in this repo

You are helping **Aliaskar Bekishev** complete a **Product Manager take-home** for **Nomad Venture
Studio (Jobescape)**. Deadline **2026-07-28 23:59**. This is a hiring evaluation — the bar is
**quality of thinking**, not volume or visual polish.

## Read first
1. `BRIEF.md` — the verbatim assignment (source of truth; answer it literally, don't restate it).
2. `README.md` — status board + how the work is split.
3. `ORCHESTRATION.md` — the AI-agent plan (which agent does what, dependencies, order).
4. `00-context/` — company notes, external inputs manifest, credentials (gitignored).

## Folder map
- `part-a-audience/` — segments + product expectation-vs-reality gap. Needs Drive materials + a paid product walkthrough.
- `part-b-competitors/` — find/analyze competitors + prioritized "what to take". Mostly web research.
- `part-c-release-verdict/` — analyze the "Challenge" feature from BigQuery, give a verdict, propose v2, **build a working prototype** (`prototype/`).
- `part-d-economics/` — cohort LTV model (Task 1) + A/B plan-upgrade break-even (Task 2). Data in `data/plans.csv`. Self-contained — start here to build momentum.
- `deliverable/` — the final compiled submission + CV to attach.
- Each part has a **`PLAN.md`** — a ready-to-use agent brief for that part. When spawning a subagent, point it at its part's `PLAN.md` + `BRIEF.md`.

## Working conventions
- **Every claim is defensible.** Show calculations (Part C/D). State assumptions explicitly where the brief is silent — a labeled assumption is fine; a hidden one is not.
- **Numbers before opinions** in Part C/D. Pull/derive the metric, then interpret.
- Answers are Markdown in each part's numbered files (`01-*.md`, `02-*.md`, ...). Keep them tight and structured — a reviewer skims.
- Don't invent data. If an input is missing (e.g. Drive materials not downloaded, BQ not pulled), write `> ⚠ BLOCKED: needs <input>` and continue with what's available.
- Secrets live only in `00-context/credentials.md` (gitignored). Never paste the BQ password into committed files or the submission.
- **On-brand angle:** Jobescape sells "use AI at work." Using AI agents to do this assignment well is a feature, not a cheat — note it in the final submission.

## Definition of done (per part)
- A → segments table + gap analysis, each tied to evidence from creatives/quiz/product.
- B → competitor table (direct/indirect + why) + per-competitor teardown + prioritized recommendations with rationale for the order.
- C → engagement-cohort metrics with SQL/calcs shown, a clear yes/no verdict with reasoning, a v2 plan, and a **live prototype link**.
- D → LTV per plan (gross+net) + blended, with the model shown; A/B break-even conversion + a recommendation.
