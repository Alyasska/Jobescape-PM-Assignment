# Part C — Release Verdict (Challenge feature) · agent brief

**Roles:** Data Analyst (T1) → Verdict Writer (T2–T3) → Prototype Builder (T4).
**Blocked on:** H3 (BigQuery exports → `data/`) and the Events Convention doc + a live walkthrough of
the Challenge. Read `../BRIEF.md` Part C. The feature: 7-day challenge, 1 AI skill/day, meant to build a
daily-return habit → lift first-week retention & cut unsubscribes. **Target = D1 Retention.**

## Getting the data (H3)
- BQ console + creds in `../00-context/credentials.md`. Tables: `app_events`, `subscribe_events`.
- First read the **Events Convention** doc to learn event names / user props (age, profession, etc.).
- Pull exports to `data/` (gitignored). Suggested pulls: challenge start/day-complete/lesson events,
  subscription + unsubscribe events, user attributes. Save the SQL in `sql/`. It's **not an SQL test** —
  use Python/AI freely; what's judged is the questions asked and conclusions drawn.

## Task 1 — Release analytics → `01-analytics.md` (+ `sql/`)
- Define **engagement tiers** yourself and justify the cutoffs: e.g. **high** = completed ≥5/7 days,
  **low** = started but ≤2 days, **didn't take it** = eligible but never started. State the denominator.
- Compute for each tier: **D1 (target)**, plus D3, D7 retention, **unsubscribe rate**, lesson completion,
  CSAT if available. Show the counts and the formula for each metric (**show calculations**).
- Segment cuts: by **age, profession**, and any strong axis from the events. Look for who the challenge
  works/doesn't work for.
- ⚠ Watch **selection bias:** high-engagers are more retentive by disposition. Note it; where possible
  compare challenge-takers vs a comparable non-taker baseline rather than claiming pure causation.

## Task 2 — Verdict → `02-verdict.md`
- Clear **success / not** call. Which metrics you relied on and **how you interpret** them (lead with D1).
- **Why** the result came out this way — tie it to the feature mechanics (daily cadence, 7-day length,
  skill-per-day relevance) and to observed user behavior (drop-off day, who churns).

## Task 3 — What's next → `03-whats-next.md`
- If it worked → a concrete **v2** (specific mechanics to strengthen the habit — reminders, streaks,
  personalization by profession, shorter/relevant days, social proof). If inconclusive/failed → the
  specific changes to make it work. Pick ONE focused bet to prototype.

## Task 4 — Prototype → `prototype/` + live link
- Vibe-code the core flow of your Task-3 bet (Claude Code / v0 / Lovable / Replit). Working > pretty.
- Must show the **essence + core flow** end-to-end. Deploy to a live URL (Vercel/Netlify/tool's host).
- In `03-whats-next.md` (or a `prototype/README.md`), explain **exactly how** it improves the challenge
  in the next release, and put the **link** there and in `deliverable/SUBMISSION.md`.

## Quality bar
- Every metric shows its calculation and denominator. Verdict is unambiguous. Prototype link actually loads.
- Have a second agent independently recompute D1/D3/D7 for the tiers and reconcile before the verdict is final.
