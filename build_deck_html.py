#!/usr/bin/env python3
"""Build the Jobescape PM deck as ONE self-contained HTML file.

Structure — the assignment's eleven tasks, in the brief's order.
Voice     — fragments, points, diagrams, plots. Not prose: the speaker talks, the slide shows.
Evidence  — every claim carries a numbered marker, resolved on the References slide.
Treatment — editorial print, warm-white ground, exactly one accent element per slide.

    python3 build_deck_html.py          # -> presentation/Jobescape-PM-Deck.html
    python3 build_deck_html.py --pdf    # + print-ready PDF via headless Chrome
"""
import html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "presentation"))
from deck_assets import font_face_css, img                          # noqa: E402
from deck_diagrams import (block_diagram, dfd, erd, pbd, shrink_report,   # noqa: E402
                            state_flow)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(HERE, "presentation", "Jobescape-PM-Deck.html")
OUT_PDF = os.path.join(HERE, "presentation", "Jobescape-PM-Deck.pdf")

SLIDES = []
MAIN_COUNT = 34
REFS = []
CITES = {}          # ref number -> slide numbers citing it, so a reference can point back
CUR_SLIDE = 0       # set by build() while a slide renders


def e(s):
    return html.escape(str(s), quote=False)


def slide(section, layout):
    def deco(fn):
        SLIDES.append({"section": section, "layout": layout, "fn": fn})
        return fn
    return deco


def ref(short, where):
    """Register a source; return the clickable marker to sit beside the claim.

    The marker jumps to the entry on the References slide, and that entry carries a link back
    to every slide citing it — so a question in Q&A is two clicks, there and back, in the PDF
    as well as the browser (Chrome turns internal anchors into real PDF links)."""
    num = next((n for n, s, w in REFS if (s, w) == (short, where)), None)
    if num is None:
        REFS.append((len(REFS) + 1, short, where))
        num = len(REFS)
    CITES.setdefault(num, [])
    if CUR_SLIDE and CUR_SLIDE not in CITES[num]:
        CITES[num].append(CUR_SLIDE)
    return f'<sup class="ref"><a href="#sref-{num}">{num}</a></sup>'


# ───────────────────────────────────────────── fragments
def col(inner, span, align=None):
    st = f"grid-column:{span}" + (f";align-self:{align}" if align else "")
    return f'<div class="col" style="{st}">{inner}</div>'


def kicker(t):
    return f'<p class="kicker">{e(t)}</p>'


def h(t, _c=None):
    return f'<h2 class="h">{t}</h2>'


def lede(t):
    return f'<p class="lede">{t}</p>'


def points(items, num=False):
    o = ['<dl class="pts">']
    for i, it in enumerate(items, 1):
        if isinstance(it, (list, tuple)):
            a, b = it
            n = f'<span class="pn">{i:02d}</span>' if num else ""
            o.append(f'<div class="pt">{n}<dt>{a}</dt><dd>{b}</dd></div>')
        else:
            o.append(f'<div class="pt"><dt class="solo">{it}</dt></div>')
    return "".join(o) + "</dl>"


def table(headers, data, _c=None, accent_row=None, accent_cell=None, tight=False):
    NUMISH = re.compile(r"^[−+\-]?[\d.,$%\s/–—:]+$")

    def numeric(idx):
        cells = [r[idx] for r in data if str(r[idx]).strip()]
        return bool(cells) and all(NUMISH.match(str(c).strip()) for c in cells)

    nums = {i for i in range(1, len(headers)) if numeric(i)}
    cls = "tbl tight" if tight else "tbl"
    o = [f'<table class="{cls}"><thead><tr>']
    for i, hd in enumerate(headers):
        o.append(f'<th class="{"num" if i in nums else ""}">{e(hd)}</th>')
    o.append("</tr></thead><tbody>")
    for r, row in enumerate(data):
        hi = ' class="hi"' if accent_row == r else ""
        o.append(f"<tr{hi}>")
        for i, cell in enumerate(row):
            c = ["num"] if i in nums else []
            if accent_cell == (r, i):
                c.append("acc")
            o.append(f'<td class="{" ".join(c)}">{cell}</td>')
        o.append("</tr>")
    return "".join(o) + "</tbody></table>"


def hero(number, caption, _c=None, accent=True):
    return (f'<div class="hero"><div class="figure{" acc" if accent else ""}">{number}</div>'
            f'<p class="figcap">{caption}</p></div>')


def picture(name, max_w, _c=None, cap=None, height=None, disp=None):
    # Forcing a height crops the overflowing axis. That is safe for a portrait screenshot in a
    # landscape box (it trims the bottom) and destructive for a wide one (it trims the sides,
    # through the content). check_images.py enforces the distinction.
    hs = f";height:{height}px;object-fit:cover;object-position:top" if height else ""
    fs = f' style="max-width:{disp}px"' if disp else ""
    o = f'<figure{fs}><img src="{img(name, max_w)}" alt="" style="width:100%{hs}">'
    if cap:
        o += f"<figcaption>{e(cap)}</figcaption>"
    return o + "</figure>"


# ───────────────────────────────────────────── plots
C_MUTED, C_MUTED2, C_ACCENT = "#D8D2C6", "#A79F91", "#C2461F"
C_TEXT, C_LABEL = "#14120F", "#6E6A61"


def _txt(x, y, s, size=22, fill=C_LABEL, anchor="start", weight=400, mono=True, ls=".05em"):
    fam = "IBM Plex Mono, monospace" if mono else "Inter, sans-serif"
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}">{e(s)}</text>')


def bars_h(items, w=980, bar=52, gap=26, label_w=360, vmax=None, fmt=None):
    fmt = fmt or (lambda v: f"{v:.1%}")
    vmax = vmax or max(i[1] for i in items)
    bw = w - label_w - 320
    hgt = len(items) * (bar + gap)
    o = [f'<svg viewBox="0 0 {w} {hgt}" width="100%">']
    for i, (lab, v, acc, note) in enumerate(items):
        y = i * (bar + gap)
        o.append(_txt(label_w - 26, y + bar * .68, lab, 25, C_TEXT if acc else "#4A463F",
                      "end", 500, False, "0"))
        o.append(f'<rect x="{label_w}" y="{y}" width="{max(v/vmax*bw,3):.1f}" height="{bar}" '
                 f'fill="{C_ACCENT if acc else C_MUTED}"/>')
        o.append(_txt(label_w + v / vmax * bw + 20, y + bar * .68, fmt(v), 27,
                      C_ACCENT if acc else C_TEXT, "start", 500))
        if note:
            o.append(_txt(w - 4, y + bar * .68, note, 22, C_LABEL, "end"))
    return "".join(o) + "</svg>"


