# Product Manager — Test Assignment (Nomad Venture Studio / Jobescape)

> Verbatim capture of the assignment from the Notion brief (pulled 2026-07-24).
> Source: https://jobescape.notion.site/Product-Manager-Test-Assignment-38ac18739cd58083a8c2e0ea8f3f94d3
> This file is the single source of truth. Do not paraphrase the tasks — answer them.

---

## Introduction

**About the Company** — Nomad Venture Studio builds products helping people grow, create, and earn using modern technologies.

**Our Product** — Jobescape helps professionals and career workers learn how to apply AI in their work and career — to achieve better results and work faster and more efficiently. At the core is the flagship course **Master the Claude**, plus focused career courses (Claude for Accountants, Claude for Lawyers, Claude for Sales, and others).

**Our Markets** — International, primary focus on Tier-1 markets, US and Western Europe. Multiple locales.

**Users & Scale** — Around **1,000 new users register every day**.

**Submission Guidelines**
- Language: **English**
- Format: Any, but clear & structured
- Submission: Telegram — **@islam_s10**

---

## Test Assignment (framing)

This evaluates the **quality of thinking, not volume of output**: how you frame questions, find root causes, make choices, and drive to a decision.

**Disclaimer** — A submitted, imperfect assignment beats an unsubmitted one. Don't chase perfection so hard you submit nothing. If you need more time, let them know — quality matters more than speed.

**What they are NOT looking for**
- Beautiful design — they evaluate whether it works and how you think, not visuals
- Volume — a focused, working tool beats a big half-working one
- Restating the assignment back in fancier language

Asking the right questions is part of what they evaluate. Questions → **@islam_s10**.

---

# Part A. Audience & Product

**Context** — Users are acquired through ad creatives and a quiz funnel, after which the user reaches the paywall and the product.

**Materials**
- Ad Creatives — https://drive.google.com/drive/folders/1g2re4islAXTyjZwMGazMl0PI-t9nfBDo
- Quiz Funnel Answers — https://drive.google.com/drive/folders/1NOnAg-e13vvh0HaS0M2TQ1MMBqK0xmcy
- Quiz Funnel (live) — http://jobescape.me/chat-v3?quiz_version=v7.0.8
- **Product access** — go through the funnel and product yourself, **including paying at the paywall**. They will refund the subscription — just tell them which email you used.

### Task 1. Audience Segments
Based on the provided materials, build segments of the audience.
For each segment: **who they are, what job they're trying to do, what expectations and motivation they arrive with, what pain or need they have.**
Explain **what you split the audience by and why.**

### Task 2. Does the Product Meet Their Need
Go through the product and assess how well it addresses the pains and expectations of this audience.
Break down the gap between expectation and reality:
- what the user expected to get (based on creatives and quiz) — and what they got in the product;
- what doubts they might have had before purchasing — did the product resolve them or not;
- what was promised at the entry point but not delivered inside.

**Where is the main gap, and what's the risk for us?**

---

# Part B. Competitors

**Context** — In Part A you analyzed our audience and how our product addresses their needs. Now do the same for competitors and tell us what we should take from them.

### Task 1. Find Competitors
Find competitors similar to us — direct or indirect (those solving a similar job for a similar audience).
Explain **why** you consider them competitors and which are **direct vs. indirect.**

### Task 2. How They Serve Their Audience
Break down each competitor:
- which audience it serves and how similar it is to ours;
- which expectations and intents of that audience it addresses, and **how exactly** (mechanics, onboarding, product);
- what's done well and what's done poorly.

### Task 3. What to Take
A prioritized list of recommendations: which specific initiatives and mechanics to adopt and why they'd fit our audience. **Explain the order.**

---

# Part C. Release Verdict

**Context** — They recently shipped the feature **Challenge**.
- **Idea:** deliver the educational course as a 7-day challenge. One day = one specific AI skill (day 1 — working with documents, day 2 — working with Excel, etc.).
- **Hypothesis:** the daily challenge format (one skill/day) builds a habit of returning every day — raising first-week retention and reducing unsubscribes.
- **Target metric:** D1 Retention (retention the day after the challenge started).
- **Secondary metrics:** unsubscribe rate, lesson completion rate, Retention D3, Retention D7, CSAT.

**Links**
- In-app: https://app.jobescape.me/skills/challenges/338?source=skills
- Design (Figma): https://www.figma.com/design/w0O2ryFP52hITEPqmqlKSn/Challenges?node-id=0-1&t=DMf6W1QVWCESh7ED-1

**Data (BigQuery)**
- Console: https://console.cloud.google.com/bigquery?project=persona-496908
- Login + password: supplied by the company; kept in `00-context/credentials.md` (gitignored, never committed)
- Tables needed: `app_events` (all user events from app), `subscribe_events` (user + subscription details)
- Events Convention — https://drive.google.com/drive/u/0/folders/1QXWw3ZMwNavYohuE4GdNvsjMxH2osqYd
- Disclaimer: **not an SQL test** — use any tools including AI. They look at product analytics: what questions you ask the data, how you pull it, what conclusions you draw.

