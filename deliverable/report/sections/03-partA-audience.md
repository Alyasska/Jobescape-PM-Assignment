# Part A — Audience &amp; Product

## A.0 — The funnel, decoded (primary evidence)

Jobescape's quiz was reconstructed end-to-end from its public constructor API — all **37 pages, every question, every answer option, and the one branch point**. It is a textbook "diagnose the pain, then sell the cure" funnel in four movements:

1. **Hook + segment on prior AI use.** Page 1 asks *"Have you ever used Claude?"* and **branches on `used_ai`** — the funnel's only fork. "Yes" → a FOMO card ("You're ahead — but this is just the start"); "No" → a reassurance card ("You're right on time"). Same destination, tailored emotion.
2. **"My Profile" — biometrics & intent.** why-Claude · work status · age · gender · goal → a *"Did we get everything right?"* summary. This is the raw material for demographic segmentation.
3. **"Challenges" — poke the pain, then teaser-sell.** Three pain blocks, each followed by a persuasion teaser: career fear (*"What scares you most about AI and your career?"*) → *"There is nothing to worry about"* + the Harvard "humans with AI will replace humans without AI" quote; document pain (*"used AI then spent just as long fixing it?"*) → "Create polished content"; build-an-app pain → "Building an app has never been this easy."
4. **"Personalization" → commitment → paywall.** Learning-style, time-commitment, certification desire, *"what stopped you before?"*, an AI-profile reveal, a fake-progress loader, **email + name capture**, a "Your Personal Plan" teaser, then the **selling page** and a second "chase" offer.

**The read:** the funnel's *product* is emotional — it manufactures urgency (FOMO), self-identified pain, sunk-cost investment (35 taps of personalization), and then presents payment at the peak of aroused anxiety. Full page-by-page map in the Appendix.

## A.1 — Audience segments

**How these were produced.** The first version of this section was a framework: six segments
authored from a jobs-to-be-done model, then counted by a hand-written rule chain. It read well and
it could not be wrong — the structure came from me, so no answer in the data could contradict it.

So it was replaced with a real segmentation. k-modes clustering over **38,071 quiz respondents ×
10 categorical answers**, from a 49,528-respondent export. k-modes rather than k-means because the
answers are nominal: the average of "35–44" and "business owner" is not a quantity, and one-hot
plus Euclidean distance quietly assumes every pair of answers is equally far apart — which is the
assumption under test.

**The honest headline is that there is no elbow.** Within-cluster cost falls smoothly across
k = 2…8 (5.09, 4.79, 4.67, 4.49, 4.40, 4.31, 4.20) with no knee. This audience is a continuum, not
a set of natural types. Six is a resolution chosen and defended, not a count the data forced —
and any segmentation of this audience should be presented that way.

| Segment | Who they are (cluster signal) | Share | Strongest lift |
|---|---|---|---|
| **The Striver** | senses a gap and is closing it deliberately — growth-motivated, 45–54, male-skewed | 28.4% | "somewhat ready, could be behind" **1.9×** |
| **The Latecomer** | the oldest buyers; hasn't started, watching the field move without them | 22.0% | "falling behind as others move faster" **2.2×** · never used Claude 1.9× |
| **The Adept** | already gets real value from AI and wants more leverage — female-skewed | 20.9% | "AI already helps me a lot" **2.5×** |
| **The Optimiser** | mid-career professional using Claude on real work, wants speed | 12.3% | aged 35–44 **2.6×** |
| **The Founder** | learning AI to build something of their own | 9.0% | "start my own business" **3.1×** |
| **The Switcher** | between jobs, changing direction, starting from zero | 7.4% | "exploring options" **4.4×** |

*Derived by k-modes clustering over 38,071 quiz respondents × 10 categorical answers
(`part-a-audience/analysis/cluster_quiz.py`), not authored. Lift = share inside the cluster ÷ share
in the population. There is no elbow — within-cluster cost falls smoothly across k = 2…8 — so
this audience is a continuum and six is a defended resolution, not a count the data forced.*

> Why the clusters split on motive rather than age: occupation-level AI adoption ranges ~12–65%, and self-assessed *confidence* — not age — is the strongest predictor of use (HBS). The data agrees: the sharpest single signal is **work status** ("exploring options", 4.4× lift), not a demographic band.

The buyer-side cut comes from `subscribe_events` (**9,956 paying subscribers**), read against the quiz clusters. An earlier hand-written rule chain produced a different six: clustering rejected two of them and surfaced one — The Adept — that the framework had missed entirely.

