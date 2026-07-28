# PM Test Assignment — Submission · Aliaskar Bekishev

*Prepared for Nomad Venture Studio (Jobescape). Submitted to @islam_s10.*

---

## Answers at a glance

Eleven tasks, in your order. The section number is where the full answer sits in this document.

| Task | The answer | § |
|---|---|---|
| **A1** · Segments | Six, **derived by clustering, not asserted** — Striver, Latecomer, Adept, Optimiser, Founder, Switcher. Split on motive + status, because the data's sharpest signal is work status (4.4× lift), not age. No elbow, so six is a defended resolution | 02 |
| **A2** · Expectation vs reality | Paywall sells "personal AI mentors" and "24/7 chat"; product delivers one bot named Mark and a **5-credit** chat. Main gap is activation — **50.2% never finish a lesson**. Risk is the **refund**: 11.3% of cancellations are payment disputes | 03 |
| **B1** · Competitors | 4 direct twins (Coursiv, Iro AI, Section, Outskill) + funnel twins. **The dangerous one is indirect: free content** — YouTube and ChatGPT set the quality bar | 04 |
| **B2** · How they serve | They win on **containers, not content** — practice surfaces, paywall craft, finite challenges. Nobody has better material | 05 |
| **B3** · What to take | Five, ordered **de-risk → retain → differentiate → diversify → expand**: daily-cost paywall, branded gated challenge, practice surface, owned newsletter, offer ladder | 06 |
| **C1** · Release analytics | 9,956 subscribers. **89% never start it**; of starters **44.9% complete zero lessons**. High/low/didn't-take across D1/D3/D7/unsub/CSAT, tiers defined on lessons completed and swept 1–8 | 07 |
| **C2** · Verdict | **Not a success.** The +38pt D1 gap is selection: against an exposure-matched control it is **+0.5 pts, p = 0.82**. Three further tests agree. Cause is mechanical — **no daily gate exists**, so 27% finished the "7-day" challenge in one sitting | 08 |
| **C3** · What's next | **94.6% of people shown the popup clicked it** — appeal is fine, 68.5% were never shown it. So: make it the default path, shipped to 80% with a 20% hold-out — one change fixes the biggest loss *and* creates the control group v1 never had. Then the first 10 minutes, a hard gate, and route the user to their personal plan when the day closes — today it ends into nothing | 09 |
| **C4** · Prototype | **The daily gate, built and live** — commit to a time, tomorrow locked behind a countdown, a guaranteed first win. https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/ | 09 |
| **D1** · LTV | Net **$60.42 / $123.70 / $162.15**, blended **$125.06**. ΣSₖ from the C-curve; net = gross × 0.88. Cross-checked against the observed plan mix ($126.90) | 10 |
| **D2** · A/B break-even | **8.29%** on a like-for-like one-year horizon (= $3.60 ÷ $43.44). Applying all 12 supplied transitions to both plans gives 4.88%, but that hands the test arm 156 weeks and the control 52 — the same different-clocks error Part C is about. **Recommend running it** — downside capped at $3.60 per test-arm buyer | 11 |

---

## The thesis that ties all four parts together

**Jobescape has built an excellent machine for selling a product it hasn't finished building.**

The funnel acquires an older, serious, surprisingly loyal professional audience at scale. Then
**50.2% of paying subscribers never complete a single lesson.** Every part of this assignment lands on
the same seam — acquisition is strong, *activation* was never built, and the economics depend
entirely on the retention tail that activation would protect.

- **A** — the funnel sells "work faster / feel more confident" to a 45+ professional, and that buyer is
  loyal (9.5% two-week churn). The product gives them no first win.
- **B** — the content itself is free everywhere. The only defensible moat is scaffolding, feedback and
  accountability — i.e. precisely the activation layer that is missing.
- **C** — the one feature built to be that layer reaches **11% of payers**, has no daily gate, and moves
  its target metric by **+0.5 pts (p = 0.82)**.
- **D** — **84% of LTV lands after the intro payment** (68% recurring + 16% upsells), so a 1–2 point retention gain beats any funnel
  squeeze — and refunds/chargebacks are the tail risk.

---

## Part A — Audience & Product

**A1 · Segments** → [part-a-audience/01-segments.md](../part-a-audience/01-segments.md)

I split on **driving emotion + job-to-be-done** rather than demographics, because that is what the
funnel selects for and what predicts whether a habit product will satisfy the buyer. Six segments —
**The Striver · The Latecomer · The Adept · The Optimiser · The Founder · The Switcher** — each tied to a quiz signal, with a full decode of the 37-page
quiz funnel.