### Task 1. Release Analytics
Analyze how users go through the challenge and interact with it.
Look at how different segments behave (age, profession, etc.).
Compare groups by **engagement level (high / low / didn't take it)** across the main and secondary metrics. Define what counts as high and low engagement yourself. **Show your calculations.**

### Task 2. Verdict
- State your verdict: was the release a success or not?
- Which metrics did you rely on and how do you interpret them?
- Explain **why** the result turned out the way it did: what in the feature's mechanics and in user behavior leads to this?

### Task 3. What's Next
Based on your verdict, decide what to do with the feature and propose a concrete plan.
- If it worked — propose a **v2**: what functions/mechanics/ideas to add to strengthen the effect; what to focus on in the next release.
- If inconclusive or it didn't work — what specifically to change, add, remove, or refine to make it work.

### Task 4. Prototype
Based on Task 3, build a **working prototype** — vibe-code it in any tool (Lovable, Replit, Cursor, Claude Code, v0, etc.).
A polished product/perfect design isn't needed — a working prototype showing the essence of the idea and the core flow.
Attach:
- a **link** to the prototype,
- an explanation of **how exactly** the prototype would improve the challenge in the next release.

---

# Part D. Subscription Economics

### Task 1. Total LTV Calculation

**Context** — Users acquired from the US via Meta ads; monetized via subscription with three pricing plans. Plus two upsells (one-time) at checkout. Goal: understand the real economics of an acquired user — how much they bring over their lifetime, accounting for subscription, upsells, and fees.

**What to do** — Using the data, calculate **Total Net LTV over a one-year horizon** (one cohort year):
- Gross and Net LTV for each plan.
- Blended Average Net LTV.
- **Show your calculations.**

**Assumptions** — Payment provider fee: **12%**.

**Plan data** — see `part-d-economics/data/plans.csv`. Reproduced here:

| parameter | 1-WEEK | 4-WEEK | 12-WEEK |
|---|---|---|---|
| % of total subscriptions | 10% | 70% | 20% |
| Intro Price, $ | 6.93 | 19.99 | 39.99 |
| Intro Period, weeks | 1 | 4 | 12 |
| Recurring Price, $ | 39.99 | 39.99 | 62.99 |
| Recurring Period, weeks | 4 | 4 | 12 |
| C01, % | 55% | 67% | 64% |
| C12, % | 50% | 65% | 57% |
| C23, % | 60% | 70% | 65% |
| C34, % | 75% | 75% | 75% |
| C45, % | 80% | 80% | 75% |
| C56, % | 80% | 80% | 75% |
| C67, % | 80% | 80% | 75% |
| C78, % | 80% | 80% | 75% |
| C89, % | 80% | 80% | 75% |
| C910, % | 80% | 80% | 75% |
| C1011, % | 80% | 80% | 75% |
| C1112, % | 80% | 80% | 75% |
| First Upsell — Conversion Rate, % | 30% | 30% | 30% |
| First Upsell — Price, $ | 1.99 | 69.99 | 69.99 |
| Second Upsell — Conversion Rate, % | 12% | 12% | 12% |
| Second Upsell — Price, $ | 0.99 | 29.99 | 29.99 |

**Notes on the data**
- **Cmn** — probability that a user who survived to period *m* converts to (pays for) period *n*. E.g. C12 = probability of moving from period 1 to period 2.
- **Upsell Conversion Rate** — share of subscribers who buy the corresponding upsell.
- Upsells are one-time purchases made at the point of subscription checkout.

### Task 2. A/B Test Financial Model (Plan Upgrade)

**Context** — Task 1 = control (baseline). Now run an A/B test: in the **test group**, the **4-week subscriber** is shown a **Plan Upgrade** at checkout **instead of the second upsell** — an offer to switch to the 12-week plan.
**Test hypothesis:** a longer plan brings in more, so the upgrade raises LTV. Need to know: is the test worth it, and at what purchase conversion does it start to pay off.

**What changes in the test group (given — no need to calculate, just use)**
- Test-group 4-week subscriber sees the Plan Upgrade instead of the second upsell. Control is unchanged.
- Offer price: **$49.99**, one-time (surcharge to switch to 12-week).
- A buyer becomes a **12-week subscriber** — from then on billed under 12-week plan economics.

**What to do**
- Build a financial model of the test: LTV of the test group under different purchase-conversion scenarios.
- Find the **break-even** — the conversion at which the test matches control (Task 1).
- Given your scenarios, **would you recommend running this test?**
- **Show your calculations.**

---

## Logistics (from HR correspondence)
- Assigned: 2026-07-23. **Deadline: 2026-07-28, 23:59.** (~5 full days given.)
- Send solution to Telegram **@islam_s10** — he gives feedback; good result → next stage.
- **Attach the CV** with the submission (HR request).
- Questions welcome to @islam_s10 — asking good questions is evaluated.
