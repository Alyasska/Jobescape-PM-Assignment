#!/usr/bin/env python3
"""Find slides that waste the frame, and text that wraps into ragged slivers.

Two defects the overflow check cannot see, because both are technically "inside the box":

  FILL    the content bounding box covers too little of the safe area — a slide that reads
          as under-set, which is the complaint "less empty space, bigger font".
  RAGGED  a paragraph wrapping into >=3 lines that average under ~24 characters. Narrow
          columns turn a short phrase into a ragged stack; the fix is a wider column.

DOM measurement only — no screenshots.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "Jobescape-PM-Deck.html")

PROBE = r"""
<script>
window.addEventListener('load', function () {
  var SAFE = {t: 80, b: 1080 - 126, l: 128, r: 1920 - 128};
  var area = (SAFE.r - SAFE.l) * (SAFE.b - SAFE.t);
  var out = [];
  document.querySelectorAll('section').forEach(function (s, si) {
    if (s.classList.contains('title') || s.classList.contains('divider')) return;
    var top = s.getBoundingClientRect().top;
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9, ragged = [];
    s.querySelectorAll('*').forEach(function (el) {
      if (el.closest('.foot')) return;
      var r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      if (!el.children.length || el.tagName === 'SVG' || el.tagName === 'svg' ||
          el.tagName === 'IMG' || el.tagName === 'TABLE') {
        x0 = Math.min(x0, r.left); x1 = Math.max(x1, r.right);
        y0 = Math.min(y0, r.top - top); y1 = Math.max(y1, r.bottom - top);
      }
      // ragged wrap: a leaf text node stacked into many short lines
      // headlines are display type — wrapping big and short is the intended look, not a
      // defect. Reference paths sit in deliberately narrow columns. Neither is ragged.
      if (el.closest('.h') || el.closest('.reflist')) return;
      if (!el.children.length && el.textContent.trim().length > 20) {
        var lh = parseFloat(getComputedStyle(el).lineHeight) || 0;
        if (lh > 0) {
          var lines = Math.round(r.height / lh);
          var perLine = el.textContent.trim().length / Math.max(lines, 1);
          if (lines >= 3 && perLine < 24) {
            ragged.push(lines + 'L@' + perLine.toFixed(0) + 'ch "' +
                        el.textContent.trim().slice(0, 26) + '"');
          }
        }
      }
    });
    if (x0 > 1e8) return;
    var fill = ((x1 - x0) * (y1 - y0)) / area;
    var kick = s.querySelector('.kicker');
    out.push([si + 1, fill.toFixed(3), (kick ? kick.textContent : '').slice(0, 34),
              ragged.join(' | ')].join(';;;'));
  });
  document.title = 'DENS::' + out.join('@@@');
});
</script>
"""


def main():
    doc = open(DECK).read().replace("</body>", PROBE + "</body>")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", dir=HERE, delete=False)
    tmp.write(doc)
    tmp.close()
    try:
        r = subprocess.run(
            ["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
             "--window-size=1920,1080", "--virtual-time-budget=15000", "--dump-dom",
             f"file://{tmp.name}"], capture_output=True, timeout=180, text=True)
        m = re.search(r"DENS::(.*?)</title>", r.stdout, re.S)
        if not m:
            print("  could not read probe output")
            return 1
        rows = [x.split(";;;") for x in m.group(1).strip().split("@@@") if x.strip()]
        rows = [(int(a), float(b), c, d) for a, b, c, d in rows]

        thin = sorted([r for r in rows if r[1] < 0.55], key=lambda r: r[1])
        ragged = [r for r in rows if r[3]]
        print(f"  {len(rows)} content slides measured · "
              f"median fill {sorted(r[1] for r in rows)[len(rows)//2]:.0%}")
        if thin:
            print(f"  {len(thin)} under-set (content box < 55% of safe area):")
            for n, f, k, _ in thin:
                print(f"      slide {n:2d}  {f:.0%}  {k}")
        if ragged:
            print(f"  {len(ragged)} with ragged wrap:")
            for n, _, k, g in ragged:
                print(f"      slide {n:2d}  {k}\n                {g}")
        return 0
    finally:
        os.unlink(tmp.name)


if __name__ == "__main__":
    sys.exit(main())
