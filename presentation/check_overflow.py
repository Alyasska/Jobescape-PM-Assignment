#!/usr/bin/env python3
"""Measure every slide in the built deck for content that escapes its frame.

Renders the deck in headless Chrome, walks each <section>, and reports any element
whose box crosses the slide's safe area. Catches the overflow bugs that are easy to
miss by eye across 40+ slides.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "Jobescape-PM-Deck.html")

PROBE = """
<script>
window.addEventListener('load', function () {
  var TOP = 80, BOT = 1080 - 126, L = 128, R = 1920 - 128, out = [];
  document.querySelectorAll('section.slide').forEach(function (s, i) {
    var sr = s.getBoundingClientRect(), worst = null;
    s.querySelectorAll('*').forEach(function (el) {
      if (el.tagName === 'SCRIPT' || el.closest('.foot') || el.closest('.src')) return;
      if (!el.getClientRects().length) return;
      var r = el.getBoundingClientRect();
      var top = r.top - sr.top, bot = r.bottom - sr.top;
      var over = Math.max(bot - BOT, TOP - top, L - r.left, r.right - R);
      if (over > 2) {
        var tag = el.className || el.tagName;
        if (!worst || over > worst.over) worst = {over: Math.round(over), what: String(tag).slice(0, 42),
                                                  bot: Math.round(bot)};
      }
    });
    if (worst) out.push((i + 1) + '|' + worst.over + '|' + worst.what + '|' + worst.bot);
  });
  document.title = 'OVF::' + out.join(';;');
});
</script>
"""


def main():
    with open(DECK) as f:
        doc = f.read()
    doc = doc.replace("</body>", PROBE + "</body>")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", dir=HERE, delete=False)
    tmp.write(doc)
    tmp.close()
    try:
        r = subprocess.run(
            ["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
             "--window-size=1920,1080", "--virtual-time-budget=15000", "--dump-dom",
             f"file://{tmp.name}"], capture_output=True, timeout=240, text=True)
        m = re.search(r"OVF::([^<]*)</title>", r.stdout)
        if not m:
            print("could not read probe output")
            return 1
        payload = m.group(1).strip()
        if not payload:
            print("  no overflow — every slide sits inside its safe area ✓")
            return 0
        rowsx = [x for x in payload.split(";;") if x]
        print(f"  {len(rowsx)} slide(s) overflow:")
        for row in rowsx:
            idx, over, what, bot = row.split("|")
            print(f"    slide {int(idx):02d}  +{over:>4}px   bottom@{bot:>4}   {what}")
        return 1
    finally:
        os.unlink(tmp.name)


if __name__ == "__main__":
    sys.exit(main())
