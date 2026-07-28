# Part D · Task 1 — Total Net LTV (one-year horizon)

**Answer up front (primary model):**

| Plan | Mix | Gross LTV | **Net LTV** |
|---|---|---|---|
| 1-WEEK | 10% | $68.66 | **$60.42** |
| 4-WEEK | 70% | $140.57 | **$123.70** |
| 12-WEEK | 20% | $184.26 | **$162.15** |
| **Blended (mix-weighted)** | 100% | — | **$125.06** |

Model: [`model/ltv_model.py`](model/ltv_model.py) (reads [`data/plans.csv`](data/plans.csv)). All figures reproducible by running it.

---

## How the model works

Per plan I model a cohort of **1 subscriber** and sum the cash they generate over the horizon, then apply the fee.

**1. Survival.** `Cmn` = probability a user who survived to period *m* pays for period *n*. Everyone pays the intro (period 0, survival `S0 = 1`). Survival to recurring period *k* is the running product:

```
S_k = C01 · C12 · … · C_(k-1,k)
```

**2. Revenue (gross).**
```
Gross = Intro Price
      + Recurring Price · Σ S_k        (k = 1…12, the 12 renewal transitions given)
      + E[first upsell]  = conv₁ · price₁
      + E[second upsell] = conv₂ · price₂
```
Upsells are one-time at checkout, so their expected value is applied once to every subscriber.

**3. Net.** Payment-provider fee is **12% on all collected cash** (intro, recurring, upsells):
```
Net = Gross · (1 − 0.12)
```

## Worked example — 4-WEEK plan (the 70% plan)

- Survival: S₁=.67, S₂=.4355, S₃=.3049, S₄=.2286, then ×0.80 each → S₁₂=.0384. **Σ S_k = 2.400.**
- Recurring revenue = 39.99 × 2.400 = **$95.98**
- Intro = **$19.99**
- Upsells = 0.30×69.99 + 0.12×29.99 = 20.997 + 3.599 = **$24.60**
- Gross = 19.99 + 95.98 + 24.60 = **$140.57** → Net = ×0.88 = **$123.70**

## Assumptions (stated explicitly — the brief is silent on these)

1. **Fee base.** 12% applies to *all* revenue including upsells (they clear the same processor). If the fee were subscription-only, net LTV rises slightly.
2. **Everyone pays the intro** (S0 = 1); the C-curve begins at the intro→first-recurring step (`C01`).
3. **Horizon = the 12 supplied transitions.** The data gives exactly 12 renewal steps per plan. For the 4-week plan that is 13 periods × 4 weeks = **exactly 52 weeks**, which anchors the "one-year horizon." I apply the full 12-step curve to every plan as the **primary** model.
4. **Upsells fire once, at checkout**, independent of retention.

## Sensitivity — strict 52-calendar-week horizon

The one wrinkle: a **12-week** plan billed 12 times spans ~2.8 years, not one. Under a strict "only payments within 52 weeks" reading, the 12-week plan gets just **4** billing periods:

| Plan | Net LTV (primary, full-curve) | Net LTV (strict 52-wk) |
|---|---|---|
| 1-WEEK | $60.42 | $60.42 |
| 4-WEEK | $123.70 | $123.70 |
| 12-WEEK | $162.15 | **$135.53** |
| **Blended** | **$125.06** | **$119.74** |

Only the 12-week plan (20% of mix) moves — under the strict reading it gets 4 charges (weeks 12/24/36/48, all inside the year) instead of 12 — so blended net LTV sits in a tight **$120–$125** band either way. I lead with $125.06 but flag the band. **Which reading the reviewer intends is the one open question I'd confirm** (see submission notes).

## Validation against the real cohort (BigQuery)

The brief supplies the plan table as given, so the model uses it as instructed. But the Part C pull
lets me check whether those inputs describe reality — **9,956 paying subscribers**, 2026-06-12 →
2026-06-25 ([`part-c-release-verdict/analysis/04_loose_ends.py`](../part-c-release-verdict/analysis/04_loose_ends.py)).

**Plan mix — the model's weights hold up:**

| Plan | `plans.csv` assumes | **Observed** |
|---|---:|---:|
| 1-WEEK | 10% | **10.2%** |
| 4-WEEK | 70% | **64.6%** *(incl. a 0.9% `4Week_special` variant)* |
| 12-WEEK | 20% | **25.1%** |

The mild shift from 4-week to 12-week moves blended net LTV **up**, not down: reweighting to the
observed mix gives **$126.9** against the modelled $125.06. The headline number is safe.

**Early churn — directionally consistent, and the 1-week plan is the weak point.** Observed
unsubscribe inside the 14-day window: **1-week 34.6%, 4-week 12.2%, 12-week 10.6%.** Only the 1-week
plan can even reach a renewal decision inside that window, and its 34.6% sits in the right
neighbourhood of the 45% first-period drop the supplied `C01 = 55%` implies (the gap is users who
lapse passively rather than pressing cancel). The 4-week and 12-week figures are floors — their first
renewals fall outside the window entirely — so this validates the shape of the curve, not its level.

**What it changes:** nothing in the answer, but it sharpens the read-through. The 1-week plan is 10%
of subscribers, generates the lowest net LTV ($60.42), carries almost no upsell value ($0.72/sub),
and churns at 3× the others. It is the plan most exposed to the refund/chargeback risk in
[the economics thesis](../research/deep-05-product-reality.md) — worth asking whether it earns its
place in the lineup at all.

## Read-through

- The **4-week plan carries the business** (70% of subs, $123.70 net each).
- The **12-week plan is the most valuable per user** ($162 net) but only 20% of mix — a natural target for a mix-shift, which is exactly what Task 2 tests.
- **Upsells matter unevenly:** $24.60/subscriber on the 4-/12-week plans vs just $0.72 on the 1-week plan (its upsell prices are tiny — $1.99/$0.99).
