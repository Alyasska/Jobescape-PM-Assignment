# Nomad Venture Studio — PM Test Assignment

Workspace for Aliaskar's Product Manager take-home for **NVS / Jobescape**.
**Deadline: 2026-07-28 23:59** · Submit to Telegram **@islam_s10** (+ attach CV).

- **What to do:** `BRIEF.md` (verbatim assignment — the source of truth).
- **The compiled answer:** `deliverable/SUBMISSION.md`.
- **Context for any AI session:** `CLAUDE.md` · new-chat onboarding: `00-context/HANDOFF.md`.
- **Secrets:** `00-context/credentials.md` (gitignored) — never in a committed file.


> **Note on the brief.** The assignment text itself is deliberately not published here — it is
> Nomad Venture Studio's hiring material, not mine to put on the internet. The eleven tasks it
> sets are named throughout, and the compiled answer is in
> [`Aliaskar-Bekishev-PM-Assignment/`](Aliaskar-Bekishev-PM-Assignment/).


## The thesis

> **Jobescape has built an excellent machine for selling a product it hasn't finished building.**
> Acquisition is strong; *activation* was never built; the economics depend entirely on the retention
> tail that activation would protect. The measured fact underneath it: **50.2% of paying subscribers
> never complete a single lesson.**

## The four parts

| Part | What | Folder | Status |
|------|------|--------|--------|
| **A** | Audience segments + product expectation-gap | `part-a-audience/` | ✅ **done** — 6 segments sized on 39,826 quiz-takers *and* 9,956 buyers; gap evidenced by public reviews + my own paid walkthrough |
| **B** | Competitor analysis + what to take | `part-b-competitors/` | ✅ **done** — direct/indirect map + teardowns + 5 prioritized steals with the order explained |
| **C** | Challenge: analytics → verdict → v2 → prototype | `part-c-release-verdict/` | ✅ **done** — real BigQuery analysis, explicit verdict (**not a success**), v2 plan, **live prototype** |
| **D** | LTV model + A/B plan-upgrade break-even | `part-d-economics/` | ✅ **done** — model + writeups, validated against the real cohort |
| — | Research dossier (PDF) | `deliverable/Jobescape-Research-Dossier.pdf` | ✅ **rebuilt** (17 pp) |
| — | Final compiled answer + CV | `deliverable/SUBMISSION.md` | ✅ **ready to send** |
| — | Presentation deck | `presentation/` | ✅ **built** — 41 slides, task-by-task, one self-contained HTML file + speaker report |
| — | Appendix | `deliverable/appendix/` | ✅ **generated** — analysis output, SQL, 91-check verification |

## Part C headline (the centre of gravity)

| | |
|---|---|
| Cohort | **9,956 paying subscribers**, 2026-06-12 → 2026-06-25 |
| Reach | **89%** never start the Challenge; **67.5%** never see a challenge surface |
| Target metric | takers **60.0%** D1 vs exposure-matched control **59.6%** → **+0.5 pts, p = 0.82** |
| The mechanic | no daily gate — **27%** of finishers did the whole "7-day" challenge in one sitting |
| Verdict | **Not a success.** But v1 never tested its own hypothesis → rebuild, then run it as a real experiment |

All figures reproduce from `part-c-release-verdict/analysis/` — and
**`05_qa.py` asserts all 91 of them against the source CSVs.**

```bash
cd part-c-release-verdict/analysis
python3 02_main.py        # the full Task-1 analysis
python3 05_qa.py          # verifies every documented number still matches the data
```

## Remaining human-only steps

- [ ] Share the prototype artifact (page share menu) → confirm it opens logged-out
- [ ] Dry-run the presentation once, out loud, with the demo
- [ ] Send to **@islam_s10** with CV + dossier PDF
- [ ] **Request the $15.19 refund — LAST** (it ends product + BigQuery access)

## Progress log

- **2026-07-27 (late)** — Real Part C landed. Pulled the comparison-group export (query 13) covering all 9,956 paying subscribers; built a reproducible analysis suite (`analysis/`, 6 scripts, 91 assertions). Verdict flipped from "fixable near-miss" to **"not a success — and it never tested its own hypothesis."** Rewrote Part C in full, rebuilt the prototype around the daily gate, folded buyer demographics into Part A, validated Part D against the real plan mix, corrected an overclaim about cancellation, rebuilt the PDF.
- **2026-07-27** — BigQuery access + schema captured; quiz export computed locally (39,826 takers); paid-product walkthrough screenshotted.
- **2026-07-24 (eve)** — Full autonomous pass: quiz funnel decoded, Part D done, 10 research reports → PDF dossier, first drafts of A/B/C, first prototype.
- **2026-07-24** — Environment scaffolded, brief extracted, product purchased for access.
