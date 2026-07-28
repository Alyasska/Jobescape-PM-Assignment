# Deep-04 — Economic Thesis: Funnel Reconciliation, AI-Churn Stress & the Retention Moat

**Deep-analysis Step 3 for the Jobescape (Nomad Venture Studio) PM take-home. Bridges Parts A / C / D.**
Builds on the benchmarks in `research/02-market.md` (cited inline as `[02-market §x]`). Every input is
tagged **[GIVEN]**, **[BENCHMARK]** (external, sourced), or **[ASSUMPTION]** (my labeled estimate where
the brief/data is silent). All arithmetic is shown so a reviewer can re-run it. Numbers are ranges, not
false precision.

> **Headline:** at 1,000 signups/day, base-case **net revenue ≈ $2.56M/year** (range **~$1.2M – $4.5M**),
> on a full-curve LTV basis. ~84% of that value sits in a **recurring tail that AI apps churn through
> ~30% faster than the category** — so the number is real but **front-loaded and fragile**, and the
> single highest-ROI lever is **retention (the Challenge) + transparency/easy-cancel**, not squeezing
> the funnel harder.

---

## 0. Inputs & framing

**Funnel shape [GIVEN]:** ad → ~35-step quiz → hard paywall → intro-priced subscription + 2 checkout upsells.
**Plan mix [GIVEN]:** 10% 1-week / 70% 4-week / 20% 12-week.
**Prices [GIVEN]:** intro $6.93 / $19.99 / $39.99; recurring $39.99 / $39.99 / $62.99.
**Net LTV [GIVEN, our Part D model]:** ≈ **$60 / $124 / $162** per plan; **blended ≈ $125** — already net of
the **12% processor fee**, full-curve (lifetime) horizon. *Not* stated to be net of refunds → we apply
refunds explicitly below (so we can show the drag).

**Definition of "signup":** I treat the 1,000/day as **quiz-starts** (people who enter the funnel), because
the task asks me to model `quiz-start → complete`, `complete → paywall-view`, `paywall → purchase` off that
base. If "signup" instead means post-quiz email capture, shift the top of the funnel down one stage — the
purchase count is unchanged because it's pinned by the paywall-conversion benchmark.

**Revenue basis:** "daily/annual net revenue" here = **buyers × net LTV/buyer** = the full-curve net
revenue *attributable to* each day's acquisition (cohort-LTV basis), then annualized. This is **not** same-
day cash — see the cash-timing note in §4. In steady state (once cohorts stack), annual recognized net
revenue converges to the same figure: you acquire ~21.6K buyers/year, each worth ~$119 net lifetime.

**Sanity flag on the $125 [BENCHMARK cross-check]:** RevenueCat's *annual realized* LTV/payer median is
**~$26 (NA) / ~$27 (WEU)** `[02-market §3c]`. Our $125 is a *lifetime* (full-curve) figure, not 1-year, so it
isn't apples-to-apples — but it implies **materially above-median monetization**. That is plausible for an
aggressive hard-paywall funnel with $40–63 recurring prices, but it is itself an **optimistic input**. This
is why I treat the low / AI-stress cases as the prudent planning numbers, not the base.

---

## 1. Bottom-up funnel reconciliation — 1,000 signups/day → net revenue

### 1a. The conversion chain (per day)

| Stage | Tag | Low | **Base** | High | Basis |
|---|---|---|---|---|---|
| Quiz-starts ("signups") | GIVEN | 1,000 | **1,000** | 1,000 | Brief |
| × Quiz-start → complete | ASSUMPTION | 45% | **60%** | 75% | 35-step quiz = long/health-funnel end; commitment↑ but completion↓ `[02-market §2a]`. No public quiz-completion % → my band. |
| × Complete → paywall-view | ASSUMPTION | 85% | **92%** | 97% | Plan-reveal → email capture → price screen; small drop before price. Not separately benchmarked → my band. |
| × Paywall-view → purchase | BENCHMARK | 8% | **10.7%** | 13% | RevenueCat hard-paywall D35 **10.7% median**; Noom quiz-completer→paid **>10%** `[02-market §3a]`. |
| **= Buyers/day** | | **30.6** | **59.1** | **94.6** | product of the above |
| Implied quiz-start→paid | | 3.1% | **5.9%** | 9.5% | cross-check vs Noom ~5–6% start→paid ✓ |

Base: `1,000 × 0.60 × 0.92 × 0.107 = 59.1 buyers/day`.

### 1b. Net value per buyer

