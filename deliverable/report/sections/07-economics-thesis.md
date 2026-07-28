# The economics thesis (why retention is the moat)

This bridges Parts A, C, and D: it takes the per-plan LTV (Part D) up to the whole business, then shows *why* the Challenge (Part C) is an economic instrument, not just a UX feature.

## Funnel reconciliation — 1,000 signups/day → annual net revenue

Built bottom-up, every stage tagged GIVEN / BENCHMARK / ASSUMPTION with a low/base/high band:

```
1,000 signups/day
  × ~60%  quiz completion            (assumption)
  × ~92%  complete → paywall view    (assumption)
  × ~10.7% paywall → purchase        (benchmark: hard-paywall trial→paid)
  ≈ 59 buyers/day
  × $118.75 net LTV/buyer            (blended $125 − 5% education-refund)
  × 365
  ≈ $2.56M / year  (base)     range ≈ $1.19M – $4.52M
```

The two pins carrying the model are the **10.7% hard-paywall conversion** and the **AI-churn premium** (below). I'd plan on the **low-to-stress band (~$1.2–2.1M)**, not the headline — our $125 LTV is optimistic vs. RevenueCat's ~$26 annual-realized median (ours is full-curve lifetime, but still rich).

## The tail is the business — and AI apps churn through it faster

Decomposing the $125 blended LTV: about **$23 is intro cash**, which is retention-independent, and the remaining **84% arrives later** — 68% recurring plus 16% upsells. Only the intro is safe. That tail is exactly what the "AI apps churn ~30% faster" benchmark attacks:

- Applying the premium (monthly churn ~9.4% → ~12.2%, tail ×0.77) cuts blended LTV to **~$101 (−19%)** and annual net revenue from $2.56M to **~$2.06M (−$0.5M/yr)**.
- If the $125 was itself built on a non-AI curve, **~$2.06M is the truer base.**

Only about **16% of lifetime value is Day-1 cash.** The rest is hostage to a retention curve that AI apps are measurably worse at holding. That single fact is why the economics are *front-loaded and fragile* — and why the Challenge exists.

## Retention beats the funnel (and it's safer)

| Lever | Annual value | Notes |
|---|---|---|
| **+1–2pt monthly retention** | **+$160–350K/yr** | Compounds across all cohorts; exceeds the entire refund drag; we start from the *weak* AI baseline (most headroom). |
| +1pt paywall conversion | +$239K/yr | Near the ceiling already; raises refund / chargeback / ARL risk. |
| Cut refunds (edu ~5.1%) | ~$27K per point (~$135K/yr base) | Directly recovered by better expectation-setting. |
| Stay web-billed vs app-store | +$0.2–0.4M/yr | Distribution-fee avoidance. |

**Defend the tail; don't squeeze the funnel.** The Challenge (Part C) is the instrument that buys back the AI-churn premium — a 1–2pt retention lift is worth more than a near-impossible conversion gain, and carries none of the regulatory downside.

## The asymmetric tail risk — and the one move that fixes three problems

The regulatory exposure is not theoretical: **the FTC sued Genesis (a peer quiz-funnel studio) in June 2026**, and the reference **$7.5M ARL settlement ≈ 2.9× annual net revenue** — an existential, asymmetric tail. The drags also *stack* (refunds + app-store + churn).

> Transparency + easy-cancel is a single move that fixes three things at once: it cuts refunds, defuses the regulatory existential risk, *and* lifts voluntary retention. It's the rare compliance action that is also the highest-ROI growth action.

**Net thesis:** the economics are front-loaded and fragile — a thin slice of certain Day-1 cash sitting on a fragile, fast-decaying recurring tail. So retention and trust are the moat, and the two initiatives that build them — the Challenge (habit) and transparency/easy-cancel (trust) — are not cost centers; they are the highest-leverage economic bets Jobescape can make.
