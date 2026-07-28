# Part C · Tasks 3 & 4 — "Challenge" v2: Manufacturing Streak-Grade Commitment from Day 1

**Feature under redesign:** Jobescape's *Challenge* — the course delivered as a **7-day challenge, one AI skill per day** (Day 1 = documents, Day 2 = Excel, …). App = "Duolingo for AI" with an AI-chatbot tutor.
**Target metric:** D1 retention (did they come back on Day 2?). **Secondary:** unsubscribe rate, lesson completion, D3, D7, CSAT.
**Evidence base (do not re-derive):** `research/05-challenge-science.md` (behavioral science) and `research/04-competitors-indirect.md` (competitor mechanics). Cited inline as **[05 §x]** and **[04 §x]**. Primary sources are named where a magnitude carries weight.

---

## 0. The one strategic problem this v2 exists to solve

Duolingo's streak is powered by **loss aversion on accumulated investment**, and it only bites **after ~7 days** — a 7-day streak learner is **2.4×** more likely to return the next day (Duolingo) / **3.6× more likely to complete the course** (Duolingo blog) **[04 §1.2, 05 §4.1]**. The loss-aversion engine *needs a streak to already exist* before it produces retention.

**Jobescape's funnel breaks that assumption.** It is **paywall-first**: Meta ad → quiz → paywall → *payment* → only then does the habit begin **[04 intro, §1.2]**. On Day 1 there is **no accumulated investment to protect** — the streak engine is running on empty for exactly the days (1–3) where drop-off is highest.

So the entire v2 has one job: **bridge the "fear → habit handoff."**

| Phase | What actually drives return | The asset we have | The gap to close |
|---|---|---|---|
| **Day 0 (paywall)** | *Fear + aspiration* from the quiz ("AI will make me obsolete," "I want the promotion") + money just spent | **Sunk cost** — the only commitment asset that exists yet | Convert a one-time purchase into a daily obligation |
| **Day 1** | Manufactured commitment: sunk-cost reframe + an *endowed* streak (already 2/7) + a real first win | A tangible AI output + a non-empty progress bar | Give the user something *to protect* by end of session 1 |
| **Days 2–3 (the danger zone)** | Small-streak loss aversion (weak) + anchored prompt + insurance | A 1–2 day streak (fragile) + the Day-2 Excel cliff | Survive the difficulty spike before the streak is strong enough to bite |
| **Days 4–7** | Loss aversion now self-sustaining + investment loop (personalized to *their* job) | A substantial streak + accumulating personalization | Hand off from extrinsic fear to intrinsic habit + identity |

Every mechanic below is scored on how well it closes a specific gap in that handoff. **Fear gets them to Day 1; endowed progress + early wins build the thing they fear losing; by Day 7 the streak and a new identity ("I'm someone who uses AI at work") carry them without the fear.**

---

## (A) v2 SPEC — prioritized mechanics

**Scoring:** Impact (expected pull on **D1**, the target, then secondaries) × Effort (build cost; lower = cheaper). Ranked by Impact ÷ Effort. Primary metric each mechanic owns is in bold.

| # | Mechanic | Primary metric | Impact | Effort | Priority |
|---|---|---|---|---|---|
| 1 | Anchored daily prompt + escalating D1/D3/D7 re-engagement | **D1**, unsub | 5 | Low | P0 |
| 2 | Engineered Day-1 "aha win" + peak-end close | **D1**, CSAT, completion | 5 | Med | P0 |
| 3 | Endowed-progress streak ("Day 1 of 7 — already started") | **D1**→D2, D7 | 4 | Low–Med | P0 |
| 4 | Sunk-cost / commitment-device reframe (the paywall-first bridge) | **D1**, D3 | 4 | Low | P0 |
| 5 | Streak-freeze / insurance (protect the fragile early streak) | **unsub**, D3 | 3 | Low–Med | P1 |
| 6 | AI-tutor daily accountability check-in | **completion**, D3/D7, CSAT | 3 | Med | P1 |
| 7 | Variable-reward + investment loop | **D3/D7**, completion | 3 | Med–High | P2 |
| 8 | 3-day & 7-day milestone reward chests (*useful* rewards) | **D7**, completion | 2 | Low–Med | P2 |

---