**Derived from real data, twice over.** k-modes clustering over 38,071 quiz respondents (from a 49,528-respondent, 210 MB export) and
all 9,956 paying subscribers (BigQuery). Three findings that overturned my priors:

- **The audience is old, not young — ~60% of buyers are 45+**, and the largest single cell is men
  aged 55+ (21.3% of all buyers).
- **Churn falls monotonically with age**: 31.1% (18–24) → 9.5% (45–54). The oldest buyers are the best
  buyers.
- **The goal a buyer arrives with predicts whether they stay.** "Work faster" and "feel more
  confident" are half the book and churn at ~11%. "Quick side hustle" churns at **37.2%**. Every
  creative that promises income buys a customer who leaves.

**A2 · The gap** → [part-a-audience/02-product-gap.md](../part-a-audience/02-product-gap.md)

The underlying gap is a **motivation switch** — the funnel sells fear relief and a fast payoff, the
product delivers slow habit-building. Public reviews relocate the *acute* risk to the
**price-and-exit gap**: billing above what was agreed, and a refund guarantee gated on finishing the
course in ~31 days. The event log confirms the consequence: **11.3% of all unsubscribes are payment
failures, chargebacks or refund disputes.** That is regulatory exposure, not ordinary churn — the
model the FTC sued Genesis over.

*One correction I'd make to the review-sourced picture, having paid and walked the product myself:
the widely-repeated "bot-only cancellation" claim is wrong for cancellation. There is a self-serve
**Manage Subscription** tab, and the event log shows 1,358 uses of it. The trap is the **refund**, not
the cancel.* What I did find first-hand is a different mismatch: the paywall's "personal AI mentor"
is a bot with a stock photo and a human name ("Mark"), and its "24/7 support chat" is a metered
5-credit AI chat.

## Part B — Competitors

**B1** → [01-competitors.md](../part-b-competitors/01-competitors.md) · **B2** → [02-analysis.md](../part-b-competitors/02-analysis.md) · **B3** → [03-recommendations.md](../part-b-competitors/03-recommendations.md)

Jobescape has **structural twins** (Coursiv, Iro AI — "Duolingo for AI") and a cloned funnel
(Headway). The decisive fact: **the content is free** — ChatGPT, YouTube, newsletters — so Jobescape
cannot win on content. It must win on **scaffolding, feedback and accountability**. Prioritized
steals, ordered *de-risk → retain → differentiate → diversify → expand*:

1. **Mimo's "Blinkist paywall"** (+100% trial opt-in, −25% early cancels) — cuts refund risk, near-zero build.
2. **Coursiv's branded finite challenge + honest pricing** — the retention container, and it defuses the FTC-style risk.
3. **Iro's Prompt Lab + Section's saveable co-pilot** — the practice surface; the actual moat against free tools.
4. **Owned newsletter + "expensable" pricing** — CAC hedge.
5. **Offer-ladder tests** — activation and ARPU.

## Part C — Release Verdict (the Challenge)

**C1 · Analytics** → [01-analytics.md](../part-c-release-verdict/01-analytics.md) — 9,956 paying
subscribers, all calculations reproducible via [`analysis/`](../part-c-release-verdict/analysis/).

| | |
|---|---|
| **Reach** | 89% of payers never start it; 67.5% never see a challenge surface at all |
| **Engagement** | of 1,111 starters: 45% complete zero lessons, 14% reach lesson 3, 4.3% finish |
| **Target metric** | takers **60.0%** D1 vs people who looked and walked away **59.6%** — **+0.5 pts, p = 0.82** |
| **Unsubscribe** | −2.3 pts vs the matched control, p = 0.12 — not significant |
| **CSAT** | falls as engagement rises: 3.74 → 3.53 → 3.33 → **3.10** for finishers |

**C2 · Verdict** → [02-verdict.md](../part-c-release-verdict/02-verdict.md): **No — the release was
not a success.** It moved neither its target metric nor its secondary ones.

Two things make this more than a scorecard:

- **The dashboard would have called it a win.** On the team's own metric definition the Challenge
  posts 39.8% D1 against a 26.0% baseline — a "+14-point win" that is entirely an artifact of two
  different clocks and two different populations. Correcting for survivorship takes the gap from
  +38 pts to +17; matching on exposure takes it to +0.5.