| Input | Tag | Low | **Base** | High | Basis |
|---|---|---|---|---|---|
| Blended net LTV (pre-refund) | GIVEN ±band | $115 | **$125** | $135 | Our Part D model; ±8% for horizon/upsell/mix uncertainty. |
| Refund haircut | BENCHMARK | 7% | **5%** | 3% | Education apps run the **highest** refund rate **~5.1%** `[02-market §3d]`; band = country/quality spread. |
| **= Net LTV/buyer (post-refund)** | | **$106.95** | **$118.75** | **$130.95** | LTV × (1 − refund) |

*Upsells:* the 2 checkout upsells are **unquantified upside** here (no take-rate/price given — not inventing
data). Any positive attach rate pushes the base up; treat §1's output as an **upsell-free floor**.
*Store cut:* base is **web-billed** (the whole point of a web-to-app funnel is dodging the 15–30% store cut
`[02-market §2c]`), so only the 12% processor applies and it's already in the $125. App-store distribution is
modeled as a separate downside in §3c — **not** double-counted here.

### 1c. Net revenue

```
Daily net rev = buyers/day × net LTV/buyer
  Low :  30.6 × $106.95 = $ 3,273/day  → × 365 = $1.19M/year
  Base:  59.1 × $118.75 = $ 7,014/day  → × 365 = $2.56M/year
  High:  94.6 × $130.95 = $12,385/day  → × 365 = $4.52M/year
```

**Base case ≈ $7.0K/day → ~$2.56M/year net. Range ~$1.2M – $4.5M.**

The ~3.8× spread from low to high comes almost entirely from the **conversion chain** (funnel) and the
**LTV/refund** block moving together — i.e. the answer is dominated by *how many people convert* and *how
long they stay*, which is exactly the fragility the rest of this memo quantifies.

---

## 2. AI-churn-premium downside (stress scenario)

**The finding [BENCHMARK]:** AI-powered apps earn **+41% revenue/payer but churn ~30% faster**; annual
retention **21.1% (AI) vs 30.7% (non-AI)** `[02-market §3b]`. This is *the* most Jobescape-relevant benchmark —
"Duolingo for AI" is precisely the profile that monetizes hot and retains poorly.

**Don't double-count the +41%.** Jobescape's recurring prices ($40–63) are already aggressive — the +41%
monetization is *baked into our $125*. So the stress applies **only the churn side** to that LTV.

**Decompose the blended $125 into retention-independent vs retention-dependent value:**
```
Blended intro (period 1) = 0.10×$6.93 + 0.70×$19.99 + 0.20×$39.99 = $22.68 gross
  × 0.88 (processor)                                              = $19.96 net  ≈ $20  (retention-independent)
Recurring tail net = $125 − $20                                  = $105        (retention-dependent)  → 84% of LTV
```

**Apply the churn premium to the tail.** LTV of a recurring stream ∝ average lifetime ∝ 1/churn
`[02-market §3e, Reforge LTV≈ARPU×margin/churn]`. Cross-check that "30% faster" and "21% vs 31% annual" agree:
```
Non-AI: 30.7% annual retention → monthly churn 9.4% → avg life 1/0.094 = 10.7 mo
AI    : 21.1% annual retention → monthly churn 12.2% → avg life 1/0.122 =  8.2 mo
Ratio of monthly churn 12.2/9.4 = 1.30  ✓ (consistent with "+30% faster")
Tail scales × (1/1.30) = 0.77
```
```
Stressed tail = $105 × 0.77 = $80.8
Stressed blended LTV = $20 + $80.8 = $100.8   (≈ $101)
Δ = −$24.2/buyer  =  −19% of blended LTV
```

**Flow it through the base funnel (59.1 buyers/day, 5% refund):**
```
Stressed net LTV/buyer = $100.8 × 0.95 = $95.8
Daily  = 59.1 × $95.8 = $5,654/day
Annual = $5,654 × 365 = $2.06M/year
Δ vs base = $2.56M − $2.06M = −$0.50M/year  (−19%)
```

> **AI-churn stress alone erases ~half a million dollars of annual net revenue** (−19%), moving the base
> from **$2.56M → $2.06M**. And if our $125 LTV was itself built on a *non-AI* retention curve, then **$101
> is the truer base** and the whole headline should recenter on ~$2.06M — the optimistic-input risk in §0.

---

## 3. Refund + regulatory / chargeback drag

### 3a. Refund sensitivity (already partly in the base)
At base scale, `buyers/yr = 59.1 × 365 = 21,558`. Each **1 point** of refund on a $125 LTV costs
`21,558 × $1.25 = $26.9K/year`.
```
0% refund → $2.70M      5% (base, education benchmark) → $2.56M   (−$135K)
7% refund (quality/geography stress)          → $2.51M   (−$189K)
```
Refunds are a **real but second-order** drag (~$135K at base) — an order of magnitude smaller than the
**~$500K churn drag** in §2. That ordering is itself a strategic finding: *retention >> refund* as a lever.