def bars_v(items, w=980, hgt=340, gap=18, accent_idx=0):
    PAD, TOP = 70, 40
    n = len(items)
    bw = (w - 2 * PAD - gap * (n - 1)) / n
    vmax = max(v for _, v in items)
    o = [f'<svg viewBox="0 {-TOP} {w} {hgt + TOP + 62}" width="100%">']
    for i, (lab, v) in enumerate(items):
        bh = v / vmax * hgt
        x = PAD + i * (bw + gap)
        o.append(f'<rect x="{x:.1f}" y="{hgt - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
                 f'fill="{C_ACCENT if i == accent_idx else C_MUTED}"/>')
        o.append(_txt(x + bw / 2, hgt - bh - 18, str(v), 27,
                      C_ACCENT if i == accent_idx else C_TEXT, "middle", 500))
        o.append(_txt(x + bw / 2, hgt + 44, lab, 21, C_LABEL, "middle"))
    return "".join(o) + "</svg>"


def butterfly(items, w=980, bar=48, gap=22, accent=None):
    LABEL_W = 150
    vmax = max(max(l, r) for _, l, r in items)
    half = (w - LABEL_W) * .40
    mid = LABEL_W + half + 40
    hgt = len(items) * (bar + gap)
    o = [f'<svg viewBox="0 0 {w} {hgt + 40}" width="100%">']
    o.append(_txt(mid - 18, 18, "MEN", 20, C_LABEL, "end"))
    o.append(_txt(mid + 18, 18, "WOMEN", 20, C_LABEL))
    for i, (lab, l, r) in enumerate(items):
        y = 40 + i * (bar + gap)
        al = accent == (i, "l")
        o.append(_txt(LABEL_W - 24, y + bar * .7, lab, 27, C_TEXT, "end", 500, False, "0"))
        lx = mid - l / vmax * half
        o.append(f'<rect x="{lx:.1f}" y="{y}" width="{l/vmax*half:.1f}" height="{bar}" '
                 f'fill="{C_ACCENT if al else C_MUTED}"/>')
        o.append(f'<rect x="{mid+6}" y="{y}" width="{r/vmax*half:.1f}" height="{bar}" fill="{C_MUTED}"/>')
        o.append(_txt(lx + 16, y + bar * .7, f"{l:,}", 24, "#FFFCF6" if al else C_TEXT, "start", 500))
        o.append(_txt(mid + 6 + r / vmax * half + 16, y + bar * .7, f"{r:,}", 24, C_LABEL, "start", 500))
    return "".join(o) + "</svg>"


def linechart(vals, labels, w=980, hgt=320, ymin=None, ymax=1.0, accent_last=False, fmt=None):
    fmt = fmt or (lambda v: f"{v:.0%}")
    ymin = 0 if ymin is None else ymin
    PAD, TOP = 140, 56
    n = len(vals)
    step = (w - 2 * PAD) / (n - 1) if n > 1 else 0
    span = (ymax - ymin) or 1
    pts = [(PAD + i * step, hgt - (v - ymin) / span * hgt) for i, v in enumerate(vals)]
    o = [f'<svg viewBox="0 {-TOP} {w} {hgt + TOP + 66}" width="100%">']
    d = " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    o.append(f'<path d="M{d}" fill="none" stroke="{C_MUTED2}" stroke-width="3.5"/>')
    for i, ((x, y), v) in enumerate(zip(pts, vals)):
        acc = accent_last and i == n - 1
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{10 if acc else 7}" '
                 f'fill="{C_ACCENT if acc else C_MUTED2}"/>')
        o.append(_txt(x, y - 26, fmt(v), 26, C_ACCENT if acc else C_TEXT, "middle", 500))
        o.append(_txt(x, hgt + 52, labels[i], 22, C_LABEL, "middle"))
    return "".join(o) + "</svg>"


# ════════════════════════════════════════════ 1—5 · FRAME
@slide("Title", "title")
def _(i, n):
    return '''<div class="title-wrap">
      <p class="kicker">Product Manager Test Assignment · Nomad Venture Studio</p>
      <h1>Jobescape<span class="acc">.</span><br>The assignment, task by task.</h1>
      <p class="sub">4 parts · 11 tasks · 9,956 paying subscribers</p>
      <p class="byline">Aliaskar Bekishev &nbsp;·&nbsp; July 2026</p>
    </div>'''


@slide("Overview", "index")
def _(i, n):
    items = [("A1", "Audience segments — what I split by", "07–08"),
             ("A2", "Product vs need — the gap, the risk", "09–10"),
             ("B1", "Competitors — direct vs indirect", "12"),
             ("B2", "How each serves its audience", "13"),
             ("B3", "What to take, and the order", "14"),
             ("C1", "Release analytics — high / low / didn't take", "16–21"),
             ("C2", "Verdict — and why", "22–24"),
             ("C3", "What's next", "25"),
             ("C4", "Prototype", "26"),
             ("D1", "Net LTV per plan, blended", "28"),
             ("D2", "A/B model, break-even, recommendation", "29–30")]
    ix = '<div class="index tight">'
    for c, txt, sl in items:
        ix += (f'<div class="ix"><span class="ixc">{c}</span>'
               f'<span class="ixt">{e(txt)}</span><span class="ixn">{sl}</span></div>')
    ix += "</div>"
    return (kicker("What this covers")
            + col(h('<span class="acc">Eleven</span> tasks.'), "1/5")
            + col(lede("Brief's own order · summary p.31 · references p.33 · appendix p.34–46"), "6/13")
            + col(ix, "1/13"))


@slide("Method", "diagram")
def _(i, n):
    return (kicker("How every number was produced")
            + col(h("Computed, not quoted.")
                  + points([("5 SQL queries", "one row per user"),
                            ("6 Python scripts", "pure standard library"),
                            ("91 assertions", "re-derived from the raw CSV"
                             + ref("Reproducibility harness", "part-c-release-verdict/analysis/05_qa.py"))]),
                  "1/4")
            + col(dfd(), "5/13"))


@slide("The one thing", "hero")
def _(i, n):
    return (kicker("If you remember one thing")
            + col(hero("50.2%", "OF PAYING SUBSCRIBERS NEVER COMPLETE A SINGLE LESSON — ANYWHERE"
                       + ref("50.2% never complete a lesson",
                             "analysis/04_loose_ends.py · 4,999 of 9,956")), "1/7")
            + col(points([("Selling", "excellent"),
                          ("Activation", "never built"),
                          ("Economics", "depend on the tail activation would protect")]), "8/13"))


@slide("Background", "diagram")
def _(i, n):
    return (kicker("The business, and where it breaks")
            + col(h("Money first. Value later.")
                  + points([("Paywall-first", "every user in the data is a payer"
                             + ref("Every app_events user has a purchase row",
                                   "sql/13_comparison_groups.sql")),
                            ("Consequence", "failed activation = refunds, not lost signups")]), "1/4")
            + col(block_diagram(), "5/13"))