### 1. Anchored daily prompt at a user-chosen time + escalating re-engagement — **P0, moves D1**
**What it is.** In onboarding, capture the user's preferred daily time ("When will you do your 5-min AI workout? ☀️ morning / 🌤 lunch / 🌙 evening") and, per Calm's post-first-session pattern, lock it in immediately after the Day-1 win. Fire a Fogg-style prompt at that anchor every day. If they lapse, **escalate the copy, not the volume**: Day-1 miss = gentle reminder → Day-3 = restate the *value*/what they'll lose → Day-7 = win-back. Use the mascot/tutor voice so it reads as a character, not spam.
**Behavioral evidence.** ≥1 push in first 90 days ≈ **~3× retention**; 95% of never-messaged opted-in users churn (Pushwoosh) **[05 §3.4]**. Fogg B=MAP: **no prompt → the Day-2 behavior structurally cannot fire** **[05 §1.1]**. Duolingo "protects the channel" and optimizes timing/copy over volume; escalates emotional intensity after ~3 inactive days **[04 §1.4, 05 §4.1]**.
**Handoff role.** This is the *cue* that carries the user across the Day-1→Day-2 gap before any habit exists. It's the single biggest early-retention lever and the cheapest — ship it first.

### 2. Engineered Day-1 "aha win" + peak-end close — **P0, moves D1 + CSAT**
**What it is.** Design Day 1 so every user produces a **tangible, genuinely impressive AI output within the first session** (target **<10 min to value; first meaningful interaction inside 60–90s**). End on a deliberate **peak** (the "wow, the AI actually wrote that") + a Fogg **celebration** (confetti, streak flame) + a **variable-reward teaser** of tomorrow. Then empirically find which Day-1 action best predicts D7/paid retention and optimize the first session toward it.
**Behavioral evidence.** Activation is the leading indicator of retention — Amplitude: **69% of top 7-day-activation performers were top 3-month retainers**; >30-min-to-value ≈ **~3× abandonment** **[05 §3.1, §3.3]**. Peak-End Rule: experience judged by peak + ending, and the peak encodes the memory that decides whether they return (NN/g) **[05 §5.1]**. Fogg: "emotions create habits" **[05 §1.2]**.
**Handoff role.** Manufactures the *thing to protect*. Fear got them to open Day 1; the win gives them a reason to respond to tomorrow's prompt. Without a real win, the streak is protecting nothing.

### 3. Endowed-progress streak — "Day 1 of 7, you've already started" — **P0, moves D1→D2 return**
**What it is.** Present a **7-tick progress bar that starts non-empty**: signup + finishing the quiz = the first 1–2 ticks already filled. Frame every day as *protecting built progress* ("Don't break your streak — you're 2/7 in"), not starting from zero. Show the streak flame + a calendar view.
**Behavioral evidence.** **Endowed Progress Effect** (Nunes & Drèze 2006, *JCR*): a car-wash card pre-stamped with 2 "free" stamps completed at **34% vs 19%** for the same real effort — **~1.8×** **[05 §1.4]**. Loss aversion + Duolingo's streak-extension animation alone lifted new-learner D7 **+1.7%** **[04 §1.2]**.
**Handoff role.** This is the mechanism that gives a **Day-1 user a streak to lose** — collapsing Duolingo's "wait 7 days" into "you already have 2." It is the literal answer to the paywall-first constraint.

### 4. Sunk-cost / commitment-device reframe — the paywall-first bridge — **P0, moves D1 + D3**
**What it is.** Turn the money already spent into a daily obligation. (a) A **commitment screen** immediately post-paywall: quiz-goal mirrored back + an explicit, effortful pledge ("I'm committing to the 7-Day AI Challenge to [their quiz goal]") + tap-to-confirm — a Cialdini commitment device. (b) Reframe copy so the *purchase* is the sunk cost the streak protects ("You've invested in this — finish the 7 days to make it pay off"). (c) Optional light public pledge ("share you started the challenge"). Avoid 75 Hard-style "restart from zero" — too punitive for paid B2C **[05 §4.3]**.
**Behavioral evidence.** Cialdini commitment & consistency — effortful/public commitments drive consistent behavior **[05 §1.5]**. Matthews goal study: **65%** who shared goals + reported progress completed vs **35%** who only thought about them **[05 §5.4]**. Goal-based onboarding repeatedly tied to higher early retention **[05 §3.5]**.
**Handoff role.** This is the *only* commitment asset that exists at Day 0 (§0). It carries the user through Day 1 while endowed progress + the first win build the real streak.

