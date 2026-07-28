# Executive summary

## The thesis

> **Jobescape has built an excellent machine for selling a product it hasn't finished building.**

Acquisition works. Activation was never built. And the economics depend almost entirely on the retention tail that activation would protect.

The measured fact underneath it: **50.2% of paying subscribers never complete a single lesson** — not in the Challenge, anywhere in the product. Everything below is a facet of that one seam.

## What the evidence establishes

**The funnel sells fear, and it sells well.** The 37-step quiz profiles the user, then systematically pokes pain — *"What scares you most about AI and your career?"* — before stacking FOMO teasers and presenting payment at the peak of it. That is rational positioning, not cynicism: 52% of US workers are more worried than hopeful about AI (Pew), and 66% of leaders say they won't hire someone without AI skills (Microsoft/LinkedIn).

**But fear only closes the sale.** Habit and relevance are what retain, and self-paced learning is a churn minefield — MOOC completion runs 5–15%, and the drop-off is motivational rather than cognitive. A product built on this funnel has to convert fear into habit quickly, or it inherits that churn.

**The buyer is a decade older than the internal read.** Around 60% of paying subscribers are 45+, and the largest single group is men aged 55+ — 21.3% of all buyers. Churn falls steadily with age: 31.1% at 18–24 against 9.5% at 45–54. The oldest buyers are the best buyers. That makes streak-and-badge mechanics a design aimed at the least valuable 9% of the book.

**The Challenge was the right instinct, wrongly built.** Measured across 9,956 paying subscribers: 89% never start it. Among those who do, the target metric doesn't move. Takers retain at 60.0% on D1 against **59.6% for people who reached the same screen and walked away** — a gap of +0.5 points, p = 0.82.

The reason is mechanical. The hypothesis was "one day = one skill builds a daily habit," but the gate is a dismissible warning rather than a lock — so **27% of finishers completed the whole "7-day" challenge in a single sitting.** Version one didn't fail its hypothesis. It never tested it.

**The content is free elsewhere, and the funnel is already cloned.** Structural twins run the identical playbook — Coursiv, and Iro AI which is a literal "Duolingo for AI" — while ChatGPT, YouTube and newsletters give the material away. Defensibility has to come from scaffolding, feedback and accountability: the AI tutor as a practice surface, which is the one thing free substitutes cannot provide.

**The acute risk is billing, not content.** Ratings are strong — 4.7 on the App Store, 4.5 across ~8,000 Trustpilot reviews — yet complaints cluster on surprise charges and refunds gated on course completion. In this cohort, **11.3% of all cancellations are payment failures, chargebacks or disputes.** The FTC sued a peer quiz-funnel studio, Genesis, over this exact model in June 2026. The high rating hides the exposure.

One correction worth flagging, because it cuts against the reviews: cancellation itself is **self-serve**. The event log records 1,358 uses of the Manage Subscription flow. The trap is the refund, not the cancel button.

## The numbers

| | 1-week | 4-week | 12-week | **Blended** |
|---|---|---|---|---|
| Net LTV, one-year horizon, 12% fee | $60.42 | $123.70 | $162.15 | **$125.06** |

The A/B plan-upgrade test breaks even at an **8.3% take-rate**, measuring both arms over the same year. A low bar, and the only thing at risk is the $3.60 second upsell it replaces. Recommend running it.

## What is measured, and what is inferred

**Measured from source data.** All of Part C, from BigQuery across 9,956 paying subscribers. Part A's segments, from k-modes clustering over 38,071 quiz respondents. Part D, from a model built over the supplied plan table and cross-checked against the observed plan mix. Every published figure in Parts C and D is re-derived from the raw exports by a verification script — 91 assertions, all passing.

**Inferred from public evidence.** Part B's competitor teardowns, and the expectation-versus-reality gap in Part A — sourced from public reviews plus my own walkthrough as a paying customer.

**What this data cannot settle.** Whether the Challenge was causal. There is no hold-out group and no pre/post period anywhere in the warehouse; the release shipped to 100%. The causal reading here is an observational reconstruction, and it only worked because a large "looked at it and left" group happened to exist as a natural control. That is luck, not design — which is why fixing it is the *first* recommendation in Part C rather than the last.
