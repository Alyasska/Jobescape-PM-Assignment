# ORCHESTRATION — running this take-home with AI agents

How to split the assignment across AI agents, what each needs, what a human must do first,
and the order to run them. Deadline **2026-07-28 23:59** (today 2026-07-24 → ~4.5 days).

## The dependency map

```
                 HUMAN-ONLY INPUTS (do these first — agents can't)
   ┌──────────────────────────────────────────────────────────────┐
   │ H1 Download 3 Drive folders (creatives, quiz answers, events) │
   │ H2 Walk funnel + PAY + screenshot product   (Part A/C need it)│
   │ H3 Pull BigQuery exports → part-c/data/*.csv (Part C needs it)│
   └──────────────────────────────────────────────────────────────┘
        │              │                    │                 │
        ▼              ▼                    ▼                 ▼
   ┌─────────┐   ┌───────────┐        ┌───────────┐     ┌──────────┐
   │ Part D  │   │  Part B   │        │  Part A   │     │  Part C  │
   │ LTV +   │   │ Competitor│        │ Segments +│     │ Analytics│
   │ A/B     │   │ research  │        │ gap       │     │ +verdict │
   │ (no dep)│   │ (web only)│        │ (H1,H2)   │     │ +v2      │
   └────┬────┘   └─────┬─────┘        └─────┬─────┘     └────┬─────┘
        │              │                    │                │ Task 4
        │              │                    │                ▼
        │              │                    │           ┌──────────┐
        │              │                    │           │ Prototype│
        │              │                    │           │ builder  │
        │              │                    │           └────┬─────┘
        └──────────────┴─────────┬──────────┴────────────────┘
                                 ▼
                          ┌─────────────┐
                          │  Synthesis  │  → deliverable/SUBMISSION.md
                          │  + QA agent │
                          └─────────────┘
```

**Start Part D and Part B immediately — neither is blocked on human inputs.**
Part A is blocked on H1+H2. Part C is blocked on H2+H3.

## Agent roster

| Agent | Part | Blocked on | Tools it leans on | Output |
|-------|------|-----------|-------------------|--------|
| **LTV Modeler** | D | — | Bash/Python (or a sheet) | `part-d/01-ltv-model.md`, `02-ab-test-model.md`, `model/*.py` |
| **Competitor Scout** | B | — | WebSearch/WebFetch | `part-b/01,02,03.md` |
| **Audience Analyst** | A.1 | H1, H2 | Read materials, vision | `part-a/01-segments.md` |
| **Gap Analyst** | A.2 | H2 (+A.1) | product walkthrough notes | `part-a/02-product-gap.md` |
| **Data Analyst** | C.1 | H3 | Bash/Python on CSV exports (or BQ SQL) | `part-c/01-analytics.md`, `sql/*.sql` |
| **Verdict Writer** | C.2–C.3 | C.1 | reasoning | `part-c/02-verdict.md`, `03-whats-next.md` |
| **Prototype Builder** | C.4 | C.3 | vibe-code (Claude Code / v0 / Lovable) + deploy | `part-c/prototype/`, live URL |
| **Synthesis + QA** | all | everything | Read all parts | `deliverable/SUBMISSION.md` |

## How to actually launch them (in this Claude Code session)

- **One part at a time (recommended):** use the `Agent` tool with `subagent_type: "general-purpose"`,
  and in the prompt tell it to read `BRIEF.md`, `CLAUDE.md`, and its part's `PLAN.md`, then produce
  the named output files. Independent parts (D, B) can be launched in the **same message** to run in parallel.
- **Bigger fan-out (optional, opt-in):** a `Workflow` can pipeline Part C (analytics → verdict →
  prototype) or run a competitor-per-agent sweep for Part B. Only do this if Aliaskar asks for it —
  it spends a lot of tokens.
- **Verify the numbers.** Part C and Part D are the parts that get you hired or dinged. After the
  modeling/analytics agent finishes, run a second independent agent to **re-derive the key numbers
  from scratch** and flag any mismatch before it goes in the submission.

## Suggested schedule (~4.5 days)

- **Day 1 (today):** H1 downloads + H2 funnel/pay/screenshot. Launch **Part D** and **Part B** agents in parallel (unblocked). Start H3 BQ pull.
- **Day 2:** Finish H3. Run **Part A** (Audience + Gap). Run **Part C.1 Data Analyst** on the exports.
- **Day 3:** **Part C.2–C.3** verdict + v2. Start **Part C.4 prototype**. Independent re-check of D and C numbers.
- **Day 4:** Finish + deploy prototype. **Synthesis + QA** into `deliverable/SUBMISSION.md`. Proofread against `BRIEF.md` task-by-task.
- **Day 5 (buffer / 28th):** Final polish, attach CV, request the $15.19 refund LAST, submit to @islam_s10.

## Guardrails
- Nothing ships a number without the calculation shown next to it.
- Each part answers the brief's sub-questions **explicitly** (the brief punishes "restating" and rewards decisions).
- Keep the paid subscription ACTIVE until Part A.2 and Part C.4 are fully done (see credentials.md).
