# Handoff — Part C, Task 4 (the prototype) · для нового агента

**You are helping Aliaskar Bekishev finish one task of a Product Manager take-home for Nomad
Venture Studio (Jobescape).** Everything else in the assignment is done and verified. This
session is *only* Part C Task 4 — the working prototype — plus getting it publicly hosted.

> ## ⏰ HARD CONSTRAINT: the deadline is **2026-07-28, 23:59**.
> This handoff was written at **16:30 on 2026-07-28** — roughly **7 hours left**.
> There is a working prototype and a complete submission already. **Your job is to improve and
> publish, never to rebuild.** If you have to choose between a bigger idea and a shipped link,
> ship the link. Read "Priority order" below and work strictly top-down.

---

## 1. What the brief literally asks for

Verbatim from `BRIEF.md`, Part C:

> ### Task 4. Prototype
> Based on Task 3, build a **working prototype** — vibe-code it in any tool (Lovable, Replit,
> Cursor, Claude Code, v0, etc.).
> A polished product/perfect design isn't needed — a working prototype showing the essence of
> the idea and the core flow.
> Attach:
> - a **link** to the prototype,
> - an explanation of **how exactly** the prototype would improve the challenge in the next release.

Two deliverables: **a link** and **an explanation**. Both must be reachable by a reviewer who has
only the submission email. That is the bar. Design polish is explicitly *not* the bar.

---

## 2. Where things stand

**The prototype exists and works.** `index.html` in this folder — one self-contained file,
~35 KB, no build step, no external requests, no dependencies. Open it in a browser and it runs.

It demonstrates **the daily gate**: the mechanic the shipped Challenge never had. Five screens
(`s-commit`, `s-today`, `s-work`, `s-done`, `s-tomorrow`), a screen switcher at the bottom, and a
notes panel that annotates each screen with the finding that produced it.

**The problem it has right now:** the published link is a **private claude.ai artifact**
(`https://claude.ai/code/artifact/ae28930b-…`). Private by default. Unless Aliaskar shares it
manually, **a reviewer clicking that link sees nothing** — and Task 4 scores zero despite the work
being done. That is the single biggest risk in the entire submission and it is why this session
exists.

Read `README.md` in this folder first — it documents the five screens, the design rationale, and
the one thing that is faked.

---

## 3. The evidence base — numbers you may use

**Every number in the prototype's annotations is real and verified.** They come from a BigQuery
analysis of 9,956 paying subscribers, re-derived by a 91-assertion harness
(`../analysis/05_qa.py`). **Do not invent, round, or "improve" any figure.** If you need a number
that isn't listed here, find it in `../01-analytics.md` or the analysis scripts, or leave it out.

| Finding | Figure |
|---|---|
| Starters who complete **zero** lessons | **44.9%** (≈45%) |
| Finishers who did the whole "7-day" challenge in **one day** | **27.1%** |
| …within two days | **45.8%** |
| Lesson 1 → 2 survival | **50.3%** |
| Starters who returned for a **second challenge day** | **36.8%** |
| Never completed a lesson **anywhere in the product** | **50.2%** |
| Challenge CSAT vs the same users' CSAT elsewhere | **3.25 vs 3.45** |
| Buyers who are male | **59.7%** |
| Buyers aged 45+ | **57.8%** (60.1% including a legacy bucket) |
| Under-25 unsubscribe rate | **31.1%** |

**The core verdict this prototype answers:** the Challenge's raw +38pt D1 gap was **entirely
selection**. Four independent tests all came back null. The mechanism: *no daily gate exists*, so
the "7-day" challenge could be binged in one sitting — **v1 never tested its own hypothesis.**

---

## 4. Priority order — work strictly top-down

### P0 · Publish it. (~30–45 min) — **do this before anything else**
Nothing else matters if the link is dead. Get it on GitHub Pages, verify the public URL loads in a
fresh browser context, then update the link everywhere (§6). **Once this is done the task is safe**
and everything below is upside.

### P1 · Make the prototype match the plan's own priority order (~1 h)
This is the highest-value *content* fix, and it is a real inconsistency a sharp reviewer will spot.

