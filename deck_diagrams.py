#!/usr/bin/env python3
"""Engineering + product diagrams for the deck, as inline SVG.

Five notations, each chosen because it carries an argument the prose could not:

  block_diagram   the acquisition-to-product chain, and the point where it breaks
  dfd             data-flow: how every published number was produced and verified
  erd             the two BigQuery tables and the key that joins them
  pbd             product breakdown of the Challenge — which parts shipped, which never did
  state_flow      user states through the feature, with the drop on every transition

Everything is ink-on-paper with one accent element, matching the deck.
"""

INK = "#14120F"
MUTED = "#6E6A61"
ACCENT = "#C2461F"
RULE = "#C9C3B7"
FILL = "#EFEBE2"
FILL_ACC = "#F7E2DA"
PAPER = "#FCFBF8"
MONO = "IBM Plex Mono, monospace"
SANS = "Inter, sans-serif"


# Auto-shrink is a safety net, not a layout strategy: a label that has to drop several points
# to fit is illegible next to its siblings and must be rewritten or given a bigger box. Anything
# that shrinks past the tolerance is reported by shrink_report() and printed by the build.
SHRINK_TOLERANCE = 2
SHRUNK = []


def _tw(s, size, mono, weight=400, ls_em=0.0):
    """Estimate rendered width. Factors calibrated against Chrome by check_diagram_fit.py."""
    per = 0.620 if mono else 0.610
    return len(s) * size * per + max(len(s) - 1, 0) * size * ls_em


def _pair(a, b, avail):
    """Budget two labels sharing one row. Each gets what it needs; slack is split evenly, so a
    long name and a short type never fight over a fixed ratio that suits neither."""
    na = _tw(a[0], a[1], a[2], a[3], .02)
    nb = _tw(b[0], b[1], b[2], b[3], .02)
    if na + nb <= avail:
        pad = (avail - na - nb) / 2
        return na + pad, nb + pad
    return avail * na / (na + nb), avail * nb / (na + nb)


def _t(x, y, s, size=21, fill=INK, anchor="start", weight=400, mono=False, ls=".02em", maxw=None):
    """A text node. If `maxw` is given, the size shrinks until the label fits its box.

    `data-maxw` is emitted so check_diagram_fit.py can verify the real rendered width in a
    browser rather than trusting the estimate — text spilling out of a box is exactly the
    defect that eyeballing misses.
    """
    fam = MONO if mono else SANS
    ls_em = float(str(ls).replace("em", "") or 0)
    attrs = ""
    if maxw:
        orig = size
        while size > 11 and _tw(s, size, mono, weight, ls_em) > maxw:
            size -= 1
        if orig - size > SHRINK_TOLERANCE:
            SHRUNK.append((s, orig, size))
        est = _tw(s, size, mono, weight, ls_em)
        attrs = (f' data-maxw="{maxw:.0f}" data-est="{est:.0f}"'
                 f' data-cls="{"mono" if mono else ("bold" if weight >= 600 else "reg")}"')
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}"{attrs}>{s}</text>')


def _box(x, y, w, h, fill=PAPER, stroke=RULE, sw=2, rx=0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def _arrow(x1, y1, x2, y2, stroke=MUTED, sw=2.5, head=13):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(a), y2 - head * math.sin(a)
    hw = head * .52
    p1 = (bx - hw * math.sin(a), by + hw * math.cos(a))
    p2 = (bx + hw * math.sin(a), by - hw * math.cos(a))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{stroke}" '
            f'stroke-width="{sw}"/>'
            f'<path d="M{x2:.1f},{y2:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" '
            f'fill="{stroke}"/>')


def _wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out or [""]