### 3b. Chargebacks (worse than refunds)
A chargeback costs the **refunded amount + a $15–25 network fee**, and a chargeback ratio **>~1% risks
App-Store/processor suspension** `[02-market §3d, §5c]`. Treat as **+0.5–1pt effective** on top of refunds in
stress (~+$15–30K/year) plus a **non-linear platform-suspension tail risk** that dwarfs the direct cost.

### 3c. Store-cut downside (why staying web-billed matters)
Base assumes web billing (12% processor). If a share **S** of the ~$105 recurring tail routes through app
stores at 30%, the incremental drag is `(0.30 − 0.12) × S × $105 × 21,558`:
```
S = 50% of tail  → $204K/year      S = 100% of tail → $408K/year
```
**Keeping billing on web is worth ~$0.2–0.4M/year.** This is a design decision, not a market force —
a concrete reason to keep the paywall and renewals on web.

### 3d. Regulatory / ARL tail risk (low-probability, high-severity)
The *exact* Jobescape playbook is under active FTC litigation (**FTC v. Genesis, June 2026**) and California
ARL enforcement (**HelloFresh $7.5M settlement**; CART task force) `[02-market §5a–b]`. Can't be point-
estimated, but two revenue-equivalent anchors show the asymmetry:
- **Forced easy-cancel** that lifts voluntary churn toward the AI-stress level ≈ the **−$0.50M/year**
  recurring hit from §2 (same mechanism, applied by regulation instead of product).
- **A settlement at HelloFresh scale ($7.5M) ≈ ~2.9× the entire base-case annual net revenue** — a single
  one-off that wipes out ~3 years of the business.

The vacatur of the FTC Click-to-Cancel rule (8th Cir., July 2025) was **procedural, not on the merits**, and
the FTC reopened rulemaking Jan 2026 `[02-market §5a]` — this risk is dormant, not gone.

---

## 4. Strategic conclusion — front-loaded, fragile, and why retention is the moat

### 4a. Why the economics are front-loaded and fragile
- **Front-loaded on the retention curve:** **84% of the $125 LTV is the recurring tail**, and for AI apps
  that tail collapses fast (avg life ~8 months, §2). Almost all realizable value sits in the **first handful
  of billing cycles**; there is little durable annuity behind it.
- **Cash-timing makes it worse.** Day-1 cash per cohort ≈ `59.1 × ($20 intro × 0.95) ≈ $1,120/day` — only
  **~16%** of the day's booked LTV. The other **~$5,900/day is unrealized at acquisition and hostage to the
  curve.** Commitment is front-loaded (35-step quiz, paid before value is delivered); the **cash is realized
  slowly over a fragile back-end** you don't yet control.
- **Three simultaneous compressors** all squeeze the same tail: AI-churn premium (**−$0.50M/yr**), education-
  high refunds (**−$135K/yr base**), and ARL/FTC tail risk (**one-off up to ~2.9× annual revenue**). Stack
  them and the prudent planning number is the **low-to-AI-stress band (~$1.2–2.1M), not the $2.56M base.**

### 4b. Retention is a bigger, safer lever than the funnel — quantified
**LTV sensitivity to churn** (around the AI baseline of 12% monthly), applied to the stressed tail:
```
−1pt churn (12% → 11%): avg life 8.33 → 9.09 mo (+9.1%)  → +$7.4/buyer  → +$158K/year
−2pt churn (12% → 10%): avg life 8.33 → 10.0 mo (+20%)   → +$16/buyer   → +$348K/year
```
**A 1–2pt monthly-retention improvement is worth ~$160–350K/year** — on its own it **exceeds the entire
refund drag** and materially offsets the AI-churn premium.

**Compare the funnel lever:** +1pt paywall conversion (10.7% → 11.7%) = +5.5 buyers/day = **+$239K/year** —
genuinely powerful, *but*: (i) hard paywalls are already near the conversion ceiling `[02-market §3a]`, (ii)
squeezing conversion harder raises exactly the **refund / chargeback / ARL** risks in §3, and (iii) it's a
one-time multiplier. **Retention compounds** — it lengthens every cohort's tail, forever, and Jobescape
starts from the *weak AI-retention baseline*, so it has the **most headroom and the least risk**.

