# External Inputs — what to pull, where it goes, status

Everything the task depends on that lives outside this repo. Check items off as gathered.

| # | Input | Source | Lands in | How | Status |
|---|-------|--------|----------|-----|--------|
| 1 | Ad creatives | [Drive folder](https://drive.google.com/drive/folders/1g2re4islAXTyjZwMGazMl0PI-t9nfBDo) (owner islam.shintemirov@) | `part-a-audience/materials/ad-creatives/` | Manual download (see note) | ☐ |
| 2 | Quiz funnel answers | [Drive folder](https://drive.google.com/drive/folders/1NOnAg-e13vvh0HaS0M2TQ1MMBqK0xmcy) | `part-a-audience/materials/quiz-funnel-answers/` | Manual download | ☐ |
| 3 | Quiz funnel (live) | http://jobescape.me/chat-v3?quiz_version=v7.0.8 | screenshots → `part-a-audience/materials/` | Walk it yourself; screenshot every step | ☐ |
| 4 | Product (paid) | Paywall after funnel | notes → `part-a-audience/` | **Pay** (get refund via @islam_s10), record email in credentials.md | ☐ |
| 5 | Events convention | [Drive folder](https://drive.google.com/drive/u/0/folders/1QXWw3ZMwNavYohuE4GdNvsjMxH2osqYd) | `part-c-release-verdict/` | Manual download — needed to read app_events/subscribe_events | ☐ |
| 6 | BigQuery exports | `persona-496908` (creds in credentials.md) | `part-c-release-verdict/data/` | Run SQL in console → export CSV | ☐ |
| 7 | Challenge feature (live) | https://app.jobescape.me/skills/challenges/338?source=skills | screenshots → `part-c-release-verdict/` | Walk it yourself | ☐ |
| 8 | Challenge design | [Figma](https://www.figma.com/design/w0O2ryFP52hITEPqmqlKSn/Challenges?node-id=0-1) | notes | Inspect flows | ☐ |
| 9 | Pricing table | Notion brief | `part-d-economics/data/plans.csv` | ✅ already extracted | ☑ |

## Note on Drive downloads
The three Drive folders are shared but owned by `islam.shintemirov@gmail.com`. The connected
Google Drive tool can read folder *metadata* but the API would not enumerate their children
(shared-but-not-added folders aren't indexed for search). Two easy fixes:
- **Option A (fastest):** open each link in a browser signed in as lyasskar@, "Add shortcut to Drive"
  (or just download the folder as ZIP), and drop the files into the target folders above.
- **Option B:** once the folders are added to your Drive, re-run the Drive tool listing and they'll enumerate.

Whoever/whatever downloads them: keep original filenames, and add a one-line `_index.md` in each
`materials/` subfolder noting how many creatives / how many quiz-answer records there are.
