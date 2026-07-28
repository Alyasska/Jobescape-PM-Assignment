# Appendix

## A — Jobescape quiz funnel, full decode (quiz_version v7.0.8)

Reconstructed from `api.funnel.jobescape.me/constructor/quiz-node/` — 37 pages, one branch (`used_ai` Yes/No). Questions and the variable each writes:

| # | Section | Question | Options | Writes |
|---|---|---|---|---|
| 0 | — | Have you ever used Claude? | Yes / No → **branch** | `used_ai` |
| 2 | Profile | I want to learn Claude for… | Work / Personal / Growth | `why_claude` |
| 3 | Profile | Current work status? | Full-time / Freelancer / Business owner / Between jobs / Exploring | `status` |
| 4 | Profile | How old are you? | 18-24 / 25-34 / 35-44 / 45-54 / 55+ | `age` |
| 5 | Profile | Gender identity? | Female / Male / Skip | `gender` |
| 6 | Profile | How would learning Claude benefit you? | Promotion / Work faster / Confidence / Start business / Earn more | `goal` |
| 8 | Challenges | Rate your experience with AI so far | Great / Good-but / Frustrating / Haven't tried | `experience_ai` |
| 9 | Challenges | Ready for how AI is changing careers? | Need skills fast / Bit worried / Somewhat / Confident | `skills_competitive` |
| 10 | Challenges | **What scares you most about AI and your career?** | Replaced by AI-savvier peer / Falling behind / Losing opportunities / Nothing | `career_scares` |
| 12 | Challenges | I create documents/reports regularly | 1–5 scale | `often_create` |
| 13 | Challenges | **Used AI to write, then spent as long fixing it?** | Every time / Sometimes / No / Haven't | `long_fix` |
| 14 | Challenges | What would change with polished docs in 2 min? | 3× content / stop procrastinating / look pro / strategy | `polished_documents` |
| 16 | Challenges | Had an app idea but couldn't build it? | Yes / No | `idea_app` |
| 17 | Challenges | What stopped you? | Can't code / dev too expensive / gave up / didn't know start | `app_stoppers` |
| 18 | Challenges | Possible to build an app without coding? | No / Maybe w/ AI / Yes | `app_without` |
| 20 | Personalization | How do you prefer to learn? | Own pace / Set deadlines | `prefer_learn` |
| 21 | Personalization | Time to dedicate to your goal? | 10 / 20 / 30 min / 1 hr per day | `time_goal` |
| 22 | Personalization | Approach that works best? | 80% theory / 80% practice | `approach_best` |
| 23 | Personalization | Include projects in a portfolio site? | Yes / No | `coding_experience` |
| 24 | Personalization | Want an AI mentor to guide you? | Yes / No | `ai_mentor_prefer` |
| 26 | Personalization | Would an AI certification help your career? | Definitely / Probably / No | `certification_advantage` |
| 28 | Personalization | What kept you from advancing before? | No plan / fear waste time / too busy / too confusing | `stopped_before` |
| 31 | — | Email capture | — | `email` |
| 32 | — | Name capture | — | `name` |
| 34–35 | Sell | Selling page + "chase" offer | — | paywall |

**Interleaved teasers (the persuasion layer):** FOMO cards after the `used_ai` branch; *"There is nothing to worry about"* (+ Harvard "humans with AI will replace humans without AI") after `career_scares`; *"Create polished content"* after the document pain; *"Building an app has never been this easy"* after the app-build pain; a certificate teaser; an "AI profile" reveal; and a fake-progress loader before the paywall. Full raw map: `part-a-audience/materials/quiz-map.md`.

## B — Reproducibility

- **Quiz decode:** open funnel constructor API (no auth); 37 nodes pulled and parsed → `quiz-map.md` + `quiz-nodes-raw.json`.
- **Economics:** `part-d-economics/model/ltv_model.py` reads `data/plans.csv`, prints both horizon readings and the A/B scenarios.
- **Research:** 10 sourced agent reports (5 broad + 5 deep, incl. product-reality from public reviews) under `research/`; every external claim carries a URL in the underlying files.
