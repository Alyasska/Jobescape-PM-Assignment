# How this was done

The brief grades quality of thinking, and it is on-brand for a company teaching "use AI at work" to see AI used well. So this ran as a small research operation rather than a single sitting — and, more importantly, with a rule that every number had to survive being checked.

## Three passes

**Broad research.** Five parallel agents swept the field in three directions: the science of habit formation and adult learning; the social picture of AI-at-work anxiety and reskilling; and the market — AI-upskilling edtech, the quiz-funnel model, and competitors direct and indirect. Each returned a sourced report with confidence flags.

**Synthesis.** The reports were cross-read to find the one thesis connecting all four parts, and to pick which threads justified going deeper.

**Deep dives.** Four focused agents: two competitor teardown sets, a Challenge v2 and prototype design, and a funnel economics model.

## Two things built directly, not researched

**The quiz funnel was decoded end to end.** Rather than clicking through 37 screens, the funnel's public constructor API was queried to reconstruct every page, question, answer option, the variable each answer writes, and the single branch point. That is primary evidence for Part A, not observation.

**The subscription economics were modelled from scratch** over the three plans, and cross-checked against the plan mix actually observed in the data.

## How the numbers are kept honest

This is the part that matters most, so it is stated plainly.

**Part C runs on one BigQuery export.** Five queries produced the data; `13_comparison_groups.sql` returns one row per paying subscriber, takers and non-takers alike — 9,956 rows. Three earlier queries were written against an assumed schema, superseded once the real schema was probed, and are shipped as-is with their `⚠ADJUST` markers, because they are the honest record of the working.

**The analysis is six Python scripts**, pure standard library. One settles the questions that had to be answered *before* the engagement tiers were chosen — where the retention curve breaks, how much observation window exists, whether challenge 338 really is "the Challenge". The others produce the release analysis, the supplementary tests, and the cohort baselines.

**Every published figure is re-derived and asserted.** `05_qa.py` recomputes 91 numbers straight from the raw CSVs and fails loudly if any documented figure has drifted. It exists because these numbers had to survive being copied into four places — analysis notes, this dossier, the deck, the submission — and hand-copying is where quiet errors live. It has already earned its keep: it caught a 59.557% that had been rounded to "59.5%" and propagated to eight files.

**Part A's segments were derived, not asserted.** The first version was a hand-written rule chain — six segments authored from a jobs-to-be-done framework, then counted. It was coherent and unfalsifiable: the structure came from the analyst, so no data could contradict it. It was replaced with k-modes clustering over 38,071 respondents. The clustering rejected two of the six, and surfaced one real segment the framework had missed entirely. That result is reported in full in Part A, including the part that is inconvenient.

## Evidence standards

Every external claim carries a source, and figures from secondary aggregators or vendor blogs are flagged as softer than primary data. Assumptions are stated rather than buried, particularly in the economic model. Where a claim rests on internal data, the script that computes it is named. Where the data cannot answer a question — most importantly whether the Challenge release was causal, which no observational dataset settles without a hold-out — that is said plainly rather than papered over.
