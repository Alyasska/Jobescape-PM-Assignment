# Presentation storyboard

Arc = **punchline-first, one thesis, one slide per part.** ~11 slides, ~10 min. Every slide states the
claim big, then the evidence. All numbers below are final — verified by
[`part-c-release-verdict/analysis/05_qa.py`](../part-c-release-verdict/analysis/05_qa.py) (91 checks).

| # | Type | Slide | Punchline | The one number on it |
|---|---|---|---|---|
| 1 | cover | **Title** | Jobescape: the Challenge, the audience, the economics | — |
| 2 | section | **The thesis** | "You've built an excellent machine for selling a product you haven't finished building." | **50.2%** of paying subscribers never complete a single lesson |
| 3 | content | **Part A · Who's actually buying** | Older and more loyal than the internal read — and the ads that promise income buy the churn | **60%** are 45+ · largest cell = **men 55+ (21.3%)** · churn falls monotonically with age (31.1% → 9.5%) |
| 4 | content | **Part A · The gap = the risk** | The acute risk isn't slow content — it's the **price-and-refund gap** → refunds, chargebacks, FTC-Genesis exposure | **11.3%** of unsubscribes are payment failures, chargebacks or disputes |
| 5 | content | **Part B · The competitive truth** | The content is *free* and the funnel is *cloned* → win on scaffolding, feedback, accountability | Take the **rhythm**, leave the confetti |
| 6 | content | **Part B · What to take** | 5 steals, ordered **de-risk → retain → differentiate → diversify → expand** | Mimo's paywall: **+100%** trial opt-in, **−25%** early cancels |
| 7 | **the money slide** | **Part C · Verdict: no** | "Your dashboard says this release won. It didn't." | **39.8%** (what the dashboard shows) vs **+0.5 pts, p = 0.82** (the real effect) |
| 8 | content | **Part C · Why** | It never tested its own hypothesis — there is no daily gate | **27%** of finishers did the whole "7-day" challenge in one sitting |
| 9 | section | **Part C · Prototype (demo)** | The daily gate, built — "put this in front of five 50-year-olds on a Tuesday" | live demo, 3–4 min |
| 10 | stat | **Part D · Economics** | Blended net LTV ≈ $125; the upgrade test pays off above ~5% → run it | break-even **4.9%** · validated plan mix (10.2 / 64.6 / 25.1) |
| 11 | section | **The recommendation** | Instrument → mechanic → first ten minutes → quality → **reach last** | and the one ask: **a hold-out group on the next release** |

## Notes for build time

- **Slide 7 is the whole presentation.** Build it as a two-number reveal: show 39.8% vs 26.0% first
  and let the room conclude "success," then reveal the matched control at 59.6% vs 60.0%. The reversal
  is the demonstration of thinking the brief is grading — don't bury it in a table.
- **Slide 3 needs the age×gender crosstab as a visual**, because it's where I disagree with the team's
  own read. Deliver it as agreement-then-correction, not as a gotcha: gender is right, age is a decade off.
- Slide 9 is a *demo*, not bullets — one line and the live prototype.
- If short on time, the must-haves are **2, 7, 8, 9, 11** (thesis → verdict → why → demo → ask).
- **Anticipated Q&A to prep:**
  - *"How confident are you that D1 didn't move?"* → four independent tests, all null; the tightest is
    stratified on activity level and flat in four of five strata.
  - *"Isn't 11% reach the real problem — why not just promote it?"* → CSAT falls as engagement rises
    (3.74 → 3.10). Scaling reach on 3.25-star content scales refunds. Quality before reach.
  - *"What ships first?"* → the day gate and the 45%-do-zero-lessons bug hunt. Both are small; the
    reminder infrastructure already exists in the Automation tab and just isn't wired to the Challenge.
  - *"What if the Challenge was never meant to be a retention feature?"* → then judge it on refunds and
    ticket volume, and my verdict changes. It's my first question for the team.