# ══════════════════════════════════════════════════ BLOCK DIAGRAM
def block_diagram(w=1180):
    """Ads → quiz → paywall → product. The break is after the money is taken."""
    h, bw, bh, gap = 320, 262, 104, 44
    y = 96
    o = [f'<svg viewBox="-14 -10 {w+28} {h+20}" width="100%">']
    blocks = [("Meta ads", "~1,000 / day"), ("Quiz funnel", "37 pages"),
              ("Paywall", "pay before entry"), ("The product", "50.2% finish nothing")]
    for i, (name, sub) in enumerate(blocks):
        x = i * (bw + gap)
        acc = i == 3
        o.append(_box(x, y, bw, bh, FILL_ACC if acc else FILL,
                      ACCENT if acc else RULE, 2.5 if acc else 2))
        o.append(_t(x + bw / 2, y + 48, name, 27, ACCENT if acc else INK, "middle", 600,
                    maxw=bw - 28))
        o.append(_t(x + bw / 2, y + 82, sub, 19, ACCENT if acc else MUTED, "middle", 400, True,
                    maxw=bw - 20))
        if i < 3:
            o.append(_arrow(x + bw + 8, y + bh / 2, x + bw + gap - 8, y + bh / 2))
    # the seam
    o.append(f'<line x1="{2*(bw+gap) - gap/2:.1f}" y1="60" x2="{2*(bw+gap) - gap/2:.1f}" '
             f'y2="{y+bh+56}" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="7 7"/>')
    o.append(_t(2 * (bw + gap) - gap / 2 - 16, 52, "MONEY TAKEN HERE", 18, ACCENT, "end", 400, True, ".07em"))
    o.append(_t(2 * (bw + gap) - gap / 2 + 16, 52, "VALUE OWED FROM HERE", 18, ACCENT, "start", 400, True, ".07em"))
    o.append(_t(0, y + bh + 56, "ACQUISITION — WORKS", 18, MUTED, "start", 400, True, ".07em"))
    o.append(_t(w, y + bh + 56, "ACTIVATION — NEVER BUILT", 18, ACCENT, "end", 400, True, ".07em"))
    return "".join(o) + "</svg>"


# ══════════════════════════════════════════════════ DFD
def dfd(w=1180):
    """Level-1 data-flow: source → processes → store → verification → outputs."""
    h = 420
    o = [f'<svg viewBox="-14 -10 {w+28} {h+20}" width="100%">']
    # external entity
    o.append(_box(0, 90, 210, 110, PAPER, INK, 2.5))
    o.append(_t(105, 132, "BigQuery", 25, INK, "middle", 600, maxw=186))
    o.append(_t(105, 162, "sql_assessment", 18, MUTED, "middle", 400, True, maxw=186))
    o.append(_t(105, 70, "EXTERNAL ENTITY", 16, MUTED, "middle", 400, True, ".07em"))
    # processes
    procs = [(300, "1.0", "Extract", "5 SQL queries"),
             (600, "2.0", "Analyse", "6 Python scripts"),
             (900, "3.0", "Verify", "91 assertions")]
    for x, num, name, sub in procs:
        acc = num == "3.0"
        o.append(f'<rect x="{x}" y="90" width="210" height="110" rx="55" fill="{FILL_ACC if acc else FILL}" '
                 f'stroke="{ACCENT if acc else RULE}" stroke-width="{2.5 if acc else 2}"/>')
        o.append(_t(x + 105, 124, f"{num}  {name}", 25, ACCENT if acc else INK, "middle", 600,
                    maxw=186))
        o.append(_t(x + 105, 156, sub, 18, ACCENT if acc else MUTED, "middle", 400, True, maxw=186))
    for x in (210, 510, 810):
        o.append(_arrow(x + 8, 145, x + 82, 145))
    # data store
    o.append(f'<line x1="300" y1="270" x2="810" y2="270" stroke="{INK}" stroke-width="2.5"/>')
    o.append(f'<line x1="300" y1="336" x2="810" y2="336" stroke="{INK}" stroke-width="2.5"/>')
    o.append(f'<line x1="300" y1="270" x2="300" y2="336" stroke="{INK}" stroke-width="2.5"/>')
    o.append(_t(320, 296, "D1", 20, MUTED, "start", 400, True))
    o.append(_t(320, 322, "one row per user · 9,956 rows", 21, INK, "start", 500, maxw=470))
    o.append(_arrow(405, 205, 405, 262))
    o.append(_arrow(705, 262, 705, 205))
    o.append(_t(418, 240, "write", 18, MUTED, "start", 400, True))
    o.append(_t(692, 240, "read", 18, MUTED, "end", 400, True))
    # output
    o.append(_arrow(1005, 205, 1005, 300))
    o.append(_box(900, 300, 210, 96, PAPER, INK, 2.5))
    o.append(_t(1005, 338, "Deck, dossier,", 21, INK, "middle", 500, maxw=186))
    o.append(_t(1005, 364, "submission", 21, INK, "middle", 500, maxw=186))
    o.append(_t(1005, 412, "ANY DRIFT FAILS THE BUILD", 18, ACCENT, "middle", 400, True, ".07em"))
    return "".join(o) + "</svg>"