### 5. Streak-freeze / insurance — protect the fragile early streak — **P1, moves unsubscribe + D3**
**What it is.** Grant one **earned** "streak freeze" (framed as earned by completing Day 1, so it feels self-invested, not gifted) so a single missed day doesn't cascade into an unsubscribe. Surface it exactly when at risk (the Day-3 danger zone). Keep the softer Duolingo model, not all-or-nothing restart.
**Behavioral evidence.** Streak freeze reported to cut churn **~21%** for at-risk users; doubling equipped freeze capacity raised relative DAU **+0.38%** (Duolingo) **[05 §1.5, 04 §1.2]**.
**Handoff role.** The early streak (1–2 days) is too small for loss aversion to bite hard, so one bad day can kill it. Insurance keeps the fragile streak alive until Days 4–7 when it's strong enough to self-sustain.

### 6. AI-tutor daily accountability check-in — **P1, moves completion + D3/D7 + CSAT**
**What it is.** Use the *existing chatbot* as a proactive coach, not a passive Q&A box. Each day it: recaps yesterday's win, **adapts today's difficulty** to how the user did, asks for a one-tap progress commitment, and does the practice *with* them (feedback on their attempt). Make the tutor the **practice surface** — the place you *do the work and get feedback* — which is the one thing free ChatGPT/YouTube structurally can't offer against you **[04 §3.2, §2.3]**.
**Behavioral evidence.** AI-tutor arm improved performance **~15 percentile points** (Dartmouth 2025); AI nudge check-ins reduce dropout by reminding + adapting difficulty **[05 §5.3]**. Accountability + progress reporting nearly doubles completion (Matthews) **[05 §5.4]**. Brilliant proves "learn by doing, no video" commands a premium; Duolingo Max (paid GPT tutor) is the fastest-growing tier **[04 §2.3, §1.5]**.
**Handoff role.** Carries the *intrinsic* side of the handoff — accountability + mastery feedback that builds the "I can do this" identity as the extrinsic fear fades.

### 7. Variable-reward + investment loop — **P2, moves D3/D7 + completion**
**What it is.** Close the two weakest links in the Hooked loop. **Variable reward:** make each day's payoff non-predictable — surprise "bonus prompt packs," a mystery skill unlock, tutor praise that varies, occasional chests. **Investment:** make finishing Day N *materially improve* Day N+1 — the user saves their AI outputs into a personal "prompt library," the tutor personalizes tomorrow to *their job/quiz answers*, so switching cost and relevance both rise each day.
**Behavioral evidence.** Eyal's Hooked: variable reward sustains engagement far better than fixed; investment raises switching cost and improves the next loop — and these are the Challenge's two weakest links **[05 §1.3]**. Reward *mastery/progress*, tie rewards to real value (Duolingo chests give useful items) to avoid the **overjustification effect** (Deci et al., 128 studies) **[05 §5.1]**.
**Handoff role.** The investment loop is what makes the streak *worth* protecting for a real reason (a growing personal toolkit), completing the shift from fear to genuine value by Day 7.

### 8. 3-day & 7-day milestone reward chests — **P2, moves D7 + completion**
**What it is.** Reward chests at the 3-day and 7-day tiers with **useful** rewards (a premium prompt pack, a "custom GPT for your role," a certificate) — not just confetti. Mirrors Duolingo Streak Society tiers **[05 §4.1, 04 §2.5]**.
**Behavioral evidence.** Streaks *combined with milestones* correlate with 40–60% higher DAU vs streaks alone (vendor magnitude) **[05 §4.2]**; tie rewards to value to avoid overjustification **[05 §5.1]**.
**Handoff role.** Gives the mid-week (D3) and finish-line (D7) a concrete payoff so the streak isn't abstract.

---

## (B) 7-DAY REDESIGN — skill → guaranteed win → next-day hook

**Design rules applied to every day:** (1) single learning objective (micro-learning) **[05 §2.2]**; (2) 5–10 min, first interaction <90s (Fogg-Ability) **[05 §1.1, §3.3]**; (3) a guaranteed early win engineered so *everyone* succeeds with a pre-loaded example (kills the blank-page problem); (4) peak-end close + a **cliffhanger hook** that plants curiosity about tomorrow (variable reward); (5) the AI tutor does the practice *with* them.