# ════════════════════════════════════════════ PART A
@slide("Part A", "divider")
def _(i, n):
    return ('<div class="div-wrap"><p class="div-k">Part A</p>'
            '<h1 class="div-h">Audience &amp; product</h1></div>')


@slide("A1 · Segments", "table")
def _(i, n):
    return (kicker("Part A · Task 1 — audience segments")
            + col(h('Clustered, <span class="acc">not asserted.</span>')
                  + table(["Segment", "Who they are", "Share", "Strongest signal"], [
                      ["The Striver", "senses a gap, closing it deliberately", "28.4%", "“could be behind” 1.9×"],
                      ["The Latecomer", "oldest, hasn’t started, watching others pull ahead", "22.0%", "“falling behind” 2.2×"],
                      ["The Adept", "already gets real value from AI, wants more", "20.9%", "“AI already helps me” 2.5×"],
                      ["The Optimiser", "mid-career, uses Claude on work, wants speed", "12.3%", "aged 35–44 2.6×"],
                      ["The Founder", "learning AI to build something of their own", "9.0%", "“start my own business” 3.1×"],
                      ["The Switcher", "between jobs, starting from zero", "7.4%", "“exploring options” 4.4×"],
                  ]), "1/13")
            + col(lede("k-modes on 38,071 quiz respondents × 10 answers. Signal = lift vs population."
                       " <b>No elbow</b> — this is a continuum, so six is a resolution I chose, not a "
                       "count the data forced."
                       + ref("k-modes clustering, 38,071 respondents",
                             "part-a-audience/analysis/cluster_quiz.py")), "1/13"))


@slide("A1 · Who pays", "chart")
def _(i, n):
    return (kicker("Part A · Task 1 — who actually pays")
            + col(h("A decade older than the internal read.")
                  + points([("Gender read", "right — 59.7% men"),
                            ("Age read", "~60% are 45+"),
                            ("Biggest cell", "men 55+"),
                            ("Churn", "31.1% at 18–24 → 9.5% at 45–54")]), "1/5")
            + col(f'<p class="charttitle">PAYING SUBSCRIBERS BY AGE AND GENDER · n = 9,956'
                  f'{ref("Buyer demographics, n = 9,956", "subscribe_events · analysis/02_main.py §6")}</p>'
                  + butterfly([("55+", 2120, 1035), ("45–54", 1444, 1065), ("35–44", 1040, 815),
                               ("25–34", 613, 493), ("18–24", 602, 310)], accent=(0, "l")), "6/13"))


@slide("A2 · The gap", "evidence")
def _(i, n):
    return (kicker("Part A · Task 2 — expectation vs reality")
            + col(h("Paid. Walked it. Checked."), "1/5")
            + col(points([("Sold", "“personal AI mentors · 24/7 support chat”"),
                          ("Got", "one bot, stock photo, named Mark"),
                          ("Got", 'chat metered to <span class="acc">5 credits</span>')])
                  + lede("My own read corrected: cancellation is <b>self-serve</b> — 1,358 uses. "
                         "The trap is the refund."
                         + ref("Self-serve cancel used 1,358 times",
                               "app_events · subscription_manage_subscription_unsubscribe_click")),
                  "6/13")
            + col(picture("paywall.png", 620, cap="PROMISED AT THE PAYWALL", height=320), "1/4")
            + col(picture("mark-chat.png", 460, cap="THE “MENTOR”", height=320), "5/8")
            + col(picture("chat-credits.png", 950, cap="THE “24/7 CHAT”, METERED"),
                  "9/13", align="end"))


@slide("A2 · The risk", "hero")
def _(i, n):
    return (kicker("Part A · Task 2 — where the main gap is")
            + col(hero("11.3%", "OF UNSUBSCRIBES ARE PAYMENT FAILURES, CHARGEBACKS OR DISPUTES"
                       + ref("11.3% of unsubs are payment / chargeback / dispute",
                             "app_events.unsubscribe_reason · analysis/03_supplement.py §E")), "1/7")
            + col(points([("Scale", "157 of 1,393 · in 14 days"),
                          ("Mechanism", "refund gated on finishing in ~31 days"),
                          ("Exposure", "the model FTC sued Genesis over, June 2026"
                           + ref("FTC v. Genesis, June 2026",
                                 "research/deep-05-product-reality.md"))]), "8/13"))


# ════════════════════════════════════════════ PART B
@slide("Part B", "divider")
def _(i, n):
    return '<div class="div-wrap"><p class="div-k">Part B</p><h1 class="div-h">Competitors</h1></div>'


@slide("B1 · The field", "split")
def _(i, n):
    tc = '<div class="twocol"><div><p class="colhead">Direct</p>'
    for a, b in [("Coursiv", "~95% overlap · identical funnel"),
                 ("Iro AI", "“Duolingo for AI” · weak commercially"),
                 ("Outskill", "same buyer · premium price"),
                 ("Be10x", "tripwire CRO · US launch pending")]:
        tc += f'<div class="row"><dt>{e(a)}</dt><dd>{e(b)}</dd></div>'
    tc += '</div><div><p class="colhead">Indirect</p>'
    for a, b in [("Section AI", "pivoted courses → AI co-pilot"),
                 ("The Rundown", "2M newsletter → $1,008/yr"),
                 ("Mimo / Headway", "the paywall playbook"),
                 ("ChatGPT, YouTube", "give it away free")]:
        tc += f'<div class="row"><dt>{e(a)}</dt><dd>{e(b)}</dd></div>'
    tc += "</div></div>"
    return (kicker("Part B · Task 1 — find competitors")
            + col(h("4 direct twins. The dangerous one is indirect.")
                  + points([("Same job", "use AI at work without feeling behind"),
                            ("Decisive", '<span class="acc">the content itself is free</span>'),
                            ("So", "win on scaffolding, feedback, accountability"
                             + ref("Competitor set and classification",
                                   "part-b-competitors/01-competitors.md"))]), "1/5")
            + col(tc, "6/13"))


@slide("B2 · How they serve", "table")
def _(i, n):
    return (kicker("Part B · Task 2 — how they serve that audience")
            + col(h("Nobody wins on content.")
                  + table(["Competitor", "Overlap", "Mechanic", "Well / badly"], [
                      ["Coursiv", "~95%", "Finite branded challenge · honest pricing", "Container works · content thin"],
                      ["Iro AI", "High", "Graded Prompt Lab", "Real practice · no distribution"],
                      ["Section AI", "High", "Role-specific co-pilot, saveable", "Admits courses don't retain"],
                      ["Mimo", "Adjacent", "Trial-timeline paywall + reminder", "Best paywall · off-subject"],
                      ["The Rundown", "Broad", "Newsletter → paid university", "Owned audience · not skills"],
                  ], accent_cell=(2, 3)), "1/13")
            + col(lede("From public product, pricing pages and trials."
                       + ref("Competitor teardowns",
                             "part-b-competitors/02-analysis.md · research/deep-01, deep-02")), "1/13"))


