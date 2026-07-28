# Appendix — the working behind the answer

Everything here is **generated output**, not hand-written prose. If any figure in the submission, the
dossier or the deck is ever questioned, the answer is in one of these files — and all of it can be
regenerated from the source CSVs in one command.

```bash
cd part-c-release-verdict/analysis
python3 05_qa.py          # re-derives all 91 published figures and fails loudly on any drift
```

## Contents

| File | What's in it | Answers |
|---|---|---|
| [`05_qa-output.txt`](05_qa-output.txt) | **91 assertions**, each computed from the raw CSV and checked against the published figure | *"Is this number real?"* — start here |
| [`02_main-output.txt`](02_main-output.txt) | The full Part C Task-1 analysis: exposure ladder, tier calibration, the headline comparison with confidence intervals, all four causal tests, threshold-robustness sweep, and every segment cut | *"Show your calculations"* |
| [`03_supplement-output.txt`](03_supplement-output.txt) | Target-metric definitions side by side, the CSAT inversion, the refund-gate test, the popup-decliner group, data-quality flags, and the economic sizing of the feature | *"What else did you check?"* |
| [`04_loose_ends-output.txt`](04_loose_ends-output.txt) | Cohort baselines, the confound check on exposure, the **stratified takers-vs-control comparison**, challenge-start dates, and the plan-mix validation against Part D | *"Is the effect just activity level?"* |
| [`01_diagnostics-output.txt`](01_diagnostics-output.txt) | The questions settled *before* the engagement tiers were chosen: challenge-start lag, the 8-lesson structure, dose-response by both measures, censoring, and coverage of course 338 | *"How did you pick the cut?"* |
| [`sql/`](sql/) | All 8 BigQuery queries — see the table below for which produced data | *"How did you pull it?"* |

## The queries, and which ones are load-bearing

`00` probes the real schema; `01`–`03` were written **before** it was known, against assumed column
names, and were superseded rather than run — they are kept because they are the actual working, and
they still carry their `⚠ADJUST` markers. Five queries produced every CSV the analysis reads.

| Query | Ran | Produced |
|---|---|---|
| `00_explore_schema.sql` | ✅ | 95 rows — the real column list for both tables |
| `01_engagement_tiers.sql` | — | superseded draft (assumed schema) |
| `02_core_metrics.sql` | — | superseded draft (assumed schema) |
| `03_segment_breakdown.sql` | — | superseded draft (assumed schema) |
| `10_explore_events.sql` | ✅ | the 67-event catalogue, event×course counts, unsubscribe-reason counts, row samples |
| `11_challenge_funnel.sql` | ✅ | 1 row — the whole-cohort funnel counts |
| `12_challenge338_user_table.sql` | ✅ | **1,111 rows** — one per challenge-338 starter |
| `13_comparison_groups.sql` | ✅ | **9,956 rows** — one per paying subscriber. The analysis dataset |
| `14_unsub_timing.sql` | not run | would make unsub % at 12h/24h reportable |

## The three numbers most likely to be challenged

| Claim | Where to find it | Test |
|---|---|---|
| The Challenge moved D1 by **+0.5 pts, p = 0.82** | `02_main-output.txt` §4 Test A | Two-proportion z-test, takers (n=1,111) vs exposure-matched control (n=994) |
| The effect is **not** an activity artefact | `04_loose_ends-output.txt` | Stratified by product activity — flat in 4 of 5 strata |
| **27%** of finishers completed it in one sitting | `02_main-output.txt` §5 | 13 of 48 finishers have `active_challenge_days = 1` |

## Method notes

- **Confidence intervals** are Wilson score intervals, not normal-approximation — several cells are
  small and several proportions sit near 0 or 1, where the normal approximation returns impossible
  bounds.
- **Group comparisons** are two-proportion z-tests with a pooled-variance standard error, reported
  as difference, z and p rather than as a bare "significant".
- **Censoring** is handled with explicit restricted denominators, stated on every table. The
  observation window is 14 days (2026-06-12 → 2026-06-25), so D7 is only observable for 72.5% of the
  cohort and **every unsubscribe rate is a floor**.
- **No regression, no model.** With no hold-out group in the data, the honest tool is a natural
  control — people who reached the same surface and declined it. Simpler than a model, and it does
  not hide its assumptions inside coefficients.
- The analysis scripts are **pure Python standard library** (no pandas or numpy on the machine they
  were written on), so they run anywhere with Python 3 and the two CSVs.

## What this appendix cannot tell you

Whether the Challenge was *causal*. There is no hold-out group and no pre/post period anywhere in the
warehouse — the release shipped to 100%. Every causal statement in the submission is an observational
correction that worked only because a large "looked at it and left" group happened to exist as a
natural control. Fixing that is the first recommendation in Part C, not the last.
