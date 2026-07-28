# Part D — Subscription Economics · agent brief

**Role:** LTV Modeler. **Blocked on:** nothing — data is in `data/plans.csv`. **Start here.**
Read `../BRIEF.md` Part D for the exact wording. Answer literally. **Show every calculation.**

## Task 1 — Total Net LTV (1-year horizon, one cohort)
Build a per-plan cohort model, then blend.

Mechanics to model (per plan, per 100 subscribers or per 1 subscriber — pick one, state it):
1. **Subscription revenue** = intro payment + recurring payments across periods, each period weighted
   by cumulative survival. Survival to period *n* = C01·C12·C23·…·C(n-1)(n). The **Cmn** notes:
   C01 = intro→period1 conversion; C12 = period1→period2, etc.
2. **Horizon = 1 year = 52 weeks.** Convert each plan's periods to weeks:
   - 1-week plan: intro 1wk then 4-week recurring cycles → count cycles until 52 weeks.
   - 4-week plan: intro 4wk + 4-week recurring cycles → ~13 periods in 52 weeks.
   - 12-week plan: intro 12wk + 12-week recurring cycles → ~4-ish periods in 52 weeks.
   - **State your period-count assumption explicitly** (the brief gives C-values up to C1112, i.e. 12 transitions — decide how that maps to 52 weeks and justify it).
3. **Upsells** = one-time at checkout: `conv_rate × price` for first and second upsell, added once.
4. **Gross LTV** = subscription + upsells (before fees). **Net LTV** = Gross × (1 − 0.12) payment fee.
   (Decide whether the 12% applies to upsells too — it's a payment-provider fee, so yes; state it.)
5. **Blended Net LTV** = Σ (plan mix % × plan Net LTV) using 10/70/20.

Deliverables:
- `model/ltv.py` (or a spreadsheet) that computes everything from `data/plans.csv`.
- `01-ltv-model.md`: a table of Gross & Net LTV per plan + Blended Net LTV, the period→week mapping,
  every assumption labeled, and a short read of which plan is most valuable and why.

## Task 2 — A/B test: Plan Upgrade instead of 2nd upsell (4-week group)
- **Control** = Task 1 result (baseline Blended Net LTV, and the 4-week plan's Net LTV).
- **Test group:** the 4-week subscriber is offered a **$49.99 one-time Plan Upgrade** *instead of* the
  2nd upsell. If they take it (`p` = upgrade purchase conversion), they pay $49.99 once AND become a
  **12-week subscriber** → their remaining lifetime is billed under 12-week economics. If they decline,
  they stay a 4-week subscriber but **lose the 2nd upsell** (it was replaced by the offer).
- Model **test-group 4-week-cohort LTV as a function of `p`**: 
  `LTV_test(p) = (1−p)·[4wk LTV without 2nd upsell] + p·[$49.99·(1−fee) + 12wk-from-here LTV]`.
  Be careful what "12wk-from-here" means: they already paid the 4-week intro, then upgrade — model
  their forward economics as a 12-week subscriber and state the timing assumption.
- **Break-even:** solve for `p*` where blended (or 4-week-segment) Test LTV = Control LTV.
- Run scenarios (e.g. p = 5/10/20/30%) → table. **Recommend** run/don't-run based on how plausible p* is.

Deliverables: `model/ab_test.py`, `02-ab-test-model.md` (scenario table, break-even `p*`, recommendation).

## Sanity checks before you hand off
- Net = Gross × 0.88 everywhere. Survival is monotonically decreasing. Blended sits between plan LTVs.
- 12-week plan should have the highest per-subscriber LTV (higher price, but check retention drag).
- Have a second agent re-derive Blended Net LTV independently and compare.
