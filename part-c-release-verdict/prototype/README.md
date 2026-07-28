# Challenge v2 — the daily gate

**Live:** https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/

A working prototype of the next release of Jobescape's **Challenge** feature.
Part C, Task 4 of the Nomad Venture Studio Product Manager take-home.

React + Vite, built in Jobescape's own design language so it reads as a feature of the
product rather than a mockup of one. Every step has its own URL:

| Step | What it shows |
| --- | --- |
| [`#/commit`](https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/#/commit) | pick the daily time |
| [`#/today`](https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/#/today) | **the gate** — one day open, tomorrow locked |
| [`#/work`](https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/#/work) | the first win |
| [`#/done`](https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/#/done) | a result you keep |
| [`#/tomorrow`](https://alyasska.github.io/Nomad_Venture_Studio_TA_C4/#/tomorrow) | the gate opens |

The **Why this screen** panel on the right carries the finding behind each step. Every
figure comes from a BigQuery analysis of 9,956 paying subscribers, re-derived by a
91-assertion verification harness.

## The problem it fixes

The Challenge's hypothesis was *"one day = one skill builds a habit of returning every
day."* Nothing in the shipped feature holds a day back — so **27.1%** of the people who
finished the "7-day" challenge finished it in a single sitting, and **45.8%** within two
days. The raw +38pt D1 engagement gap that made the feature look like a success was
entirely selection; four independent tests came back null.

**v1 never tested its own hypothesis.** This prototype makes one day one day.

## How it improves the Challenge in the next release

1. **The first ten minutes produce one kept result.** 44.9% of starters complete zero
   lessons and 50.2% never complete one anywhere in the product. `#/work` pre-loads three
   real tasks and ends with something saved to the user's library — the win arrives before
   the user has to supply any motivation of their own.
2. **The habit engine actually switches on.** A day that cannot be opened early is the
   difference between a 7-day challenge and a 7-lesson course. The countdown is the
   product's promise that tomorrow exists and has something in it.
3. **The feature becomes measurable.** v1 shipped to 100% with no hold-out and no
   `challenge_day_unlocked` / `challenge_day_missed` events. A gate creates those events,
   so the next release can be judged on evidence rather than on a selection-inflated
   D1 number.

## On gamification

Jobescape's academy uses a streak counter and level badges. This prototype borrows the
**design language** — the blue, the rounded cards, the staggered lesson path — but not that
mechanic. The buyer is 59.7% male and 58–60% aged 45+, and the under-25s who respond best
to streaks churn at 31.1%. The slot where the streak pill sits now counts the days the
product has opened for you. The reward is competence, not celebration.

## Running it

```bash
npm install
npm run dev      # http://localhost:5173/Nomad_Venture_Studio_TA_C4/
npm run build    # -> docs/, which is what GitHub Pages serves
```

```
src/
  App.jsx                  app shell, step routing
  screens/                 the five steps
  components/              sidebar, day path, mentor, evidence panel
  state/useChallenge.js    localStorage-backed state + countdown + draft stream
  state/useHashRoute.js    deep links
  data/challenge.js        the seven days, the tasks, the verified figures
  styles/tokens.css        Jobescape design tokens
```

State persists to `localStorage` — the gate survives a refresh, which is the point of a
gate. **Reset demo** in the top bar clears it.

## The one thing that's faked

The AI draft streams from a scripted string in `src/data/challenge.js`, because a static
page cannot hold an API key. It looks identical to a live call. To make it real, replace
`DRAFT` and the interval in `useTypewriter` with a fetch to your own backend proxying the
Claude Messages API:

```js
const r = await fetch('/api/tutor', {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ task }),
})
// then pipe r.body into the draft exactly as the scripted stream does
```

Everything else — the gate, the countdown, the seven-day path, task selection, saving to
the library, the reminder, persistence — is real.
