# Part A · Task 1 — audience segments

## How these were produced

**Derived, not asserted.** k-modes clustering (Huang 1998) over **38,071 quiz respondents × 10
categorical answers**, from the 210 MB quiz export (49,528 respondents; 38,071 answered at least 6
of the 10 core questions). Hamming distance, per-attribute modes, unanswered kept as its own level,
seeded, 4 restarts per k. Reproduce with `analysis/cluster_quiz.py`.

**Why k-modes and not k-means** — a mean over nominal levels ("35–44", "Business owner") has no
meaning. One-hot + Euclidean silently asserts that every pair of levels is equidistant, which is
exactly the assumption being tested.

> ### The honest headline: there is no elbow.
> Within-cluster cost per user falls smoothly across k = 2 … 8 — 5.09, 4.79, 4.67, 4.49, 4.40,
> 4.31, 4.20 — with no knee. **This population is a continuum, not a set of natural kinds.** Six is
> a resolution chosen and defended, not a count the data forced. Any segmentation of this audience
> is a decision about granularity, and should be presented as one.

## The six segments

| Segment | Who they are | Share | Strongest signal (lift vs population) |
|---|---|---|---|
| **The Striver** | senses a gap and is closing it deliberately — growth-motivated, 45–54, male-skewed | 28.4% | "somewhat ready, could be behind" **1.9×** · growth-motivated 1.6× |
| **The Latecomer** | the oldest buyers, hasn't started, watching the field move without them | 22.0% | "falling behind as others move faster" **2.2×** · never used Claude 1.9× · 55+ 1.4× |
| **The Adept** | already gets real value from AI and wants more leverage — female-skewed | 20.9% | "AI already helps me a lot" **2.5×** · confident 2.5× · female 1.7× |
| **The Optimiser** | mid-career professional using Claude on real work, wants speed | 12.3% | aged 35–44 **2.6×** · work tasks 1.4× · already uses Claude 1.3× |
| **The Founder** | learning AI to build something of their own | 9.0% | "start my own business" **3.1×** · female 2.2× |
| **The Switcher** | between jobs, changing direction, starting from zero | 7.4% | "exploring options" **4.4×** · hasn't tried AI 2.3× |

Names follow one pattern deliberately — six agent nouns — so they read as a set and stay memorable
in a room. Each is a **runnable quiz filter**, not a persona sketch: every segment above can be
reconstructed from answers the funnel already collects.

## What this replaced, and what changed

The first version of this analysis was a hand-written rule chain (`segment_sizer.py`): six segments
authored from a jobs-to-be-done framework, then counted, with unmatched respondents falling through
to a default bucket — which is why one segment came out at 38.7%. **The clustering did not validate
it.**

| | Finding |
|---|---|
| **Did not survive** | "Gen Z / Early Striver" — 18–24 never separates as a cluster. "Burned Time-Poor Doer" — no cluster at any k. |
| **Was missing entirely** | **The Adept (20.9%)** — already competent, female-skewed. The largest group the framework failed to imagine, and commercially the most interesting: a retention-and-expansion audience, not a fear-relief one. |
| **Was cut on the wrong variable** | the sharpest single signal in the data is `work_status = "exploring options"` at **4.4× lift** — a *status* variable. The old taxonomy cut that group by *age*, so it dissolved. |

## Limits

- `sub` / `unsub` / `upsell` are **all zero** in this export, so segments cannot be profiled by
  conversion here. Buyer-side demographics come from `subscribe_events` in BigQuery (n = 9,956) and
  are unaffected — see `02-product-gap.md` and Part C.
- No elbow means the cluster boundaries are soft. Treat shares as indicative of *mix*, not as hard
  memberships.
- k-modes is sensitive to initialisation; 4 restarts per k with a fixed seed makes this run
  reproducible, not globally optimal.