@slide("B3 · What to take", "index")
def _(i, n):
    ix = '<div class="index">'
    for c, ttl, why in [("01", "Mimo's trial-timeline paywall", "+100% trial opt-in · −25% early cancels · near-zero build"),
                        ("02", "Coursiv's finite branded challenge", "retention container · defuses regulatory risk"),
                        ("03", "A graded practice surface", "the only moat against free"),
                        ("04", "Owned newsletter + expensable pricing", "CAC hedge · compounds slowly"),
                        ("05", "Offer-ladder tests", "after retention, not before")]:
        ix += (f'<div class="ix"><span class="ixc{" acc" if c == "01" else ""}">{c}</span>'
               f'<span class="ixt"><b>{e(ttl)}</b> — {e(why)}</span></div>')
    ix += "</div>"
    return (kicker("Part B · Task 3 — what to take, prioritized")
            + col(h("Order follows the money."), "1/5")
            + col(table(["#", "Steal", "From", "Why here"], [
                      ["1", "Daily-cost paywall with anchored discount", "Mimo", "highest ROI, lowest cost"],
                      ["2", "Branded finite challenge as the container", "Coursiv", "retention, and you half-built it"],
                      ["3", "A practice surface — prompt lab, saveable output", "Iro · Section", "the only durable moat"],
                      ["4", "Owned newsletter / in-app daily brief", "The Rundown", "compounds, so start it early"],
                      ["5", "Free-workshop → high-ticket ladder", "Outskill", "last — needs retention first"],
                  ], accent_cell=(0, 0))
                  + lede("De-risk → retain → differentiate → diversify → expand."
                         + ref("Prioritized recommendations",
                               "part-b-competitors/03-recommendations.md")), "6/13"))


@slide("B3 · The two that pay first", "split")
def _(i, n):
    return (kicker("Part B · Task 3 — the top two, concretely")
            + col(h("Both are container work. Neither is content.")
                  + lede("You do not need better lessons. You need better vessels for the ones "
                         "you have — and vessels are the cheap half."), "1/5")
            + col(points([("Steal 1 · the paywall",
                           "day-price framing (“$0.71/day”), the original struck through, one "
                           "pre-selected plan. Mimo ships it; your paywall sells a 61% discount "
                           '<span class="acc">with no daily anchor</span>' ),
                          ("Steal 2 · the container",
                           "a branded, finite, gated challenge — the thing Part C proves you "
                           "half-built. Coursiv brands theirs and gates the days"),
                          ("Why these two first",
                           "both defend revenue already booked. Everything else on the list "
                           "chases revenue you do not have yet"
                           + ref("Competitor teardowns",
                                 "part-b-competitors/02-analysis.md · research/deep-01, deep-02"))]),
                  "6/13"))


# ════════════════════════════════════════════ PART C
@slide("Part C", "divider")
def _(i, n):
    return ('<div class="div-wrap"><p class="div-k">Part C</p>'
            '<h1 class="div-h">The Challenge release</h1></div>')


@slide("C1 · What shipped", "diagram")
def _(i, n):
    return (kicker("Part C · Task 1 — what actually shipped")
            + col(h("The gate is a suggestion.")
                  + lede("One day = one skill → daily return. The gate warns, then yields."
                         + ref("Feature = course_id 338 · 99.7% of all challenge starts",
                               "app_events · analysis/01_diagnostics.py Q5")), "1/13")
            + col(pbd(), "1/13"))


@slide("C1 · Definitions", "split")
def _(i, n):
    return (kicker("Part C · Task 1 — engagement tiers")
            + col(h("High / low, defined up front.")
                  + points([("Measure", "challenge lessons completed"),
                            ("Not days", "coming back <i>is</i> retention — circular"),
                            ("Cut at 3", 'where the D7 curve steps — <span class="acc">18% → 39%</span>'),
                            ("Robust", "swept every threshold 1–8"
                             + ref("Tier definition + threshold sweep",
                                   "analysis/02_main.py §2, §4"))]), "1/5")
            + col(table(["Tier", "Rule", "Users", "Share"], [
                ["High", "≥ 3 of 8 lessons", "158", "1.6%"],
                ["Low", "≤ 2 lessons", "953", "9.6%"],
                ["Didn't take it", "never started", "8,845", "88.8%"],
            ]), "6/13"))


@slide("C1 · The journey", "diagram")
def _(i, n):
    return (kicker("Part C · Task 1 — how users go through it")
            + col(h("89% never start it.")
                  + lede("But 94.6% of those who see the popup click it — distribution, not desire."
                         + ref("Exposure ladder, 9,956 payers",
                               "analysis/02_main.py §1 · sql/13_comparison_groups.sql")), "1/13")
            + col(state_flow(), "1/13"))


@slide("C1 · The comparison", "table")
def _(i, n):
    return (kicker("Part C · Task 1 — the comparison the brief asks for")
            + col(h("Reads like the Challenge triples D1.")
                  + table(["Metric", "High · 158", "Low · 953", "Didn't take · 8,845"], [
                      ["D1 — the target", "69.6%", "58.4%", "21.7%"],
                      ["D3", "57.0%", "34.4%", "10.0%"],
                      ["D7", "39.1%", "18.0%", "6.9%"],
                      ["Unsubscribe", "11.4%", "11.4%", "14.3%"],
                      ["Lessons, all courses", "19.28", "6.38", "1.81"],
                      ["CSAT", "3.33", "3.53", "3.74"],
                  ], accent_row=0)
                  + lede('<span class="acc">It does not.</span> Same clock — first app day. '
                         'Intervals in the appendix.'
                         + ref("Tier comparison, Wilson intervals", "analysis/02_main.py §3")), "1/13"))


@slide("C1 · Is it causal", "chart")
def _(i, n):
    left = (h("Same screen. Same result.")
            + points([("The 8,845", "mostly never saw the feature — not a control"),
                      ("The fair test", "takers vs people who saw it and declined"),
                      ("Read the bars", "top three are level · the cliff is the bottom one")])
            + '<div class="inline-hero"><div class="figure sm acc">+0.5</div>'
              '<p class="figcap">PERCENTAGE POINTS · p = 0.82'
              + ref("Exposure-matched control · z = +0.22", "analysis/02_main.py §4 Test A")
              + '</p></div>')
    return (kicker("Part C · Task 1 — is that gap causal?")
            + col(left, "1/6")
            + col('<p class="charttitle">D1 RETENTION · COMMON CLOCK</p>'
                  + bars_h([("Started the Challenge", .600, False, "n = 1,111"),
                            ("Joined, never started", .604, False, "n = 230"),
                            ("Viewed, never joined", .593, False, "n = 764"),
                            ("Never reached a surface", .122, False, "n = 6,716")],
                           bar=72, gap=38, label_w=370, vmax=.70), "7/13"))


