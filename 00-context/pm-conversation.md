# PM conversation — Nomad Venture Studio

*Spoken with a Jobescape PM, 2026-07-28. Recorded verbatim where quoted, then translated. This is
now a **source** for Part C — the metric hierarchy below overrides the brief's framing of what
"success" means.*

## What they said

1. **The Challenge is rolled out to a specific cohort**, and the job is to evaluate *which
   initiatives win and which lose*.
2. **Resource management** is the frame: there are business initiatives and there are retention
   initiatives, and they compete for the same engineering capacity.
3. **"Gross profit is the first priority; retention is the second priority."**
4. The metric hierarchy, verbatim:

   > **главные метрики** — gross profit, unsub % 12h/24h (косвенно улучшает gross profit),
   > Rebill rate period 0 to 1, 1 to 2
   >
   > **второстепенные метрики** — D1, D3, D7 retention, Session time, Session depth, CSAT

   **Primary:** gross profit · unsub % at 12h / 24h (which indirectly improves gross profit) ·
   rebill rate period 0→1 and 1→2.
   **Secondary:** D1 / D3 / D7 retention · session time · session depth · CSAT.

5. **"If your mechanic can improve the primary metrics, that's ideal. If not, better to aim at the
   secondary ones."**

## Why this matters for the answer

**The brief names D1 retention as the Challenge's target metric. By the company's own hierarchy, D1
is a secondary metric.** So the release was scoped against a second-order outcome from the start.
That is a resource-allocation finding, not just an analytics one, and it reframes Part C:

- It makes the verdict **stronger, not weaker**. The Challenge missed its stated (secondary) target,
  *and* shows no effect on the nearest primary-metric proxy the data allows me to observe
  (unsubscribe: −2.3 pts, p = 0.12).
- It **re-orders the v2 plan.** Fixing the first ten minutes attacks **unsub 12h/24h** — a *primary*
  metric — and is the cheapest item in the plan. It should therefore come before the day gate, whose
  nearest primary-metric effect (rebill 0→1) is one step removed. See
  [`../part-c-release-verdict/03-whats-next.md`](../part-c-release-verdict/03-whats-next.md).
- The **cohort rollout removes the main objection to a hold-out.** They already ship to specific
  cohorts, so holding one back is how they already work — not new machinery.

## What the assignment dataset cannot tell me

Checked directly against the data, not assumed:

| Primary metric | Observable in the provided data? |
|---|---|
| Gross profit | **No** — no revenue, cost or refund-amount fields in either table |
| Unsub % at 12h / 24h | **Not in my export** — needs the unsubscribe timestamp; one query away, written as [`sql/14_unsub_timing.sql`](../part-c-release-verdict/sql/14_unsub_timing.sql) |
| Rebill rate 0→1, 1→2 | **No** — `pr_webapp_subscription_renewed` fires **17 times** across 9,956 subscribers. A 4-week plan's first rebill lands at day 28, outside the 14-day window entirely |
| Unsubscribe (any time in window) | **Yes** — and it does not move: −2.3 pts, p = 0.12 |

**So the honest position:** the dataset supplied for this assignment can evaluate the *secondary*
metrics well and the *primary* ones barely at all. I say that on the slide rather than quietly
substituting D1 for gross profit and hoping nobody notices.

## Not asked, still open

- What gross-profit delta would have made the Challenge worth its build cost?
- Is the 12h/24h unsub window measured from purchase or from first app open? (Changes the mechanic.)
- Which cohort was the Challenge rolled out to, and was anything held back?