| Day | Skill | Guaranteed early win (engineered) | Next-day hook |
|---|---|---|---|
| **1** | **AI for Documents / Writing** | Type one line ("follow-up email to a client who missed a deadline") → tutor returns a polished draft in ~15s. Universal, zero-setup, instant "the AI actually wrote that." **This is the aha (§A2).** | "Tomorrow: make the spreadsheet you dread build its own formulas — just by asking. **No more Googling VLOOKUP.**" (reframes Day 2 as *relief*, not challenge) |
| **2** | **AI for Excel / Spreadsheets** — *the difficulty cliff* | On a **pre-loaded sample dataset**, user asks in plain English ("which region sold most?") → tutor returns the **copy-paste-ready formula + the answer**, one-tap insert. Win in <60s, no syntax typed. | "Tomorrow: turn your 47-email inbox into a 3-line summary + drafted replies in 2 minutes." |
| **3** | **AI for Email & Inbox** | Paste a messy thread → tutor summarizes + drafts a reply in the user's tone. **3-day milestone chest unlocks.** | "Tomorrow: never take meeting notes again — AI does it and assigns the action items." |
| **4** | **AI for Meetings** | Paste a transcript/notes → tutor returns summary + owner-tagged action items. | "Tomorrow: turn a rough idea into a full slide deck outline." |
| **5** | **AI for Presentations / Slides** | One-line topic → tutor returns a structured deck outline + speaker notes. | "Tomorrow: read a 20-page report in 90 seconds and pull the 3 things that matter." |
| **6** | **AI for Research & Analysis** | Paste/upload a long doc → tutor returns TL;DR + key risks + questions to ask. | "Tomorrow: assemble everything into *your* personal AI workflow — and graduate." |
| **7** | **Capstone — Build Your AI Workflow** | Tutor helps assemble the week's outputs into a saved **personal prompt library / role-specific "custom GPT."** **7-day chest + certificate. Peak-end of the whole challenge.** | Graduation → transition to the ongoing product / next challenge; identity reflected back ("You're now someone who uses AI at work"). |

### Defusing the Day-2 (Excel) difficulty cliff — the make-or-break for D1 retention
Day 2 is structurally the worst D1-retention moment: **the highest-friction, most-intimidating, least-universal skill meets the smallest possible streak (1 day).** An unmanaged difficulty spike breaks flow and is a documented Day-2/3 drop-off cause **[05 §5.2]**. Nine concrete moves:

1. **Re-scope the objective from "learn Excel" to "make Excel stop scaring you."** Position AI as *removing* the fear of spreadsheets, not adding a hard new skill. Emotional frame: *"You'll never fear a spreadsheet again."* (Ability up via motivation reframe, Fogg B=MAP **[05 §1.1]**.)
2. **Pre-load a sample dataset.** No one brings their own file — kills setup friction and the blank-page problem, the top time-to-value killer **[05 §3.3]**.
3. **Guarantee a <60s win:** plain-English question → formula + answer returned instantly. First success before any chance to feel lost.
4. **Zero syntax burden:** copy-paste-ready formulas, one-tap "insert." User never types `=VLOOKUP(...)`. (Maximize Ability.)
5. **Make Day 2 the *shortest* lesson of the week** — lowest ability cost on the hardest-*feeling* day.
6. **Warm the cliff from Day 1's close** (the hook above): pre-frame Day 2 as relief so users arrive expecting rescue, not difficulty.
7. **Over-reward the hardest day:** an extra variable-reward/bonus on Day-2 completion, so effort ↔ reward stays balanced right where drop-off spikes **[05 §1.3, §5.1]**.
8. **AI-tutor extra hand-holding on Day 2:** proactive check-in, offers a worked example first, adapts down if the user stalls **[05 §5.3]**.
9. **Relevance off-ramp, not a dead end:** for the minority who genuinely never touch spreadsheets, offer a one-tap swap ("Don't use Excel? Do *AI for Email* instead") — "this doesn't apply to me" is a real churn reason; branch it rather than lose them. Default stays Excel.

---

## (C) PROTOTYPE SPEC — buildable in a few hours (Lovable / Cursor / Claude-code)

**Goal of the prototype:** make the **fear→habit handoff tangible and testable** — demonstrate that we can manufacture a streak-grade commitment and a real "aha" win on Day 1, before any habit exists. Mobile-first single-page app; local state (localStorage); one real AI call for the wow.

### Screens