@slide("C1 · Segments", "table")
def _(i, n):
    return (kicker("Part C · Task 1 — how segments behave")
            + col(h("No segment rescues it."), "1/5")
            + col(points([("Take-up range", '<span class="acc">8.8% – 14.9%</span> across every cut'),
                          ("Taker gap", "roughly constant across ages"
                           + ref("Segment behaviour", "analysis/02_main.py §6"))]), "6/13")
            + col(table(["Age", "Buyers", "Take rate", "D1 takers", "D1 non-takers"], [
                ["55+", "32.1%", "10.2%", "60.9%", "21.4%"],
                ["45–54", "25.6%", "10.9%", "62.1%", "22.6%"],
                ["35–44", "19.0%", "12.0%", "66.1%", "22.5%"],
                ["25–34", "11.2%", "12.4%", "54.0%", "20.1%"],
                ["18–24", "9.2%", "10.3%", "44.7%", "19.3%"],
            ], tight=True), "1/7")
            + col(table(["Work status", "Buyers", "Take rate"], [
                ["Full-time employee", "33.6%", "11.6%"],
                ["Business owner", "18.3%", "8.8%"],
                ["Freelancer", "14.9%", "11.6%"],
                ["Between jobs", "5.8%", "13.1%"],
                ["Student", "1.8%", "14.9%"],
            ], tight=True), "8/13"))


@slide("C2 · The scoreboard", "split")
def _(i, n):
    return (kicker("Part C · Task 2 — the metric that mattered")
            + col(h("You measure something else.")
                  + lede('Brief says D1. Your hierarchy says D1 is <span class="acc">secondary</span>.'
                         + ref("Metric hierarchy · Jobescape PM, 2026-07-28",
                               "00-context/pm-conversation.md")), "1/5")
            + col(points([("Primary", "gross profit · unsub % 12h/24h · rebill 0→1, 1→2 · LTV"),
                          ("Observable here", "unsub timing yes · rebill no, 17 events · profit no"
                           + ref("subscription_renewed = 17 events, n = 9,956",
                                 "app_events event catalogue · sql/14_unsub_timing.sql")),
                          ("Secondary", "D1 / D3 / D7 · session · CSAT — what it was aimed at"),
                          ("So", "scoped second-order, and missed that too")]), "6/13"))


@slide("C2 · Verdict", "statement")
def _(i, n):
    return (kicker("Part C · Task 2 — the verdict")
            + col('<div class="statement"><h1>No.<br>Not a <span class="acc">success</span>.</h1></div>', "1/7")
            + col(points([("D1 — target", "+0.5 pts vs matched control · p = 0.82"),
                          ("Unsubscribe", "−2.3 pts · p = 0.12 · not significant"),
                          ("CSAT", "falls as engagement rises · 3.74 → 3.10"
                           + ref("CSAT by engagement tier", "analysis/03_supplement.py §B")),
                          ("Rule set first", "dose-response surviving exposure matching — failed both")]),
                  "8/13"))


@slide("C2 · Why", "chart")
def _(i, n):
    return (kicker("Part C · Task 2 — why")
            + col(h("A soft gate is not a gate.")
                  + points([("27%", "finished in a single sitting"),
                            ("46%", "within two days"),
                            ("1.46", "mean lessons per active challenge day"),
                            ("Verdict", "not disproven — never tested")]), "1/5")
            + col(f'<p class="charttitle">DAYS TAKEN TO FINISH THE “7-DAY” CHALLENGE · n = 48'
                  f'{ref("Days-to-finish distribution, 48 finishers", "analysis/02_main.py §5")}</p>'
                  + bars_v([("1", 13), ("2", 9), ("3", 6), ("4", 4), ("5", 5), ("6", 2), ("7", 3),
                            ("8", 3), ("9", 2), ("10", 1)], accent_idx=0), "6/13"))


@slide("C3 · The plan", "table")
def _(i, n):
    return (kicker("Part C · Task 3 — what's next")
            + col(h('It isn’t unappealing. It’s <span class="acc">hidden.</span>')
                  + table(["Phase", "Ships", "Metric it moves"], [
                      ["0 · Placement", "Open on the Challenge · 80/20 hold-out", "Biggest loss — and it gives you the control group"],
                      ["1 · First 10 min", "Why 45% get nothing · guaranteed win", "Unsub % 12h/24h — primary"],
                      ["2 · Mechanic", "Make the gate real · wire the reminder", "Rebill 0→1 — primary"],
                      ["3 · Hand-off", "Day ends → send them to the plan", "D3, D7 — today it ends nowhere"],
                      ["4 · Quality", "Mine 3,601 exit-reason events", "CSAT — guardrail 3.45"],
                  ], accent_row=0), "1/13")
            + col(points([("Why placement first", "94.6% of people shown it clicked · 68.5% were never shown it"),
                          ("Kill rule", "hold-out ships · no lift · kill it"
                           + ref("v2 plan, phases and kill rule",
                                 "part-c-release-verdict/03-whats-next.md"))]), "1/13"))


@slide("C4 · Prototype", "evidence")
def _(i, n):
    return (kicker("Part C · Task 4 — the prototype")
            + col(h("The loop, built.")
                  + points([("The hook", "the Challenge greets you · gated, daily"),
                            ("The grind", "the plan · open, no gate"),
                            ("The missing arrow", "day ends → you land on the plan")])
                  + lede('<span class="mono-link acc">alyasska.github.io/'
                         'Nomad_Venture_Studio_TA_C4</span>'), "1/5")
            + col(picture("proto-challenge.png", 1300,
                          cap="THE CHALLENGE, SERVED ON ARRIVAL — DAY 5 IS LOCKED"), "6/13"))


# ════════════════════════════════════════════ PART D
@slide("Part D", "divider")
def _(i, n):
    return ('<div class="div-wrap"><p class="div-k">Part D</p>'
            '<h1 class="div-h">Subscription economics</h1></div>')


@slide("D1 · LTV", "table")
def _(i, n):
    return (kicker("Part D · Task 1 — total net LTV, one-year horizon")
            + col(h("Blended net LTV $125.06.")
                  + table(["Plan", "Mix", "Gross", "Net"], [
                      ["1-week", "10%", "$68.66", "$60.42"],
                      ["4-week", "70%", "$140.57", "$123.70"],
                      ["12-week", "20%", "$184.26", "$162.15"],
                      ["Blended", "100%", "—", "$125.06"],
                  ], accent_row=3, accent_cell=(3, 3)), "1/7")
            + col(points([("Survival", "Sₖ = running product of the C-curve"),
                          ("Gross", "intro + recurring × ΣSₖ + both upsells"),
                          ("Net", "× 0.88 — 12% fee on all collected cash"),
                          ("Validated", "observed mix 10.2 / 64.6 / 25.1 → $126.90"
                           + ref("LTV model + plan-mix validation",
                                 "part-d-economics/model/ltv_model.py · analysis/04_loose_ends.py")),
                          ("Weak point", "1-week plan · 34.6% churn in 14 days")]), "8/13"))


