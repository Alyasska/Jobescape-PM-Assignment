# Part D — Subscription economics

*Fully modeled from the raw plan data; reproducible via `part-d-economics/model/ltv_model.py`.*

## D.1 — Total Net LTV (one-year horizon)

**Method.** Per plan, model one subscriber: everyone pays the intro (survival S₀ = 1); survival to recurring period *k* is the running product of the given conversion rates `S_k = C01·C12·…`. Revenue = intro + recurring·ΣS_k + expected upsells (conv×price, one-time). Net = gross × (1 − 12% processor fee).

| Plan | Mix | Gross LTV | **Net LTV** |
|---|---|---|---|
| 1-WEEK | 10% | $68.66 | **$60.42** |
| 4-WEEK | 70% | $140.57 | **$123.70** |
| 12-WEEK | 20% | $184.26 | **$162.15** |
| **Blended (mix-weighted)** | 100% | — | **$125.06** |

**Worked example (4-week, the 70% plan):** ΣS_k = 2.400 → recurring 39.99×2.400 = $95.98; + intro $19.99; + upsells (0.30×69.99 + 0.12×29.99) = $24.60 → gross **$140.57**; ×0.88 → **$123.70 net**.

**Key assumptions (stated):** 12% fee on *all* revenue incl. upsells; the 12 supplied `Cmn` transitions define the horizon (for the 4-week plan that is exactly 52 weeks — the anchor for "one year"); upsells fire once at checkout.

**Sensitivity.** The only wrinkle is the 12-week plan: billed 12 times it spans ~2.8 years, not one. Under a strict "payments charged within 52 weeks" reading it gets just 4 charges (weeks 12/24/36/48) → 12-week net LTV $135.53, **blended $119.74**. Since only 20% of the mix moves, blended net LTV sits in a tight **$120–$125 band** either way. *(Which horizon the reviewer intends is the one clarifying question worth asking.)*

**Read-through:** the **4-week plan carries the business** (70% × $123.70); the **12-week plan is the most valuable per user** ($162) but under-represented — a natural mix-shift target, which is exactly what Task 2 tests.

## D.2 — A/B plan-upgrade break-even

**Setup.** Test group: the 4-week buyer is shown a **Plan Upgrade to 12-week** ($49.99 one-time) instead of the second upsell; a buyer is billed under 12-week economics thereafter.

Intro and first upsell are identical in both arms (they cancel), and the 12% fee is uniform (cancels too), so break-even is clean:

```
Both arms must be measured over the SAME year. A 12-week plan billed 12 times spans
156 weeks; a 4-week plan billed 12 times spans exactly 52. Inside one year the
12-week plan bills 4 times.

p* = E[2nd upsell] / (Upgrade + RecRev12(1yr) − RecRev4(1yr))
   = 3.60 / (49.99 + 89.43 − 95.98) = 3.60 / 43.44 = 8.29%
```

Inside one year the recurring delta is **negative** (−$6.55): a 12-week subscriber bills four times against the 4-week plan's twelve. So the upgrade is a **cash-forward trade** — $49.99 today against slightly less recurring this year, for a subscriber on a lower-churn plan. It cannibalises **$3.60**.

| Upgrade take-rate | Test net LTV / 4-wk buyer | vs control ($123.70) |
|---|---|---|
| 0% | $120.53 | −$3.17 — the cost of the swap if nobody upgrades |
| 8.3% | $123.70 | break-even |
| 15% | $126.27 | +2.1% |
| 30% | $132.00 | +6.7% |

**Break-even ≈ 8.3%** on a like-for-like one-year horizon.

**Recommendation: run the test.** The downside is tiny and bounded (the $3.60 second upsell, test arm only); the upside is a permanent shift toward the highest-LTV plan. But because break-even is so low, the spreadsheet isn't the real question — the **live test must watch second-order effects the point-model ignores:** (a) does inserting an upgrade step depress overall checkout completion or first-upsell take? (b) do upgraded users **churn/refund faster** because they were pushed into a bigger commitment? Track early-period retention and refunds on upgraded cohorts, not just the Day-0 take-rate.