**Three findings that overturned my priors:**

1. **The audience is old, not young.** ~62% of quiz-takers and **~60% of buyers are 45+**; the largest single cell among buyers is **men aged 55+ (21.3%)**. Buyers are 59.7% male. The AI-adoption age skew was the wrong prior for *this* funnel.
2. **Older buyers are the better buyers.** Two-week unsubscribe falls monotonically with age: **31.1%** (18–24) → 19.7% → 14.5% → **9.5%** (45–54) → 9.7% (55+). The loyal core is the oldest half of the book — which makes gamified streak mechanics a design aimed at the 9% that churns hardest.
3. **The goal a buyer arrives with predicts whether they stay.** "Work faster" (30.3% of buyers) and "feel more confident with AI" (20.0%) churn at ~11%; **"get a quick side hustle" churns at 37.2%**, "gain flexibility / work remotely" at 27.4%, "unlock better income" at 25.4%. The income-and-freedom intents are ~12% of buyers and churn at 2.5–3.5×. **Every creative that promises a side hustle buys a customer who leaves** — the positioning inconsistency of A.2, priced.

Also notable: only **47%** of quiz-takers name a career fear at all — the rest call AI an opportunity. The fear-heavy funnel over-indexes on one half of its own audience.

## A.2 — Does the product meet the need? (expectation vs. reality)

The *reality* column combines **public user evidence** — App Store 4.7 (~1.5K), Trustpilot 4.5 (~8K), plus the Coursiv twin as proxy (`research/deep-05`) — with my own walkthrough as a paying customer (I bought the 4-week plan for $15.19 and screenshotted the funnel, paywall, product and cancel flow; notes in `part-a-audience/materials/walkthrough/observations.md`). **Tell:** ratings are high *and* billing complaints are constant — an aggressive review-solicitation funnel over a dispute-heavy monetization model; the score is a marketing asset, not proof the gap is closed.

**Three things I could only confirm by paying for it:**

- The paywall's **"personal AI mentors"** is a single bot with a stock-photo face and a human name ("Mark"), present on every page as an "Ask Mark" button.
- The paywall's **"24/7 support chat"** is a **metered 5-credit** AI chat.
- **Live pricing differs from the supplied plan table** — a "61% intro offer" with a 9:46 countdown: $6.93 / $15.19 / $25.99 intro, renewing at $38.95 / $38.95 / $66.65. Part D uses the brief's figures as instructed; the real dynamic pricing is flagged as an observation.

**And one correction to the review-sourced picture:** the widely-repeated *"bot-only cancellation"* claim is **wrong for cancellation**. The paywall fine print names a self-serve **Manage Subscription** tab, it exists, and the event log records **1,358 uses of it**. The trap is the **refund** (gated on finishing the plan in ~31 days), not the cancel. Worth being precise about — it's the difference between a dark pattern and a bad guarantee.

| Lens | Entry-point promise | What users say they got (reviews) |
|---|---|---|
| **Expected** | ~$25 "trial"; personalized plan; expert instruction; exclusive tools | A bigger bill (**+$88 "AI support" in fine print**, "$100 not a trial," silent renewals, a **bank-flagged-as-fraud** charge); content "you can just ask ChatGPT," repackaged free tools, **anonymous team** |
| **Doubts** | "Will this work for me? Am I behind?" | Often *reinforced* — "shallow vs. free alternatives" |
| **Promised, not delivered** | "Earn or money-back" guarantee; a freelance *income* ("land clients in 3 months") | Refund **gated on finishing 14 modules / the plan in ~31 days**; outcome-buyers feel misled ("gurus promising 10k/mo") |

**Where the main gap is, and the risk.** I came in expecting the core gap to be the *motivation switch* (fear-sale → slow habit product) — and that's real. But the evidence relocates the *acute* risk one layer down: the **price-and-exit gap** — users are billed more than they agreed, then can't easily get their money back (the refund weaponized as a completion trap — cancellation itself is self-serve). That's not just churn — it's **refunds, chargebacks, 1-star reviews, and regulatory exposure**: this is the exact model the **FTC sued Genesis (a peer) over in June 2026** (ARL tail ≈ 3× annual net revenue, Part D). The 4.5–4.7 ratings **hide** it. Compounding it: a **positioning inconsistency** (jobescape.me "AI at work" vs. app "freelancing income" vs. a rotating App-Store title) pre-loads mismatched expectations. The fix is the same one Part D calls an economic moat and Part B ranks first — **transparent pricing + a guarantee that isn't a trap.**
