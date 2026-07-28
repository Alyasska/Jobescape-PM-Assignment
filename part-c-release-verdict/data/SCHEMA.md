# BigQuery schema + observed events (dataset `persona-496908.sql_assessment`)

*Captured from INFORMATION_SCHEMA + 20-row samples on 2026-07-27. This is the reference I use to write the real analysis queries.*

## Join key
`user_id` (INT64) links the two tables. `subscribe_events` = 1 row per purchase; `app_events` = product/usage events.

## `subscribe_events` — the purchase + segmentation table
One row per subscription purchase (`event_name = pr_funnel_subscribe`, metadata `event_name:"Purchase"`).
**Segmentation fields (this is what gives us REAL segment sizes — no Drive file needed):**
`age` (18-24…55+) · `gender` · `goal` · `status` (Full-time / Freelancer / Business owner / Student / Exploring…) · `coding_experience` · `subscription` (**1Week / 4Week / 12Week** = the plan) · `subscription_id`.
**Also:** `country_code`, `utm_source/campaign/medium/placement`, `landing/paywall/pricing/quiz_version`, `payment_method`, `cohort_day/week/year`, `personal_plan_pk`, `event_metadata` (JSON, has `email`, `name`, `chase`, upsell/onboarding versions, etc.).

## `app_events` — the product/usage table (Challenge lives here)
**Observed `event_name` values:** `pr_webapp_lesson_started` · `pr_webapp_lesson_completed` · `pr_webapp_lesson_page_click` · `pr_webapp_homepage_view` · `pr_webapp_onboarding_view` · `pr_webapp_challenge_view` · `pr_webapp_lesson_csat_click` · `pr_webapp_lesson_practice_question_view`.  *(An unsubscribe event exists — `unsubscribe_reason`/`unsubscribe_explanation` columns — but its exact `event_name` wasn't in the sample; **find it first** with a `SELECT DISTINCT event_name` query.)*
**Key fields:** `course_id/course_name/course_order` · `module_id/name/order` · `lesson_id/name/order/title` · `personal_plan_id/name` · `csat_score` + `csat_feedback` · `is_correct` · `question_type` · `mechanic_name` · `action` · `status` · `rating` · `unsubscribe_reason/explanation` · `webapp_cohort_day/week/year` · `path` (e.g. `/skills/challenges/338`, `/v2/lessons/623/finish/`).

## How to identify Challenge participation (the crux for Part C)
- **Challenge views:** `event_name = 'pr_webapp_challenge_view'` and/or `path LIKE '/skills/challenges/%'`. Brief's challenge = **338**, but there are many tracks (Excel, Sales, PM, Accounting, Developers, Filmmaking…), each **7 lessons · 15 min/day** (also a 14-day variant).
- **Open question to resolve in query 1:** how a *challenge lesson* is distinguished from a *regular course lesson* — is a challenge its own `course_id`, or flagged by `category_name`/`mechanic_name`, or only by the `/skills/challenges/` path? Run a distinct-values probe before building the tier metrics.

## First queries to run (in order)
1. `SELECT DISTINCT event_name, COUNT(*) FROM app_events GROUP BY 1 ORDER BY 2 DESC` — get the full event list incl. the unsubscribe + any streak/challenge-complete events.
2. Inspect challenge rows: `SELECT * FROM app_events WHERE path LIKE '/skills/challenges/%' OR event_name LIKE '%challenge%' LIMIT 100` — see how challenge participation is logged.
3. Then build: engagement tiers → D1/D3/D7 retention (activity vs challenge-start day) → unsubscribe → lesson completion → CSAT, by segment. (I'll write these once #1–2 confirm the shape.)

## Note vs Part D
The live paywall showed **different prices** than `data/plans.csv` (intro $6.93 / $15.19 / $25.99; recurring $38.95 / $38.95 / $66.65 — a "61% off" variant). Part D uses the *provided* plans.csv as instructed; flag the real dynamic pricing as an observation.