- **v1 never tested its own hypothesis.** The theory was "one day = one skill builds a daily habit,"
  but the gate is a dismissible warning, not a lock, and it is not logged. **27% of the people who finished the "7-day" challenge
  finished it in a single sitting**, 46% within two. You cannot fail a daily-habit test with a feature
  that has no days in it.

**C3 · What's next** → [03-whats-next.md](../part-c-release-verdict/03-whats-next.md): rebuild the
mechanic, then re-run it as a real experiment. Sequenced **instrument → mechanic → first-ten-minutes
→ quality → reach**, with pre-registered success criteria and a kill rule.

The counter-intuitive call: **reach is the last fix, not the first.** The obvious response to "only
11% see it" is to promote it — but satisfaction *falls* as engagement rises, so scaling reach on
3.25-star content scales refunds, which Part D says is the real threat.

**C4 · Prototype — ▶ LIVE:** **https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/**

A working React app built in **Jobescape's own design system**, so it reads as a feature of the
product rather than a mockup of one. Five steps around **the daily gate — the mechanic v1 never
shipped** — each with its own URL and each annotated on the page with the finding that produced it.
It takes Jobescape's visual language but not its streak: the buyer is a professional in their
fifties, and the 18–24s who respond to streaks and confetti are 9% of the book and churn at 31%.
Source: [Alyasska/Nomad_Venture_Studio_TA_C4](https://github.com/Alyasska/Nomad_Venture_Studio_TA_C4).

## Part D — Subscription Economics

**D1 · LTV** → [01-ltv-model.md](../part-d-economics/01-ltv-model.md)

| Plan | Mix | Gross LTV | **Net LTV** |
|---|---|---|---|
| 1-WEEK | 10% | $68.66 | **$60.42** |
| 4-WEEK | 70% | $140.57 | **$123.70** |
| 12-WEEK | 20% | $184.26 | **$162.15** |
| **Blended** | 100% | — | **$125.06** |

Full model and code in [`model/ltv_model.py`](../part-d-economics/model/ltv_model.py). Sensitivity on
the horizon question keeps blended net LTV in a tight **$120–$125** band.

**Validated against the real cohort:** the observed plan mix is 10.2% / 64.6% / 25.1% against the
brief's 10 / 70 / 20 — reweighting moves blended net LTV to **$126.90**, so the headline is safe. The
1-week plan is the weak point: lowest LTV, almost no upsell value, and **34.6% churn inside two weeks**.

**D2 · A/B break-even** → [02-ab-test-model.md](../part-d-economics/02-ab-test-model.md) —
plan-upgrade break-even at **≈8.3%** take-rate, like-for-like. **Recommend running it**; only the $3.60 second-upsell
is at risk. Watch upgraded-cohort churn and refunds in the live test.

---

## The three questions I'd ask before doing any of this

Asking the right questions is part of the brief, and these are the ones the data cannot answer:

1. **Was the Challenge ever meant to be judged on D1?** There is no hold-out anywhere in the data. If
   it shipped as a refund-gate or a support-deflection device, it should be judged against refunds and
   ticket volume — and my verdict changes.
2. **What D1 number would the team have called success?** I can say the release moved nothing; I can't
   say whether it missed the bar by a little or a lot.
3. **Which LTV horizon does the team model** — the full supplied curve, or 52 calendar weeks? It is the
   one genuine ambiguity in Part D, worth $5 of blended LTV.

## What's in this submission

| | |
|---|---|
| **1 · Answers** | this document — every task in your order, with the calculations |
| **2 · Presentation** | 48 slides, ~30 minutes, all eleven tasks. Citations are clickable in the PDF |
| **3 · Research dossier** | the evidence, the market picture, and the economics thesis |
| **4 · Appendix** | generated analysis output, all 8 SQL queries, the verification run, and the key scripts |
| **5 · CV** | |
| **Prototype** | https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/ — Part C Task 4, live |

Every figure in Parts C and D can be re-derived in one command:
`cd part-c-release-verdict/analysis && python3 05_qa.py`.

### Pre-submit checklist

- [x] Prototype published to GitHub Pages — public, verified in a logged-out browser
- [ ] Attach `Jobescape-Research-Dossier.pdf`, `Jobescape-PM-Deck.html` + `Aliaskar_Bekishev_CV.pdf`
- [ ] BQ password / secrets NOT present anywhere in the submission
- [ ] **Request the $15.19 refund from @islam_s10 — LAST step** (it ends product + BigQuery access)