### 4c. The moat, and the highest-ROI lever
- **The Challenge (Part C) is an economic instrument, not a feature.** Its job is to buy back the AI-churn
  premium — a habit loop / streak / outcome-proof mechanism (Duolingo's playbook `[02-market §3f]`) that
  pushes monthly churn from ~12% back toward the ~9% non-AI level. Each point it recovers is worth ~$160K/yr
  and re-rates the whole LTV.
- **Transparency + easy-cancel is the *same* lever from the other side.** It (i) cuts the ~$135K refund drag
  and the chargeback/suspension tail, (ii) defuses the FTC-Genesis/ARL existential risk (turning §3d from a
  liability into a trust position — the "uncrowded honest middle" `[02-market §4]`), and (iii) tends to *raise*
  voluntary retention. The regulatory risk and the retention opportunity are the **same $0.5M/year, addressed
  by the same move.**
- **Highest-ROI economic lever: retention, delivered through the Challenge + a transparent/easy-cancel
  posture.** The funnel is already optimized and legally exposed; the tail is where the money, the headroom,
  and the moat all are. **Defend the tail, don't squeeze the funnel.**

---

## Numbers to carry into Parts C & D
| Quantity | Value |
|---|---|
| Base buyers/day (range) | **59** (31 – 95) |
| Base net revenue/day (range) | **$7.0K** ($3.3K – $12.4K) |
| **Base net revenue/year (range)** | **$2.56M** ($1.19M – $4.52M) |
| AI-churn-stress annual net rev / Δ | **$2.06M** / **−$0.50M (−19%)** |
| Blended LTV split | intro **~$20 (16%)** / recurring tail **~$105 (84%)** |
| Refund drag (base 5% / per point) | **−$135K/yr** / **$27K per point** |
| Store-cut downside (50–100% of tail) | **$0.2M – $0.4M/yr** |
| Value of a **1–2pt** monthly-retention gain | **+$160K – $350K/yr** |
| Value of a **1pt** paywall-conversion gain | **+$239K/yr** (but near ceiling, higher risk) |
| ARL/FTC settlement anchor | **$7.5M ≈ 2.9× base annual net rev** |

---

## Sources
All external benchmarks are drawn from and cited against `research/02-market.md`, which carries the primary
URLs. Key sources used here:
- **RevenueCat State of Subscription Apps (2025 & 2026)** — hard-paywall D35 10.7%; AI apps +41%/payer &
  ~30% faster churn (21.1% vs 30.7% annual retention); median churn 13–14%; annual realized LTV/payer ~$26.
  https://www.revenuecat.com/state-of-subscription-apps/ · https://www.revenuecat.com/state-of-subscription-apps-2025
- **Adapty / Business of Apps** — subscription-app refund rates 2–5%; **education highest ~5.1%**; app-store
  15–30% cut. https://adapty.io/blog/refund-rate-metrics-and-benchmarking/ · https://www.businessofapps.com/data/app-refund-rates/
- **Web2App World (Noom teardown)** — quiz-completer→paid >10%; funnel psychology & upsell stack.
  https://web2appworld.com/breakdowns/noom/
- **FunnelFox web-funnel trends (311 funnels)** — web-vs-in-app split, intro-pricing/upsell architecture,
  web purchase→download 90–95%. https://blog.funnelfox.com/web-funnels-insights-and-trends/
- **Reforge** — LTV ≈ (ARPU × gross margin) / churn; LTV/CAC & payback norms.
  https://www.reforge.com/guides/calculate-ltv-cac-and-payback-period
- **Regulatory:** FTC v. Genesis (TechCrunch, June 2026); 8th Cir. Click-to-Cancel vacatur (Cooley/Sidley,
  July 2025); FTC revival ANPRM (Crowell, Jan 2026); California ARL / HelloFresh $7.5M (Benesch).
  https://techcrunch.com/2026/06/17/ftc-lawsuit-reveals-how-subscription-scam-networks-evade-app-store-enforcement/ ·
  https://www.beneschlaw.com/insight/a-dozen-new-lawsuits-and-two-7-5m-settlements-signal-a-new-era-for-automatic-renewal-compliance/
- **Duolingo (retention north-star):** FY25 shareholder letter; Duolingo Max monetization.
  https://www.sec.gov/Archives/edgar/data/1562088/000162828026012246/q4fy25duolingo12-31x25shar.htm

**Assumption ledger (my estimates, not benchmarked):** quiz-start→complete 45/60/75%; complete→paywall-view
85/92/97%; LTV ±8% band; refund 3/5/7% band around the 5.1% education benchmark; store-cut share S
illustrative. All flagged inline. The two **benchmarked pins** doing the heavy lifting are **paywall→purchase
10.7%** and **AI churn +30% / 21% vs 31% retention**.