`../03-whats-next.md` orders the v2 work: **Phase 0** instrument → **Phase 1** fix the first ten
minutes → **Phase 2** build the daily gate → Phase 3 quality → Phase 4 reach. Phase 1 is ranked
first because it lands on a **primary** business metric and 45% of starters complete zero lessons.

But the prototype **leads with the gate (Phase 2)**. Screen 3 does cover Phase 1.2 (the pre-loaded
guaranteed win), but the framing puts the second-priority fix first.

Fix by **reframing, not rebuilding**: lead the page and the notes with "45% of starters finish
nothing — so the first ten minutes must produce one kept result; *then* the gate makes it a habit."
The screens can stay in the same order; the argument has to match Task 3. Cheap, and it makes
Tasks 3 and 4 read as one coherent piece of thinking.

### P2 · Persist state across reloads (~20 min)
`var state = { day: 1, saved: [], hour: 8, minute: 30 }` lives in memory only. **The one mechanic
being demonstrated — a gate that holds a day back — resets the moment you refresh.** Put `state`
in `localStorage`, and add a clearly-labelled "Reset demo" control so a reviewer can start over.
Small change, removes an obvious hole.

### P3 · Show the instrumentation (~40 min)
Phase 0 of the plan says v1's fatal flaw was that it shipped at 100% with no hold-out and no
`challenge_day_unlocked` / `challenge_day_missed` events — it was **unmeasurable**, which is how it
got away with never testing its hypothesis.

Add a toggleable panel that prints the analytics events as the user triggers them
(`challenge_day_unlocked`, `challenge_day_missed`, `lesson_completed`, `result_saved`, …). It makes
the prototype argue Phase 0 as well as Phase 2 — "this version can be measured; v1 couldn't." Low
risk, purely additive, and it is the kind of detail that reads as PM maturity rather than decoration.

### P4 · Put the explanation on the hosted page (~20 min)
The brief requires the explanation **attached to the link**. Right now it lives in `README.md` and
the deck. On GitHub Pages the README renders in the repo, not on the site — so make sure the
explanation is either on the page itself (the notes panel, expanded) or one obvious click away.

### P5 · Check it on a real phone width (~10 min)
It is a phone-framed UI. Verify at 390 × 844 that nothing overflows and the countdown is legible.

---

## 5. Do NOT do these

- **Do not rebuild the prototype.** It works. You have hours, not days.
- **Do not add gamification** — no streak flames, badges, confetti, or progress rings. This is a
  deliberate, evidence-backed decision: the buyer is 59.7% male and ~58% aged 45+, and the under-25s
  who respond to those patterns churn at 31.1%. An earlier version *was* gamified and was replaced
  after the data came in. The restraint is part of the argument.
- **Do not make the AI draft "real."** It streams from a scripted string because a static page
  cannot hold an API key. This is disclosed in `README.md`, which is the honest thing to do. Do not
  add a "paste your API key" field — never ask a reviewer for a credential.
- **Do not invent numbers.** See §3.
- **Do not touch anything outside this folder** unless it is the link update in §6.

---

## 6. Publishing — GitHub Pages

### 🔒 Safety rule, read before running any git command

**This project folder is NOT a git repo, and most of it must never be published.** It contains:

- `00-context/credentials.md` — **a live BigQuery password** (gitignored, keep it that way)
- `part-c-release-verdict/data/*.csv` — **~10k rows of real production user records** with
  `user_id`, age, gender, country. Publishing these would leak the company's user data.
- `part-a-audience/materials/` + product screenshots — a paid account's UI

**Therefore: create a brand-new, separate repo containing only the prototype.** Do not
`git init` in the take-home root. Do not copy the folder and delete things afterwards.

```bash
SRC=~/Tuki-Tuki/Work_space/Nomad-Venture-Studio-TA/part-c-release-verdict/prototype
DEST=~/jobescape-challenge-v2-prototype

mkdir -p "$DEST" && cd "$DEST"
cp "$SRC/index.html" "$SRC/README.md" .      # ← these two files ONLY
touch .nojekyll                              # serve the file as-is

git init -b main
git add -A
git status                                   # ← EYEBALL THIS. Only index.html, README.md, .nojekyll.
git commit -m "Challenge v2 prototype — the daily gate the shipped feature never had"
gh repo create jobescape-challenge-v2-prototype --public --source=. --push
```