# ══════════════════════════════════════════════════ ERD
def erd(w=1180):
    """The two tables, their keys, and the cardinality between them."""
    h, bw = 430, 500
    o = [f'<svg viewBox="-14 -10 {w+28} {h+20}" width="100%">']
    tables = [
        (0, "app_events", "680,224 rows", [
            ("user_id", "INT64  FK"), ("event_name", "STRING"), ("timestamp", "TIMESTAMP"),
            ("course_id", "INT64"), ("lesson_id", "INT64"), ("csat_score", "INT64"),
            ("unsubscribe_reason", "STRING"), ("path", "STRING")]),
        (w - bw, "subscribe_events", "1 row per purchase", [
            ("user_id", "INT64  PK"), ("subscription", "STRING"), ("age  ·  gender", "STRING"),
            ("goal  ·  status", "STRING"), ("country_code", "STRING"), ("utm_source", "STRING"),
            ("payment_method", "STRING"), ("cohort_day", "INT64")]),
    ]
    for x, name, sub, fields in tables:
        o.append(_box(x, 30, bw, 372, PAPER, INK, 2.5))
        o.append(f'<rect x="{x}" y="30" width="{bw}" height="56" fill="{INK}"/>')
        m1, m2 = _pair((name, 24, True, 600), (sub, 17, True, 400), bw - 60)
        o.append(_t(x + 22, 67, name, 24, PAPER, "start", 600, True, maxw=m1))
        o.append(_t(x + bw - 22, 67, sub, 17, "#B8B2A6", "end", 400, True, maxw=m2))
        for i, (f, ty) in enumerate(fields):
            yy = 118 + i * 35
            key = "FK" in ty or "PK" in ty
            m1, m2 = _pair((f, 21, True, 600 if key else 400), (ty, 19, True, 400), bw - 60)
            o.append(_t(x + 22, yy, f, 21, ACCENT if key else INK, "start", 600 if key else 400,
                        True, maxw=m1))
            o.append(_t(x + bw - 22, yy, ty, 19, ACCENT if key else MUTED, "end", 400, True,
                        maxw=m2))
            if i < len(fields) - 1:
                o.append(f'<line x1="{x+22}" y1="{yy+13}" x2="{x+bw-22}" y2="{yy+13}" '
                         f'stroke="{RULE}" stroke-width="1"/>')
    # relationship, crow's foot: one purchase -> many events
    mx1, mx2, my = bw, w - bw, 128
    o.append(f'<line x1="{mx1}" y1="{my}" x2="{mx2}" y2="{my}" stroke="{ACCENT}" stroke-width="2.5"/>')
    o.append(f'<path d="M{mx1+30},{my-16} L{mx1},{my} L{mx1+30},{my+16}" fill="none" '
             f'stroke="{ACCENT}" stroke-width="2.5"/>')          # crow's foot = many
    o.append(f'<line x1="{mx2-34}" y1="{my-15}" x2="{mx2-34}" y2="{my+15}" stroke="{ACCENT}" '
             f'stroke-width="2.5"/>')                             # bar = exactly one
    o.append(_t((mx1 + mx2) / 2, my - 26, "user_id", 22, ACCENT, "middle", 600, True))
    o.append(_t((mx1 + mx2) / 2, my + 40, "MANY EVENTS", 18, MUTED, "middle", 400, True, ".07em"))
    o.append(_t((mx1 + mx2) / 2, my + 66, "ONE PURCHASE", 18, MUTED, "middle", 400, True, ".07em"))
    o.append(_t(w / 2, h - 6, "EVERY app_events USER HAS A PURCHASE ROW — \"USER\" AND \"PAYER\" ARE THE SAME SET",
                18, ACCENT, "middle", 400, True, ".06em"))
    return "".join(o) + "</svg>"