@slide("D2 · The A/B test", "chart")
def _(i, n):
    return (kicker("Part D · Task 2 — the plan-upgrade A/B model")
            + col(h("Break-even 8.3%. Run it.")
                  + points([("Same year, both arms", "12-wk bills 4× in a year, not 12×"),
                            ("Each upgrade", "+$49.99 − $6.55 recurring = $43.44"),
                            ("p*", "3.60 ÷ 43.44 = 8.29%"),
                            ("Cannibalises", "$3.60 second upsell — the whole downside")]), "1/5")
            + col(f'<p class="charttitle">TEST-GROUP NET LTV PER 4-WEEK BUYER · CONTROL $123.70 · '
                  f'AXIS FROM $120{ref("A/B break-even model", "part-d-economics/02-ab-test-model.md")}</p>'
                  + linechart([120.53, 123.70, 126.27, 132.00],
                              ["0%", "8.3%", "15%", "30%"], hgt=280, ymin=119, ymax=134,
                              accent_last=True, fmt=lambda v: f"${v:,.2f}"), "6/13"))


@slide("D2 · Reading it", "progression")
def _(i, n):
    prog = '<div class="prog">'
    for fig, lab, note, acc in [("+$1.31", "PER +1 PT OF REBILL 0→1", "≈1% of blended LTV — inside cohort noise", False),
                                ("$478k", "SAME POINT, PER YEAR", "at 1,000 signups a day", False),
                                ("$1.69m", "+2 PTS ON BOTH REBILLS", "money large · signal faint", True)]:
        prog += (f'<div class="pcol"><div class="pfig{" acc" if acc else ""}">{fig}</div>'
                 f'<p class="plab">{lab}</p><p class="pnote">{e(note)}</p></div>')
    prog += "</div>"
    return (kicker("Part D · what the primary metrics are worth")
            + col(h("LTV prices. It cannot detect."), "1/6")
            + col(lede("Your words: LTV rarely reacts to anything but the obvious. Here is the size — "
                       "so read a v2 on unsub 12h/24h + rebill, then price it with LTV."
                       + ref("LTV sensitivity to rebill",
                             "part-d-economics/model/ltv_sensitivity.py")), "7/13")
            + col(prog, "1/13"))


# ════════════════════════════════════════════ CLOSE
@slide("Summary", "index")
def _(i, n):
    ix = '<div class="index tight">'
    for c, s in [("A1", "6 segments on emotion + JTBD · ~60% of buyers 45+ · churn falls with age"),
                 ("A2", "Acute risk is the refund — 11.3% of unsubs are payment failures or disputes"),
                 ("B1", "4 direct twins · the dangerous indirect competitor is free content"),
                 ("B2", "They win on containers, practice surfaces, paywall craft — not content"),
                 ("B3", "5 steals · de-risk → retain → differentiate → diversify → expand"),
                 ("C1", "89% never start · 45% of starters do zero lessons · gap real, not causal"),
                 ("C2", "Not a success · +0.5 pts, p = 0.82 · never tested its own hypothesis"),
                 ("C3", "Rebuild the mechanic · instrument first · reach last"),
                 ("C4", "Working prototype of the daily gate · pre-registered bar · kill rule"),
                 ("D1", "Net LTV $60 / $124 / $162 · blended $125.06 · validated on real mix"),
                 ("D2", "Break-even 8.3% like-for-like · run it · downside bounded to $3.60")]:
        ix += (f'<div class="ix"><span class="ixc{" acc" if c == "C2" else ""}">{c}</span>'
               f'<span class="ixt">{e(s)}</span></div>')
    ix += "</div>"
    return kicker("All eleven answers") + col(h("Every task, one line."), "1/6") + col(ix, "1/13")


@slide("Open questions", "split")
def _(i, n):
    return (kicker("What I'd need to go further")
            + col(h('<span class="acc">Three</span> the data cannot answer.'), "1/5")
            + col(points([("Was D1 ever the real bar?",
                           "no hold-out exists · if it shipped as a refund gate, my verdict changes"),
                          ("What D1 = success?",
                           "I can say it moved nothing · not whether it missed by a little"),
                          ("Which LTV horizon?",
                           "full curve or 52 weeks · worth ~$5 of blended LTV")], num=True), "6/13"))


@slide("References", "refs")
def _(i, n):
    o = '<div class="reflist">'
    for num, short, where in REFS:
        back = " · ".join(f'<a href="#s{c}">{c:02d}</a>' for c in CITES.get(num, []))
        back = f'<span class="rfb">↩ {back}</span>' if back else ""
        o += (f'<div class="rf" id="sref-{num}"><span class="rfn">{num}</span>'
              f'<span class="rft">{e(short)}</span>'
              f'<span class="rfw">{e(where)}{back}</span></div>')
    o += "</div>"
    return (kicker("References — every marker on every slide")
            + col(h("Sources.")
                  + points([("Re-run", "<b>python3 05_qa.py</b>"),
                            ("Result", '<span class="acc">91 checks</span> · any drift fails')]), "1/4")
            + col(o, "5/13"))


# ════════════════════════════════════════════ APPENDIX
@slide("Appendix", "divider")
def _(i, n):
    return ('<div class="div-wrap"><p class="div-k">Appendix</p>'
            '<h1 class="div-h">The working behind the answers</h1></div>')


@slide("Appendix · The data", "diagram")
def _(i, n):
    return (kicker("Appendix · the data model")
            + col(h("Two tables. One key.")
                  + lede("The product sits entirely behind the paywall."), "1/13")
            + col(erd(), "1/13"))


@slide("Appendix · Test 2", "table")
def _(i, n):
    return (kicker("Appendix · causal test 2 of 4")
            + col(h('Activity held constant → effect stays <span class="acc">zero</span>.')
                  + table(["Product activity", "n takers", "D1 takers", "n control", "D1 control", "Diff", "p"], [
                      ["1 active day", "97", "0.0%", "63", "0.0%", "+0.0", "1.000"],
                      ["2", "270", "46.3%", "257", "42.4%", "+3.9", "0.370"],
                      ["3–4", "446", "64.8%", "427", "65.1%", "−0.3", "0.924"],
                      ["5–7", "217", "82.9%", "205", "84.4%", "−1.4", "0.689"],
                      ["8+", "81", "90.1%", "42", "76.2%", "+13.9", "0.038"],
                  ]), "1/13")
            + col(lede("4 of 5 strata flat · the significant cell is smallest and 1 test in 5."
                       + ref("Stratified comparison", "analysis/04_loose_ends.py")), "1/13"))


