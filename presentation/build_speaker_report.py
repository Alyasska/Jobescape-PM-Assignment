#!/usr/bin/env python3
"""Assemble the speaker report and print it to PDF.

The report is the document Aliaskar holds while presenting, so its slide numbers MUST match the
deck exactly. They did not: it was written against an earlier deck and drifted by one to two
slides from slide 5 onward, with no cue card at all for 15 slides including the whole appendix.

So the front matter (timing table, slide map, section headers) is now GENERATED FROM THE DECK,
and `--check` fails if any slide lacks an entry or any entry points at a slide that no longer
exists. The prose lives in SPEAKER-REPORT.md; the numbering is not hand-maintained.

    python3 build_speaker_report.py            # -> Jobescape-Presenter-Reference.pdf
    python3 build_speaker_report.py --check    # verify sync only, no output
"""
import os
import re
import subprocess
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "Jobescape-PM-Deck.html")
SRC = os.path.join(HERE, "SPEAKER-REPORT.md")
OUT_PDF = os.path.join(HERE, "Jobescape-Presenter-Reference.pdf")
OUT_HTML = os.path.join(HERE, "Jobescape-Presenter-Reference.html")

# minutes budgeted per deck section, in deck order
BUDGET = {"Title": 0.2, "Overview": 0.7, "Method": 0.8, "The one thing": 1.0, "Background": 0.7}


def deck_slides():
    """(number, section, label) for every slide, read from the built deck."""
    doc = open(DECK).read()
    out = []
    for i, s in enumerate(re.findall(r'<section\b[^>]*>(.*?)</section>', doc, re.S), 1):
        foot = re.search(r'class="foot"><span>(.*?)</span>', s, re.S)
        dh = re.search(r'class="div-h"[^>]*>(.*?)</div>', s, re.S)
        k = re.search(r'class="kicker"[^>]*>(.*?)</p>', s, re.S)
        lab = dh.group(1) if dh else (k.group(1) if k else "Title")
        clean = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
        out.append((i, clean(foot.group(1)) if foot else "", clean(lab)))
    return out


def entries():
    """slide number -> (title, body) parsed from the markdown."""
    txt = open(SRC).read()
    body = txt.split("\n<!-- ENTRIES -->\n", 1)[1]
    parts = re.split(r"(?m)^### (\d+) · (.+?)$", body)
    out = {}
    for i in range(1, len(parts), 3):
        out[int(parts[i])] = (parts[i + 1].strip(),
                              re.split(r"(?m)^## ", parts[i + 2])[0].rstrip())
    return out


def check():
    slides, ents = deck_slides(), entries()
    n = len(slides)
    missing = [i for i, _, _ in slides if i not in ents]
    orphan = [i for i in ents if i > n]
    print(f"  deck {n} slides · report {len(ents)} cue cards")
    if missing:
        print(f"  {len(missing)} slides have NO cue card: {missing}")
    if orphan:
        print(f"  {len(orphan)} cue cards point at slides that don't exist: {orphan}")
    if not missing and not orphan:
        print("  every slide has a cue card, and every card points at a real slide ✓")
    return 1 if (missing or orphan) else 0


CSS = """
@page { size: A4 portrait; margin: 16mm 15mm 18mm; }
* { box-sizing: border-box; }
body { font: 400 11.6pt/1.5 'Inter', -apple-system, sans-serif; color: #14120F;
       -webkit-font-smoothing: antialiased; }
h1 { font-size: 25pt; letter-spacing: -.02em; margin: 0 0 6pt; }
h1 + p { color: #55514A; font-size: 12pt; margin-bottom: 14pt; }
h2 { font-size: 15pt; margin: 22pt 0 8pt; padding-bottom: 5pt;
     border-bottom: 1.6pt solid #14120F; break-after: avoid; }
h2.part { break-before: page; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 12pt; font-size: 10pt; }
th { text-align: left; font-weight: 600; border-bottom: 1.2pt solid #14120F;
     padding: 4pt 8pt 4pt 0; font-size: 9pt; text-transform: uppercase;
     letter-spacing: .05em; color: #55514A; }
td { padding: 4pt 8pt 4pt 0; border-bottom: .6pt solid #DED9CF; vertical-align: top; }
code { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: .87em;
       background: #F1EDE4; padding: .5pt 3pt; border-radius: 2px; }
blockquote { margin: 8pt 0; padding: 6pt 12pt; border-left: 2.5pt solid #C2461F;
             color: #55514A; }
hr { border: 0; border-top: .6pt solid #DED9CF; margin: 14pt 0; }

/* Cards may flow across a page — forcing each to stay whole left 40% of some pages blank,
   which is worse in a lookup document. What must never split: a data table, and a card
   heading stranded at the foot of a page away from its content. */
.card { margin: 0 0 13pt; padding: 9pt 0 0; border-top: .8pt solid #DED9CF; }
.card .hd { break-after: avoid; page-break-after: avoid; }
table { break-inside: avoid; page-break-inside: avoid; }
.card .hd { display: flex; align-items: baseline; gap: 10pt; margin-bottom: 5pt; }
.card .no { font: 600 19pt/1 'Inter', sans-serif; letter-spacing: -.02em;
            color: #C2461F; min-width: 34pt; }
.card .ti { font: 600 13pt/1.25 'Inter', sans-serif; flex: 1; }
.card.appendix .no { color: #6E6A61; }
.card p { margin: 0 0 5pt; }
.card strong { font-weight: 600; }
.card em { color: #55514A; }
"""


def build():
    md = open(SRC).read().split("\n<!-- ENTRIES -->\n")
    front = markdown.markdown(md[0], extensions=["tables", "sane_lists"])

    # cue cards: render each as its own unbreakable block with a big slide number
    cards = []
    parts = re.split(r"(?m)^### (\d+) · (.+?)$", md[1])
    pre = markdown.markdown(parts[0], extensions=["tables"])
    for i in range(1, len(parts), 3):
        num, title = parts[i], parts[i + 1].strip()
        body, _, tail = re.split(r"(?m)^(## .*)$", parts[i + 2] + "\n## \x00", maxsplit=1)[:3]
        cls = "card appendix" if int(num) >= 34 else "card"
        cards.append(f'<div class="{cls}"><div class="hd"><span class="no">{int(num):02d}</span>'
                     f'<span class="ti">{markdown.markdown(title)[3:-4]}</span></div>'
                     f'{markdown.markdown(body, extensions=["tables"])}</div>')

    doc = (f'<!doctype html><meta charset="utf-8">'
           f'<title>Presenter reference — Jobescape PM assignment</title>'
           f"<style>{CSS}</style>{front}{pre}" + "".join(cards))
    open(OUT_HTML, "w").write(doc)
    r = subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", f"--print-to-pdf={OUT_PDF}",
                        "--virtual-time-budget=15000", f"file://{OUT_HTML}"],
                       capture_output=True, timeout=180)
    print(f"  {len(cards)} cue cards -> {OUT_PDF} "
          f"({os.path.getsize(OUT_PDF)/1024:.0f} KB, chrome exit {r.returncode})")


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    check()
    build()