# ══════════════════════════════════════════════════ PBD
def pbd(w=1180):
    """Product breakdown of the Challenge. The status on each leaf is the argument."""
    ROOT_W, ROOT_H = 400, 66
    GRP_Y, GRP_H = 140, 54
    LEAF_H, LEAF_GAP = 48, 12
    LEAF_Y = 212
    kids = [("Distribution", [("Homepage popup", "ships"), ("Skills catalogue", "ships")]),
            ("Content", [("8 lessons", "ships"), ("6 languages", "ships")]),
            ("Habit engine", [("Streak counter", "shows 0"), ("Daily gate", "NOT BUILT"),
                              ("Scheduled unlock", "NOT BUILT")]),
            ("Reward", [("Certificate", "0.2% take it")])]
    cw, gap = 262, 44
    x0 = (w - (len(kids) * cw + (len(kids) - 1) * gap)) / 2
    deepest = max(len(v) for _, v in kids)
    bottom = LEAF_Y + deepest * LEAF_H + (deepest - 1) * LEAF_GAP
    h = bottom + 46

    o = [f'<svg viewBox="-14 -10 {w+28} {h+20}" width="100%">']
    o.append(_box((w - ROOT_W) / 2, 0, ROOT_W, ROOT_H, FILL, INK, 2.5))
    o.append(_t(w / 2, 42, "7-Day Claude Challenge", 25, INK, "middle", 600, maxw=ROOT_W - 34))
    o.append(f'<line x1="{w/2}" y1="{ROOT_H}" x2="{w/2}" y2="{GRP_Y-40}" stroke="{RULE}" stroke-width="2"/>')
    o.append(f'<line x1="{x0+cw/2}" y1="{GRP_Y-40}" x2="{x0+3*(cw+gap)+cw/2}" y2="{GRP_Y-40}" '
             f'stroke="{RULE}" stroke-width="2"/>')

    for i, (grp, items) in enumerate(kids):
        x = x0 + i * (cw + gap)
        acc = grp == "Habit engine"
        col = ACCENT if acc else RULE
        o.append(f'<line x1="{x+cw/2}" y1="{GRP_Y-40}" x2="{x+cw/2}" y2="{GRP_Y}" '
                 f'stroke="{col}" stroke-width="{2.5 if acc else 2}"/>')
        o.append(_box(x, GRP_Y, cw, GRP_H, FILL_ACC if acc else FILL, col, 2.5 if acc else 2))
        o.append(_t(x + cw / 2, GRP_Y + 35, grp, 22, ACCENT if acc else INK, "middle", 600,
                    maxw=cw - 32))
        prev_bottom = GRP_Y + GRP_H
        for j, (nm, st) in enumerate(items):
            top = LEAF_Y + j * (LEAF_H + LEAF_GAP)
            missing = st == "NOT BUILT"
            # connector runs between boxes, never through one
            o.append(f'<line x1="{x+cw/2}" y1="{prev_bottom}" x2="{x+cw/2}" y2="{top}" '
                     f'stroke="{RULE}" stroke-width="1.5"/>')
            o.append(_box(x + 16, top, cw - 32, LEAF_H, PAPER,
                          ACCENT if missing else RULE, 2.5 if missing else 1.5,
                          dash="6 5" if missing else None))
            o.append(_t(x + cw / 2, top + 21, nm, 19, INK, "middle", 500, maxw=cw - 52))
            o.append(_t(x + cw / 2, top + 40, st.upper(), 14,
                        ACCENT if st != "ships" else MUTED, "middle", 400, True, ".07em",
                        maxw=cw - 52))
            prev_bottom = top + LEAF_H
    o.append(_t(w / 2, bottom + 32, "THE HYPOTHESIS NEEDED THE DASHED BOXES. THEY WERE NEVER SHIPPED.",
                19, ACCENT, "middle", 400, True, ".06em"))
    return "".join(o) + "</svg>"


# ══════════════════════════════════════════════════ STATE FLOW
def state_flow(w=1180):
    """User states through the feature, with the loss on every transition."""
    h = 410
    states = [("All payers", "9,956"), ("Saw popup", "3,140"), ("Viewed page", "2,109"),
              ("Started", "1,111"), ("Lesson 1", "612"), ("Finished", "48")]
    drops = ["−68.5%", "−32.8%", "−47.3%", "−44.9%", "−92.2%"]
    bw, gap = 168, 34
    x0 = (w - (len(states) * bw + (len(states) - 1) * gap)) / 2
    y = 118
    o = [f'<svg viewBox="-14 -10 {w+28} {h+20}" width="100%">']
    for i, (nm, n) in enumerate(states):
        x = x0 + i * (bw + gap)
        acc = i == 3
        o.append(_box(x, y, bw, 104, FILL_ACC if acc else FILL, ACCENT if acc else RULE,
                      2.5 if acc else 2, rx=6))
        o.append(_t(x + bw / 2, y + 42, nm, 21, ACCENT if acc else INK, "middle", 600, maxw=bw - 20))
        o.append(_t(x + bw / 2, y + 76, n, 24, ACCENT if acc else MUTED, "middle", 500, True,
                    maxw=bw - 20))
        if i < len(states) - 1:
            o.append(_arrow(x + bw + 6, y + 52, x + bw + gap - 6, y + 52))
            worst = drops[i] in ("−68.5%", "−92.2%")
            o.append(_t(x + bw + gap / 2, y - 18, drops[i], 20,
                        ACCENT if worst else MUTED, "middle", 600 if worst else 400, True))
    o.append(_t(x0, y - 62, "LOSS AT EACH TRANSITION", 18, MUTED, "start", 400, True, ".07em"))
    o.append(_t(x0, y + 168, "TWO CLIFFS: NEVER OFFERED IT, AND PRESSED START THEN GOT NOTHING",
                19, ACCENT, "start", 400, True, ".06em"))
    return "".join(o) + "</svg>"


def shrink_report():
    """Labels that had to shrink more than SHRINK_TOLERANCE points to fit their box."""
    return sorted(set(SHRUNK), key=lambda r: r[1] - r[2], reverse=True)
