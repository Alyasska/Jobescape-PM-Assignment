# Presentation

**Deck:** [`Jobescape-PM-Deck.html`](Jobescape-PM-Deck.html) — one self-contained file, 1920×1080 per
slide. Open in any browser and press F11. A print-ready [`PDF`](Jobescape-PM-Deck.pdf) sits beside it.
**Presenter reference:** [`Jobescape-Presenter-Reference.pdf`](Jobescape-Presenter-Reference.pdf) — the
datasheet to hold while presenting: one entry per slide with the data, the argument, the proof and
the likely questions. Source: [`SPEAKER-REPORT.md`](SPEAKER-REPORT.md); rebuild with
`python3 build_speaker_report.py`.

**41 slides — 28 main, 13 appendix. ~30 minutes.**

## Structure

The deck walks the assignment's **eleven tasks in the brief's own order**. Slide 2 is a contents page
mapping every task to its slides; slide 28 restates all eleven answers on one page. Anything that is
supporting evidence rather than an answer lives in the appendix, reachable by number when a question
demands it.

| | Slides |
|---|---|
| Frame — overview, method, the one thing | 1–4 |
| **Part A** — A1 segments, A1 sizing, A2 gap, A2 risk | 5–9 |
| **Part B** — B1 the field, B2 how they serve, B3 what to take | 10–13 |
| **Part C** — C1 ×5, C2 verdict, C2 why, C3 plan, C4 prototype | 14–23 |
| **Part D** — D1 LTV, D2 the A/B test | 24–26 |
| Close — open questions, summary of all eleven answers | 27–28 |
| Appendix — the three further causal tests, method, tables, SQL, sources | 29–41 |

## Rebuilding

```bash
python3 build_deck_html.py           # -> presentation/Jobescape-PM-Deck.html
python3 build_deck_html.py --pdf     # + the PDF (needs google-chrome)

cd presentation
python3 check_overflow.py            # measures every slide for content escaping its frame
python3 check_accent.py              # enforces exactly one accent region per content slide
python3 prep_assets.py               # re-crop the product screenshots (refuses any crop with PII)
```

`check_overflow.py` renders the deck in headless Chrome and walks every element in every slide — it
catches the layout bugs that are impossible to spot by eye across 41 slides. Both checks currently
pass clean.

## Design

Editorial print — a magazine feature spread rather than a pitch deck. Confident, typographic,
deliberately dense in places and deliberately empty in others.

| Token | Value | Use |
|---|---|---|
| Background | `#14120F` | warm near-black, every slide |
| Primary text | `#F5F1E8` | warm off-white |
| Muted text | `#8C8578` | labels, captions, source lines, footers |
| Accent | `#C85A2E` | burnt orange — **exactly one element per slide** |
| Rules | `#2E2A24` | hairlines and the bottom rule |

**Type:** Inter Tight 600 for headlines (tight tracking, sentence case, max two lines); Inter 400 for
body at a 65-character measure; IBM Plex Mono for every number, label, axis and caption, uppercase with
0.08em tracking. All three are **embedded as latin-subset woff2 data URIs**, so the file renders
identically on any machine with no network and no font substitution.

**Layout:** a 12-column grid with an 8% outer margin. The default slide puts the headline in columns
1–5 and the evidence in 6–13 — asymmetric by rule, never split down the middle. Eleven distinct
layouts across the deck (title, index, split, hero, table, chart, evidence, statement, progression,
code, divider), and no two consecutive slides share one. Section dividers are full-bleed accent.

**Charts** are inline SVG: no gridlines, no legends, no shadows. Every point is labelled directly and
every series is desaturated except the one that matters. Where a chart uses a non-zero baseline, the
axis floor is printed in the chart title.

## Files

| Path | What |
|---|---|
| `../build_deck_html.py` | The generator — all content and slide composition |
| `deck_assets.py` | Embeds the fonts and right-sizes the screenshots |
| `prep_assets.py` | Crops the product captures; refuses any crop containing my name/email |
| `check_overflow.py`, `check_accent.py` | The two automated design audits |
| `assets/`, `fonts/` | Embedded source material |
| `OUTLINE.md` | The storyboard |
| `_superseded/` | The earlier SVG-per-slide pipeline, kept for reference |

*The earlier build produced one editable SVG per slide for Lunacy. It was replaced by this
single-file HTML deck on the brief's revised visual direction; the old pipeline is in `_superseded/`
if per-layer editing is ever wanted again.*
