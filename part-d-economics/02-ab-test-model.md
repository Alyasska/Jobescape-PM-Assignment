# Part D · Task 2 — A/B Plan-Upgrade break-even

**Question:** In the test group, a **4-week** subscriber is shown a **Plan Upgrade to 12-week** ($49.99 one-time) **instead of the second upsell**. An upgrade buyer is billed under 12-week economics from then on. At what upgrade-conversion does the test beat control, and should we run it?

**Answer up front:** Break-even upgrade conversion is **≈ 4.9%** (primary model) to **≈ 8.3%** (conservative horizon). Both are low and realistic for a checkout upgrade offer → **yes, run the test.**

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

## Primary model (full 12-period curve)

- Recurring revenue, 4-week stream = **$95.98**
- Recurring revenue, 12-week stream = **$119.67** (Δ = **+$23.69**)
- Each upgrade adds 49.99 + 23.69 = **$73.68**, cannibalises **$3.60**
- **Break-even p\*** = 3.60 / 73.68 = **4.88%**

| Upgrade take-rate | Test net LTV (per 4-wk buyer) | Lift vs control ($123.70) |
|---|---|---|
| 0% (control) | $123.70 | — |
| 5% | $123.77 | +0.1% |
| 10% | $127.02 | +2.7% |
| 20% | $133.50 | +7.9% |
| 30% | $139.98 | +13.2% |

## Conservative model (strict 52-week horizon)

If the 12-week recurring stream is capped at payments charged inside one calendar year (4 periods — weeks 12/24/36/48 — $89.43), an upgrade slightly *shortens* the modelled recurring window, so the surcharge does more of the work:

- Each upgrade adds 49.99 + (89.43 − 95.98) = **$43.44**, cannibalises $3.60
- **Break-even p\*** = 3.60 / 43.44 = **8.28%**

Even here the test turns positive by ~8% take-rate and reaches +6.7% lift at 30%.

## Recommendation

**Run the test.** The downside is tiny and bounded: the only thing at risk is the $3.60 expected second upsell per 4-week buyer, and only for the test arm. The upside is a permanent **mix shift toward the highest-LTV plan** ($162 vs $124 net). Break-even sits at **~5–8%** upgrade conversion — well within what checkout upgrade/one-click-upsell offers typically achieve.

**How I'd run it & de-risk:**
1. Size the test for the target metric = **upgrade take-rate**, with net-LTV-per-4-week-buyer as the readout. Need enough 4-week buyers to detect a ~5% take-rate with confidence.
2. **Watch second-order effects the point model ignores:** (a) does adding an upgrade step depress overall checkout completion / first-upsell take? (b) do upgraded users **churn faster** because they were pushed into a bigger commitment (higher refund/chargeback risk)? Track early-period retention and refunds on upgraded cohorts, not just the day-0 take-rate.
3. Because break-even is so low, the real question isn't "will it pay off at a given conversion" but "does the upgrade **cannibalise something more valuable** (checkout completion, refunds)" — that's what the live test, not the spreadsheet, has to answer.

Model & scenarios: [`model/ltv_model.py`](model/ltv_model.py).