@slide("Appendix · Test 3", "progression")
def _(i, n):
    prog = '<div class="prog">'
    for fig, lab, note, acc in [("+38.3", "RAW GAP", "all takers vs never-took", False),
                                ("+17.4", "− SURVIVAL HEAD START", "day-0 starters only", False),
                                ("+0.5", "− EXPOSURE SELECTION", "vs looked-and-left", True)]:
        prog += (f'<div class="pcol"><div class="pfig{" acc" if acc else ""}">{fig}</div>'
                 f'<p class="plab">{lab}</p><p class="pnote">{e(note)}</p></div>')
    prog += "</div>"
    return (kicker("Appendix · causal test 3 of 4 — immortal time")
            + col(h("Takers are pre-selected survivors."), "1/6")
            + col(points([("24%", "start on day 0"), ("Median", "day +1"),
                          ("28%", "day +3 or later"
                           + ref("Immortal-time correction", "analysis/02_main.py §4 Test B"))]), "7/13")
            + col(prog, "1/13"))


@slide("Appendix · Test 4", "chart")
def _(i, n):
    return (kicker("Appendix · causal test 4 of 4")
            + col(h("Bigger day-0 dose → <i>worse</i> return.")
                  + points([("Clean test", "816 takers · all activity on one day"),
                            ("Result", "−9.2 pts · p = 0.048"),
                            ("Bingers", "all 8 in a day → 38.5% unsub")]), "1/5")
            + col(f'<p class="charttitle">D1 NEXT DAY, BY DAY-0 DOSE · AXIS FROM 28%'
                  f'{ref("Non-tautological dose-response", "analysis/02_main.py §4 Test C")}</p>'
                  + linechart([.557, .544, .505, .333], ["0 LESSONS", "1", "2", "3"],
                              hgt=280, ymin=.28, ymax=.60, accent_last=True), "6/13"))


@slide("Appendix · The metric", "split")
def _(i, n):
    return (kicker("Appendix · the governance point")
            + col(h("Your dashboard would call this a win.")
                  + lede('39.8% vs a 26.0% baseline = a <span class="acc">+14-point win</span> — '
                         'an artifact.'
                         + ref("Target metric under both anchors",
                               "analysis/03_supplement.py §A")), "1/5")
            + col(points([("Different clocks", "takers from challenge-start · others from first app day"),
                          ("Different populations", "88.8% of the book · ⅔ never reached a surface"),
                          ("No hold-out", "shipped to 100%"),
                          ("Corrected", "+38 → +17 → +0.5")]), "6/13"))


@slide("Appendix · CSAT", "chart")
def _(i, n):
    return (kicker("Appendix · the red flag")
            + col(h("Satisfaction falls as engagement rises.")
                  + points([("Challenge content", "3.25"),
                            ("Same users, elsewhere", "3.45"),
                            ("So", "scaling reach on 3.25-star content scales refunds")]), "1/5")
            + col(f'<p class="charttitle">MEAN CSAT, 1–5'
                  f'{ref("CSAT inversion", "analysis/03_supplement.py §B · 3,740 / 845 / 158 / 48 raters")}</p>'
                  + bars_v([("NEVER TOOK IT", 3.74), ("LOW · 0–2", 3.53), ("HIGH · 3+", 3.33),
                            ("FINISHED ALL 8", 3.10)], hgt=300, accent_idx=3), "6/13"))


@slide("Appendix · Criteria", "table")
def _(i, n):
    return (kicker("Appendix · Part C Task 3 detail")
            + col(h("Pre-registered success criteria.")
                  + table(["", "Metric", "Bar"], [
                      ["Primary", "Unsub % 12h / 24h, test vs hold-out", '<span class="acc">the business metric</span>'],
                      ["Primary", "Rebill 0→1", "~$1.31 blended LTV per point"],
                      ["Secondary", "Exposure-matched D1 lift", "≥ +5 points"],
                      ["Secondary", "Starters completing ≥1 lesson", "55% → 75%"],
                      ["Guardrail", "Challenge CSAT", "≥ 3.45 · must not fall"],
                      ["Guardrail", "Refund / chargeback rate", "must not rise"],
                      ["Guardrail", "Lessons per starter", "must not fall — gating risk"],
                  ], accent_row=0), "1/13")
            + col(lede("Stated before the test, so the result cannot be reinterpreted after."), "1/13"))


@slide("Appendix · Already built", "evidence")
def _(i, n):
    return (kicker("Appendix · Part C Task 3 detail")
            + col(h("The rebuild is a wiring job.")
                  + points([("Already ships", "WhatsApp agent · motivational messages · study reminders"),
                            ("Already renders", "streak counter · weekly tracker"),
                            ("Shows", '<span class="acc">0</span>'
                             + ref("Automation tab and streak, my paid account",
                                   "part-a-audience/materials/walkthrough/observations.md"))]), "1/4")
            + col(picture("automation.png", 1200)
                  + picture("challenge-streak.png", 616, cap="THE STREAK, IN PRODUCTION",
                            disp=616), "5/13"))


@slide("Appendix · Method", "split")
def _(i, n):
    return (kicker("Appendix · statistical method")
            + col(h("What I used, and why.")
                  + lede('No regression, no model — a <span class="acc">natural control</span>.'), "1/5")
            + col(points([("Wilson intervals", "small cells · proportions near 0 and 1"),
                          ("Two-proportion z-tests", "pooled variance · diff, z, p reported"),
                          ("Explicit denominators", "D7 observable for 72.5% only"),
                          ("Multiple comparisons", "1 significant stratum in 5 · reported as such")],
                         num=True), "6/13"))


@slide("Appendix · Full table", "table")
def _(i, n):
    return (kicker("Appendix · full metric table")
            + col(h("Tiers, intervals, denominators.")
                  + table(["Metric", "High", "Low", "Didn't take", "n · H / L / D"], [
                      ["D1 — target", "69.6% [62.1–76.3]", "58.4% [55.3–61.5]", "21.7% [20.9–22.6]", "158 / 953 / 8,845"],
                      ["D3", "57.0% [49.2–64.4]", "34.4% [31.5–37.5]", "10.0% [9.4–10.6]", "158 / 953 / 8,845"],
                      ["D7", "39.1% [31.2–47.6]", "18.0% [15.4–21.0]", "6.9% [6.3–7.5]", "133 / 737 / 6,345"],
                      ["Unsubscribe", "11.4% [7.3–17.3]", "11.4% [9.6–13.6]", "14.3% [13.6–15.1]", "158 / 953 / 8,845"],
                      ["Lessons, all courses", "19.28", "6.38", "1.81", "—"],
                      ["Active days", "5.37", "3.46", "1.76", "—"],
                      ["CSAT · raters", "3.33 (158)", "3.53 (845)", "3.74 (3,740)", "—"],
                  ], accent_cell=(0, 1)), "1/13")
            + col(lede("95% Wilson · anchored on each user's first app day."
                       + ref("Full tier table", "deliverable/appendix/02_main-output.txt")), "1/13"))


