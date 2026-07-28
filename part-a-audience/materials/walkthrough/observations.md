# Product walkthrough — first-hand observations (from screenshots, 2026-07-27)

*Captured from Aliaskar's own paid-account screenshots (agent can't store the images; this preserves the evidence). Tag: [SEEN] = directly observed in-product.*

## Paywall [SEEN]
- "Start Learning Claude today with **61% intro offer!**" + a **09:46 countdown timer** (manufactured urgency).
- Promises (bullets): "Build real projects – websites, apps, and more" · "50+ bite-sized lessons & step-by-step personal plan" · "**Personal AI mentors and 24/7 support chat**" · "**+7 AI tools**: CV & Portfolio builder and more".
- Plans shown: **1 Week $6.93** (→ $38.95/4wk) · **4 Weeks $15.19 "Most popular"** (→ $38.95/4wk) · **12 Weeks $25.99** (→ $66.65/12wk).
- Fine print: converts to a 4-week sub at $38.95 unless cancelled; "**I can cancel through the Manage Subscription tab in my account settings.**"
- **Gaps/notes:** (a) prices here **differ from `part-d/data/plans.csv`** (real dynamic/61%-off pricing). (b) Cancellation has a **self-serve "Manage Subscription" tab** — nuances the reviews' "bot-only cancel" claim (that likely refers to *refunds*, not cancel). (c) Sets up the "24/7 chat" and "personal mentor" promises tested below.

## The "Personal AI mentor" = a fake persona named "Mark" [SEEN]
- Chat opens: "Hi there! I'm **Mark** — your mentor here at Jobescape," with a **stock-photo human face**. Suggested prompts: "What should I do today?", "Recap last week", "What's next in my plan?". A floating "**Ask Mark**" button sits on every page.
- **Gap:** the promised "personal AI mentor" is an **AI bot dressed as a named human ("Mark")**. Reinforces the reviews' authenticity/"anonymous team, AI-generated" theme. Concrete, quotable.

## AI Chat is credit-limited [SEEN]
- `ai-chat`: "How can I help you?", model selector = **Claude**, **"5 credits"** shown top-right; quick actions (Give advice, Brainstorm, Translate, Summarize, Explain simply, Write copy).
- **Gap:** "**24/7 support chat**" (paywall) is really a **metered 5-credit** AI chat, not unlimited support.

## Product is freelancing/monetization-flavoured [SEEN]
- **Assistants** → first tab is **Freelancing** (CV transformer "Turn resumes into freelancer CVs", Employment, Interview, Personal bio); then Marketing, Copywriting.
- **Apps** → 7Art (image/video/music gen), CV builder, + IT tools (Auto QA, Debugger, SQL Query Writer, Log Summarizer).
- Cross-sell everywhere: "Master Claude AI and **turn your skills into real money**", "your own AI Music", CV builder.
- **Confirms** the identity split (Part A2): the product leans **freelancing/income**, matching the app title "Launch and Elevate Your Freelancing Career with AI."

## Retention mechanics that ALREADY exist (important for Part C) [SEEN]
- **Automation** tab: "**AI agent in WhatsApp**" (Active), "**Motivational messages** — start each day with a motivating message to your WhatsApp", "**Study progress reminder** — personalized study-progress reminders". (Also an off-topic "weather reminder.")
- **Challenges** + **Academy** both show a **streak** already: a 🔥 counter ("0 days"), and a **Mon–Sun weekly streak tracker** with a 1→7 slider.
- **⇒ Part C correction:** a streak and a reminder channel **already exist**. So the v2 isn't "add a streak" — it's **fix the streak that isn't working** (it sits at 0): make the reminder *default + anchored + escalating* (today it's WhatsApp opt-in), and add **endowed progress + Day-1 win + freeze** so the streak has something to protect. Re-frame the v2 write-up accordingly.

## The Challenge feature, confirmed [SEEN]
- `/challenges`: "**Your daily challenges** — Pick a challenge, build real projects every day, and **unlock your certificate when you finish.**" **7 Day / 14 Day** toggle. Streak "0 days".
- Tracks (each **7 lessons · 15 min/day**): Claude Basics, Sales, Claude for Project Managers, **Claude for Excel**, Claude for Marketing, Claude for Developers, Claude for Accounting, AI Filmmaking, AI Video Creation. (Challenge **338** in the brief is one of these.)
- **Confirms:** the 7-day / one-lesson-a-day / certificate-on-completion design **exactly** matches Part C. Certificate-on-completion ties to the **refund-gate** finding. Many role-specific tracks = the Challenge is a *platform*, not one feature.

## Personal plan / Academy is a real structured curriculum [SEEN]
- Example plan "**Claude Code for Developers**" (8%): modules Foundations → Core Workflow → Work Automation → External Services; lessons like "Write good prompts", "Plan mode and verification", "Hooks and enforcement", "Subagents and teams", "Agent SDK", "Capstone"; **Bronze/Gold/Platinum** levels.
- **Nuance for A2:** at least this plan is **substantial and current** (mentions Claude Code, MCP, subagents) — more than the reviews' flat "shallow" claim. The depth likely varies by track; worth saying the content isn't uniformly thin.
