# Part D · Task 2 — A/B Plan-Upgrade break-even

**Question:** In the test group, a **4-week** subscriber is shown a **Plan Upgrade to 12-week** ($49.99 one-time) **instead of the second upsell**. An upgrade buyer is billed under 12-week economics from then on. At what upgrade-conversion does the test beat control, and should we run it?

**Answer up front:** Break-even upgrade conversion is **≈ 8.3%** on a like-for-like one-year horizon. A low bar for a checkout offer → **yes, run the test.** (Applying all 12 supplied transitions to both plans gives 4.9%, but that reading is not like-for-like — see below.)

---

## What changes between control and test (4-week buyers only)

| Component | Control | Test |
|---|---|---|
| 4-week intro ($19.99) | ✅ | ✅ (unchanged) |
| First upsell (30% × $69.99) | ✅ | ✅ (unchanged) |
| Second upsell (12% × $29.99 = $3.60) | ✅ | ❌ **replaced** |
| Plan Upgrade ($49.99, one-time) | — | ✅ taken by fraction *p* |
| Recurring stream | 4-week ($39.99 curve) | *p* switch to **12-week** ($62.99 curve); (1−*p*) stay 4-week |

Intro and first upsell are identical in both arms, so they cancel in the comparison. Because the 12% fee is uniform, it also cancels — **break-even is identical gross or net.**

## The break-even formula

Setting test LTV = control LTV and cancelling the common terms:

```
p* · (UpgradePrice + RecRev₁₂ − RecRev₄) = E[2nd upsell]₄
p* = 3.60 / (49.99 + RecRev₁₂ − RecRev₄)
```

Each upgrade **adds** the $49.99 surcharge plus the *difference* between a 12-week and a 4-week recurring stream, and **cannibalises** only the $3.60 expected second upsell.

## Why the horizon has to match

The two plans bill at different rhythms, so "12 transitions" means different amounts of *time*:

| | charges | first → last charge | calendar span |
|---|---|---|---|
| 4-week plan, 12 recurring | 12 | week 4 → week 52 | **exactly one year** |
| 12-week plan, 12 recurring | 12 | week 12 → week 156 | **three years** |

So applying the full curve to both arms hands the test group **156 weeks of revenue and the control
52**. That is not a like-for-like comparison, and it is the same mistake Part C is about: two groups
measured on different clocks. Within one year the 12-week plan bills **four** times, not twelve.

| Reading | 4-wk recurring | 12-wk recurring | Δ | Gain/upgrade | **Break-even** |
|---|---|---|---|---|---|
| Full curve (unequal horizons) | $95.98 | $119.67 | +$23.69 | $73.68 | 4.88% |
| **One year, both arms** | **$95.98** | **$89.43** | **−$6.55** | **$43.44** | **8.29%** |

**The honest number is 8.29%.**

Test-arm net LTV per 4-week buyer, on the one-year horizon (control = $123.70):

| Upgrade take-rate | Test net LTV | vs control |
|---|---|---|
| 0% | $120.53 | −$3.17 — the cost of the swap if nobody upgrades |
| 8.3% | $123.70 | break-even |
| 15% | $126.27 | +2.1% |
| 30% | $132.00 | +6.7% |

## What the corrected number actually means

Inside one year the recurring delta is **negative** (−$6.55): a 12-week subscriber bills four times
against the 4-week plan's twelve. So the upgrade is **not** "a richer recurring stream" — it is a
**cash-forward trade**. You collect $49.99 today and give up a little recurring revenue this year,
in exchange for a subscriber on a plan that churns less and is worth more beyond the horizon.

That reframing matters for how you read the test: judge it on **cash collected and retention**, not
on first-year recurring revenue, which the upgrade slightly reduces by construction.

## Recommendation

**Run the test.** The downside is tiny and bounded: the only thing at risk is the $3.60 expected second upsell per 4-week buyer, and only for the test arm. The upside is a permanent **mix shift toward the highest-LTV plan** ($162 vs $124 net). Break-even sits at **~8%** upgrade conversion on a like-for-like horizon — well within what checkout upgrade offers typically achieve.

**How I'd run it & de-risk:**
1. Size the test for the target metric = **upgrade take-rate**, with net-LTV-per-4-week-buyer as the readout. Need enough 4-week buyers to detect a ~5% take-rate with confidence.
2. **Watch second-order effects the point model ignores:** (a) does adding an upgrade step depress overall checkout completion / first-upsell take? (b) do upgraded users **churn faster** because they were pushed into a bigger commitment (higher refund/chargeback risk)? Track early-period retention and refunds on upgraded cohorts, not just the day-0 take-rate.
3. Because break-even is so low, the real question isn't "will it pay off at a given conversion" but "does the upgrade **cannibalise something more valuable** (checkout completion, refunds)" — that's what the live test, not the spreadsheet, has to answer.

Model & scenarios: [`model/ltv_model.py`](model/ltv_model.py).