Then **Settings → Pages → Deploy from a branch → `main` / `(root)` → Save**. The UI path is more
reliable than the API. Give it a minute, then the URL is:

```
https://alyasska.github.io/jobescape-challenge-v2-prototype/
```

*(`gh` is already authenticated on this machine as **Alyasska** with `repo` scope — verified
2026-07-28. `gh repo create … --public --push` will work without an extra login step.)*

**Verify it in a private/incognito window before declaring it done** — that is the whole point of
this session. A link that only works while you are logged in is the bug we are fixing.

### One judgement call for Aliaskar to make
The prototype's annotations quote Jobescape's internal engagement metrics. A public repo puts those
on the open internet. This is normal for a take-home — they asked for a shareable link, and the
numbers are their own metrics shown back to them — so the recommendation is **proceed**. But it is
his call, and worth asking once. (GitHub Pages from a *private* repo requires a paid plan.)

### After publishing — update the link in all 6 places
The old artifact URL `ae28930b-c340-4970-9f2c-6d3c7ae7a693` appears in:

| File | Note |
|---|---|
| `part-c-release-verdict/prototype/README.md` | line 3 |
| `deliverable/SUBMISSION.md` | **two** places (body + the links table) |
| `deliverable/report/sections/05-partC-challenge.md` | source of the PDF dossier |
| `deliverable/report/report.html` | regenerate via `deliverable/report/build.py` |
| `build_deck_html.py` | ~line 598 — then rebuild: `python3 build_deck_html.py --pdf` |

After rebuilding the deck, re-run the audits from `presentation/`:
`check_overflow.py`, `check_accent.py`, `check_diagram_fit.py`, `check_images.py` — all four must
pass. They are fast and they catch layout regressions the eye misses.

---

## 7. Definition of done

- [ ] A **public URL** that loads the prototype in a fresh incognito window
- [ ] The **five-screen flow** works end to end at desktop and phone width
- [ ] The gate survives a page refresh (P2)
- [ ] The **explanation of how it improves the challenge** is reachable from the link (P4)
- [ ] The framing matches Task 3's priority order (P1)
- [ ] The new URL replaces the artifact link in all 6 files, deck + dossier rebuilt
- [ ] Every number on the page still matches §3

---

## 8. Read these, in this order

1. `README.md` *(this folder)* — the five screens, the design rationale, what's faked
2. `index.html` *(this folder)* — the prototype itself; JS starts ~line 532
3. `../03-whats-next.md` — Task 3, the plan the prototype is "based on". **Phases and the
   pre-registered success criteria are the spine of P1.**
4. `../02-verdict.md` — why v1 failed, and the kill rule
5. `../01-analytics.md` — where every number comes from
6. `../../BRIEF.md` — the assignment, if you need the wider framing
7. `../../CLAUDE.md` — working conventions (defensible claims, no invented data, label assumptions)

---

## 9. Working conventions for this repo

- **Every claim is defensible.** State assumptions explicitly; a labelled assumption is fine, a
  hidden one is not.
- **Don't invent data.** If an input is missing, write `> ⚠ BLOCKED: needs <input>` and continue.
- **Secrets stay in `00-context/credentials.md`** (gitignored). Never paste the BigQuery password
  anywhere, and never into the new public repo.
- **On-brand angle:** Jobescape sells "use AI at work." Using AI agents to do this assignment well
  is a feature, not a cheat — it is noted in the submission.

---

## 10. Environment notes

- This machine has **no pandas/numpy** — the analysis is pure standard-library Python. Keep it that way.
- **Never screenshot a full multi-slide document in one headless-Chrome capture.** A 1920×50000
  capture (~96 megapixels) crashed this laptop mid-session. Render one 1920×1080 view at a time, or
  use DOM-only probes.
- `gh` CLI is the expected tool for GitHub operations.
