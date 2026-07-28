#!/usr/bin/env python3
"""Verify that no diagram label spills outside the box it belongs to.

Every in-box label is emitted with `data-maxw` (see deck_diagrams._t). This loads the deck in
one 1920x1080 headless window — no giant screenshots — and compares each label's REAL rendered
width, via getComputedTextLength(), against its budget.

It also reports the worst estimate error so the width factors in `_tw` can be recalibrated
against the browser instead of guessed.
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
  var bad = [], worst = 0, worstTxt = '', cal = {};
  document.querySelectorAll('text[data-maxw]').forEach(function (t) {
    var budget = parseFloat(t.dataset.maxw);
    var real;
    try { real = t.getComputedTextLength(); } catch (e) { return; }
    var svg = t.closest('svg');
    // getComputedTextLength is in user units, same space as data-maxw — compare directly
    var ratio = real / budget;
    if (ratio > worst) { worst = ratio; worstTxt = t.textContent.slice(0, 30); }
    var c = t.dataset.cls, est = parseFloat(t.dataset.est);
    if (est > 0) { (cal[c] = cal[c] || []).push(real / est); }
    if (real > budget + 1) {
      bad.push(t.textContent.slice(0, 34) + ' :: ' + Math.round(real) + ' > ' + Math.round(budget));
    }
  });
  var cs = Object.keys(cal).map(function (k) {
    var v = cal[k]; return k + '=' + Math.max.apply(null, v).toFixed(3) + '/' + v.length;
  }).join(' ');
  document.title = 'FIT::' + bad.join(';;') + '##' + worst.toFixed(3) + '##' + worstTxt + '##' + cs;
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
             "--window-size=1920,1080", "--virtual-time-budget=12000", "--dump-dom",
             f"file://{tmp.name}"], capture_output=True, timeout=180, text=True)
        m = re.search(r"FIT::(.*?)</title>", r.stdout, re.S)
        if not m:
            print("  could not read probe output")
            return 1
        payload, worst, worst_txt, cal = m.group(1).split("##")
        rows = [x for x in payload.split(";;") if x]
        n = len(re.findall(r'data-maxw', doc))
        print(f"  {n} bounded diagram labels checked")
        print(f"  widest label uses {float(worst):.0%} of its box  ({worst_txt.strip()})")
        print(f"  estimator error, worst real/est per class: {cal.strip()}")
        if rows:
            print(f"  {len(rows)} OVERFLOW its box:")
            for x in rows:
                print("    ", x)
            return 1
        print("  no diagram text escapes its box ✓")
        return 0
    finally:
        os.unlink(tmp.name)


if __name__ == "__main__":
    sys.exit(main())