@slide("Appendix · Data quality", "index")
def _(i, n):
    ix = '<div class="index tight">'
    for c, ttl, d in [("01", "No hold-out group", "starts on every day of the window · no control arm"),
                      ("02", "14-day window", "D7 unobservable for 27.5% · unsub rates are floors"),
                      ("03", "Two quiz vocabularies pooled", "“Full-time worker” 28.5% vs “employee” 11.8%"),
                      ("04", "Popup carries no challenge id", "338 is 99.7% of starts — impact negligible"),
                      ("05", "“7-Day Challenge” ships 8 lessons", "promise and payload off by one")]:
        ix += (f'<div class="ix"><span class="ixc{" acc" if c == "01" else ""}">{c}</span>'
               f'<span class="ixt"><b>{e(ttl)}</b> — {e(d)}</span></div>')
    ix += "</div>"
    return (kicker("Appendix · data quality")
            + col(h("Flags before anyone acts."), "1/6")
            + col(lede("Two are severe enough to state before any decision."
                       + ref("Data-quality flags", "analysis/03_supplement.py §E")), "7/13")
            + col(ix, "1/13"))


@slide("Appendix · Segment method", "chart")
def _(i, n):
    ks = [5.089, 4.787, 4.669, 4.494, 4.397, 4.314, 4.198]
    return (kicker("Appendix · how the segments were derived")
            + col(h("I asserted six. Then I tested it.")
                  + points([("Method", "k-modes · Hamming · per-attribute modes. Not k-means — a "
                                       "mean over “35–44” has no meaning"),
                            ("Sample", "38,071 respondents × 10 categorical answers"),
                            ("Finding", '<span class="acc">no elbow</span> — cost falls smoothly, ' 
                                        'so the population is a continuum, not natural kinds' 
                             + ref("k-modes clustering, 38,071 respondents",
                                   "part-a-audience/analysis/cluster_quiz.py"))]), "1/6")
            + col('<p class="charttitle">Within-cluster cost per user, k = 2 … 8</p>'
                  + linechart(ks, ["2", "3", "4", "5", "6", "7", "8"], ymin=4.0, ymax=5.2,
                              fmt=lambda v: f"{v:.2f}")
                  + '<p class="src">Six is a resolution I chose and defended — not a count the '
                    'data forced. Two authored segments (Gen Z, Burned Doer) did not survive; one '
                    'real cluster (The Adept, 20.9%) was missing from the framework entirely.</p>',
                  "7/13"))


@slide("Appendix · The query", "code")
def _(i, n):
    sql = """ret AS (   -- retention off BOTH anchors, so the groups stay comparable
  SELECT a.user_id,
    MAX(IF(dd.d = DATE_ADD(a.anchor_date, INTERVAL 1 DAY),1,0)) AS ret_d1,
    MAX(IF(dd.d = DATE_ADD(a.first_seen,  INTERVAL 1 DAY),1,0)) AS fs_ret_d1 )

CASE WHEN a.ch_start_date IS NOT NULL THEN 'took_338'
     WHEN a.ch_joined = 1             THEN 'joined_338_never_started'
     WHEN a.ch_viewed  = 1            THEN 'viewed_338_never_joined'
     ELSE                                  'no_challenge' END AS group_338"""
    return (kicker("Appendix · the query")
            + col(h("One row per user.")
                  + lede('<span class="acc">Both anchors</span> in one query — that is what makes '
                         'the matched comparison possible.'), "1/5")
            + col(f'<pre class="code">{e(sql)}</pre>', "6/13"))


# ════════════════════════════════════════════ build
CSS = open(os.path.join(HERE, "presentation", "deck_style.css")).read()


def build(make_pdf=False):
    n = len(SLIDES)
    ridx = next(i for i, s in enumerate(SLIDES) if s["layout"] == "refs")
    bodies = [None] * n
    global CUR_SLIDE
    for i, s in enumerate(SLIDES):            # render everything else first so REFS is complete
        if i != ridx:
            CUR_SLIDE = i + 1
            bodies[i] = s["fn"](i + 1, n)
    CUR_SLIDE = ridx + 1
    bodies[ridx] = SLIDES[ridx]["fn"](ridx + 1, n)
    CUR_SLIDE = 0

    out = []
    for i, (s, b) in enumerate(zip(SLIDES, bodies), 1):
        cls = f'slide {s["layout"]}' if s["layout"] in ("title", "divider") else "slide"
        foot = (f'<div class="foot"><span>{e(s["section"])}</span>'
                f'<span>{i:02d} / {n:02d}</span></div>')
        out.append(f'<section class="{cls}" id="s{i}">{b}{foot}</section>')

    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<title>Jobescape — PM Test Assignment</title>\n'
           f"<style>\n{font_face_css()}\n{CSS}\n@page{{size:1920px 1080px;margin:0}}\n</style>\n"
           "</head>\n<body>\n" + "\n".join(out) + "\n</body>\n</html>\n")
    with open(OUT_HTML, "w") as f:
        f.write(doc)

    layouts = [s["layout"] for s in SLIDES]
    dupes = [(i + 1, a) for i, (a, b) in enumerate(zip(layouts, layouts[1:])) if a == b]
    print(f"  {n} slides ({MAIN_COUNT} main + {n - MAIN_COUNT} appendix) · {len(REFS)} references")
    print(f"  {len(set(layouts))} layouts · consecutive repeats: {dupes or 'none'}")

    # A diagram label that had to shrink to fit is legal but illegible next to its siblings —
    # rewrite it or widen its box rather than letting the deck ship with a 12pt caption.
    shrunk = shrink_report()
    if shrunk:
        print(f"  ⚠ {len(shrunk)} diagram labels shrank to fit — rewrite or widen the box:")
        for s, a, b in shrunk:
            print(f"      {a} -> {b}pt   {s}")

    print(f"  -> {OUT_HTML}  ({os.path.getsize(OUT_HTML)/1048576:.2f} MB, self-contained)")

    if make_pdf:
        r = subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                            "--no-pdf-header-footer", "--virtual-time-budget=20000",
                            f"--print-to-pdf={OUT_PDF}", f"file://{OUT_HTML}"],
                           capture_output=True, timeout=300)
        print(f"  pdf exit {r.returncode} -> {OUT_PDF if os.path.exists(OUT_PDF) else 'FAILED'}")


if __name__ == "__main__":
    build("--pdf" in sys.argv)
