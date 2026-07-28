#!/usr/bin/env python3
"""Generate the Part D figures for the presenter reference, as inline SVG.

Three things the prose cannot show: how fast each plan's cohort decays, where the money in one
LTV actually comes from, and how the A/B outcome moves with the upgrade rate. Values are computed
here from the same inputs as ltv_model.py, so the figures cannot drift from the numbers.
"""
INK, MUTED, ACCENT, RULE = "#14120F", "#6E6A61", "#C2461F", "#DED9CF"
MONO = "IBM Plex Mono, monospace"

PLANS = {
    "1-week":  dict(C=[.55, .50, .60, .75, .80, .80, .80, .80, .80, .80, .80, .80],
                    intro=6.93,  rec=39.99, up=0.72),
    "4-week":  dict(C=[.67, .65, .70, .75, .80, .80, .80, .80, .80, .80, .80, .80],
                    intro=19.99, rec=39.99, up=24.60),
    "12-week": dict(C=[.64, .57, .65, .75, .75, .75, .75, .75, .75, .75, .75, .75],
                    intro=39.99, rec=62.99, up=24.60),
}
FEE = 0.12


def surv(C):
    out, acc = [], 1.0
    for c in C:
        acc *= c
        out.append(acc)
    return out


def _t(x, y, s, size=13, fill=MUTED, anchor="start", weight=400, mono=True):
    fam = MONO if mono else "Inter, sans-serif"
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>')


def survival_chart(w=700, h=250):
    L, R, T, B = 46, 14, 16, 34
    pw, ph = w - L - R, h - T - B
    o = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px">']
    for frac in (0, .25, .5, .75, 1.0):
        y = T + ph * (1 - frac)
        o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{w-R}" y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        o.append(_t(L - 8, y + 4, f"{frac*100:.0f}%", 11, MUTED, "end"))
    styles = {"1-week": ("3 3", MUTED), "4-week": (None, ACCENT), "12-week": ("7 3", INK)}
    for name, p in PLANS.items():
        s = [1.0] + surv(p["C"])
        pts = " ".join(f"{L + pw*i/(len(s)-1):.1f},{T + ph*(1-v):.1f}" for i, v in enumerate(s))
        dash, col = styles[name]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.2"{d}/>')
        o.append(_t(L + pw + 2, T + ph * (1 - s[-1]) + 4, "", 11))
    o.append(_t(L, h - 8, "period  0", 11))
    o.append(_t(L + pw, h - 8, "12", 11, MUTED, "end"))
    o.append(_t(L + 6, T + 12, "— 4-week (accent) · ·· 1-week · – – 12-week", 11, MUTED))
    return "".join(o) + "</svg>"


def waterfall(w=700, h=250):
    """Where one 4-week subscriber's $123.70 comes from."""
    steps = [("intro", 19.99, MUTED), ("recurring", 95.98, MUTED),
             ("upsells", 24.60, MUTED), ("12% fee", -16.87, ACCENT)]
    total = 140.57
    L, T, BH, GAP = 96, 22, 30, 12
    o = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px">']
    scale = (w - L - 80) / total
    run = 0.0
    for i, (lab, v, col) in enumerate(steps):
        y = T + i * (BH + GAP)
        x0 = L + (run if v > 0 else run + v) * scale
        o.append(f'<rect x="{x0:.1f}" y="{y}" width="{abs(v)*scale:.1f}" height="{BH}" fill="{col}"/>')
        o.append(_t(L - 10, y + 20, lab, 13, INK, "end"))
        o.append(_t(x0 + abs(v) * scale + 8, y + 20, f"{v:+.2f}", 13, col))
        run += v
    y = T + len(steps) * (BH + GAP)
    o.append(f'<rect x="{L}" y="{y}" width="{run*scale:.1f}" height="{BH}" fill="{INK}"/>')
    o.append(_t(L - 10, y + 20, "NET LTV", 13, INK, "end", 600))
    o.append(_t(L + run * scale + 8, y + 20, f"${run:.2f}", 14, INK, "start", 600))
    return "".join(o) + "</svg>"


def breakeven(w=700, h=250):
    """Test-arm net LTV against upgrade conversion, both horizon readings."""
    ctrl = 123.70
    L, R, T, B = 60, 16, 18, 34
    pw, ph = w - L - R, h - T - B
    lo, hi = 119.0, 137.0
    o = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px">']
    for v in (120, 124, 128, 132, 136):
        y = T + ph * (1 - (v - lo) / (hi - lo))
        o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{w-R}" y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        o.append(_t(L - 8, y + 4, f"${v}", 11, MUTED, "end"))
    yc = T + ph * (1 - (ctrl - lo) / (hi - lo))
    o.append(f'<line x1="{L}" y1="{yc:.1f}" x2="{w-R}" y2="{yc:.1f}" stroke="{INK}" '
             f'stroke-width="1.6" stroke-dasharray="5 4"/>')
    o.append(_t(w - R, yc - 7, "control $123.70", 11, INK, "end"))
    for label, gain, dash in (("one year, like-for-like", 43.44, None), ("full curve — unequal horizons", 73.68, "6 3")):
        pts = []
        for i in range(41):
            p = i / 100.0
            net = (140.57 - 3.60 + p * gain) * (1 - FEE)
            pts.append(f"{L + pw*p/0.40:.1f},{T + ph*(1-(net-lo)/(hi-lo)):.1f}")
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ACCENT}" '
                 f'stroke-width="2.2"{d}/>')
    for p, txt in ((0.0829, "8.3%"), (0.0488, "4.9%")):
        x = L + pw * p / 0.40
        o.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{T+ph}" stroke="{ACCENT}" '
                 f'stroke-width="1" stroke-dasharray="2 3"/>')
        o.append(_t(x, T + ph + 15, txt, 11, ACCENT, "middle"))
    o.append(_t(L, h - 6, "upgrade conversion p", 11))
    o.append(_t(L + pw, h - 6, "40%", 11, MUTED, "end"))
    return "".join(o) + "</svg>"


if __name__ == "__main__":
    for name, fn in [("survival", survival_chart), ("waterfall", waterfall), ("breakeven", breakeven)]:
        print(f"<!--FIG:{name}-->{fn()}")