**1 — Onboarding / Commitment** (the paywall-first bridge, §A3+A4)
Components: quiz-goal echo ("Your goal: *get promoted by using AI*"), the **7-tick progress bar pre-filled to 2/7** with an "already started ✅" caption (endowed progress), a **daily-time picker** (☀️/🌤/🌙), and an **explicit commitment button** ("I commit to the 7-Day AI Challenge"). Sets the tone: you already have something to protect.

**2 — Challenge Home** (the loss-aversion surface, §A3+A5)
Components: **streak flame + counter**, the **7-day node path** (Day 1 active, Day 2 "warmed" with the relief teaser, Days 3–7 locked), **today's lesson card** (CTA "Start Day 1 · 5 min"), a visible **streak-freeze token** ("1 freeze — earned by finishing Day 1"), and the next-reward chest at Day 3.

**3 — Daily Lesson + AI-Tutor Practice** ← **THE ONE CORE INTERACTIVE FLOW**
This screen carries the whole thesis. Day-1 "documents" lesson: a 1-sentence teach, then the **tutor practice box**. User types a real task ("write a follow-up email to a client who missed a deadline") → **a real, streamed AI response appears** (the tutor as practice surface, §A6). This single flow demonstrates time-to-value, the aha win, and the tutor-as-practice-surface in ~30 seconds. Components: tutor chat bubble, input box with a pre-filled example prompt (one-tap to run — guarantees the win), streaming output, "Save to my prompt library" (the investment loop, §A7).

**4 — Completion Celebration** (peak-end, §A2)
Components: **confetti + streak animation** incrementing 2→3, a "You just did X" recap (the peak), **variable-reward reveal** (a bonus prompt pack), and the **Day-2 cliffhanger hook** ("Tomorrow: make Excel build its own formulas — no more Googling VLOOKUP"). This is the emotional high that decides whether they return.

**5 — Day-2 Hook / Notification** (the return cue, §A1 + cliff defusal §B)
Components: a **mock push-notification overlay** at the chosen time ("🔥 Keep your 2-day streak — Day 2 is ready"), and the **reframed Day-2 open screen** ("You'll never fear a spreadsheet again") with the pre-loaded dataset. Demonstrates the anchored prompt + the Day-2 cliff defusal without needing real push infrastructure.

### Build vs fake
- **Build for real:** the commitment/onboarding flow, the streak + endowed-progress + freeze UI and its persisted state (localStorage), the lesson→practice→celebration loop, the Day-2 hook screen. These *are* the hypothesis.
- **One real AI call:** wire the Day-1 practice to a live LLM (e.g., Claude API) so the "aha" is genuine — this is the whole point of the tutor. Fall back to a **scripted streamed response** if no key at demo time (looks identical).
- **Fake / stub:** real push notifications (use the in-app mock overlay in Screen 5), Days 2–7 full content (locked cards + only the Day-2 open screen), auth, payment, backend, analytics.

### How this prototype improves the next release *(required by the brief)*
The prototype converts the v2 from a document into a **testable artifact aimed at the single riskiest hypothesis: that we can manufacture streak-grade commitment on Day 1 before any habit exists.** Concretely it lets the team, before engineering commits a sprint: (a) **usability-test** the commitment + endowed-progress framing and confirm the Day-1 aha lands in <10 min; (b) **A/B the exact copy** of the endowed-progress message ("2/7 already started") and the Day-2 relief reframe with real users; (c) **validate the tutor-as-practice-surface** produces a genuine "wow" fast enough to move D1; and (d) give design/eng a **shared clickable reference** so they build the same thing. It de-risks the D1 lever and turns "we think this will retain" into "we measured that it does" — the fastest path to knowing whether the fear→habit handoff actually works.

---

## Sources
All claims trace to the two prior research files, which carry the primary URLs:
- `research/05-challenge-science.md` — Fogg B=MAP, Endowed Progress (Nunes & Drèze), Hooked loop, loss aversion, streak freeze, peak-end, activation→retention (Amplitude), time-to-value, push/notification lift, AI-tutor nudges, Matthews accountability study, overjustification.
- `research/04-competitors-indirect.md` — Duolingo first-party streak data (3.6× completion, +14% D7 wager, +1.7% D7 animation, +0.38% DAU freeze), notification bandit/escalation, Max = paid AI tutor, Brilliant "learn by doing," the paywall-first constraint framing.
