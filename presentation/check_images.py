#!/usr/bin/env python3
"""Catch screenshots that are cropped through their own content.

`object-fit:cover` with a forced height trims whichever axis overflows:

  portrait shot in a landscape box  ->  trims the bottom.  Fine — that is a deliberate
                                       top-anchored crop of a long page.
  landscape shot in a taller box    ->  trims the SIDES, through the labels, the badge,
                                        whatever the slide was pointing at. Never fine.

This measures the real rendered box and the image's natural aspect in the browser and reports
the second case, plus any image displayed so small its UI text cannot be read from a room.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "Jobescape-PM-Deck.html")

MIN_SCALE = 0.22   # below ~22% of native, product-UI text stops being readable when projected

PROBE = r"""
<script>
window.addEventListener('load', function () {
  var out = [];
  document.querySelectorAll('section img').forEach(function (im) {
    var r = im.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var sec = 0, s = im.closest('section');
    var all = document.querySelectorAll('section');
    for (var i = 0; i < all.length; i++) { if (all[i] === s) { sec = i + 1; break; } }
    var natA = im.naturalWidth / im.naturalHeight, boxA = r.width / r.height;
    var fit = getComputedStyle(im).objectFit;
    var cap = s.querySelector('figcaption');
    var lost = 0;
    if (fit === 'cover' && natA > boxA + 0.01) {
      lost = 1 - (boxA / natA);                       // fraction of the WIDTH thrown away
    }
    out.push([sec, Math.round(r.width), Math.round(r.height), natA.toFixed(2), boxA.toFixed(2),
              fit, lost.toFixed(3), (r.width / im.naturalWidth).toFixed(3),
              (cap ? cap.textContent : '').slice(0, 26)].join(';;;'));
  });
  document.title = 'IMG::' + out.join('@@@');
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
        m = re.search(r"IMG::(.*?)</title>", r.stdout, re.S)
        if not m:
            print("  could not read probe output")
            return 1
        rows = [x.split(";;;") for x in m.group(1).strip().split("@@@") if x.strip()]
        bad = [x for x in rows if float(x[6]) > 0.02]
        small = [x for x in rows if float(x[7]) < MIN_SCALE]
        print(f"  {len(rows)} images measured")
        if bad:
            print(f"  {len(bad)} cropped horizontally — content is being cut off:")
            for x in bad:
                print(f"      slide {x[0]:>2}  loses {float(x[6]):.0%} of width  "
                      f"(natural {x[3]} in a {x[4]} box)  {x[8]}")
        if small:
            print(f"  {len(small)} shown below {MIN_SCALE:.0%} of native — UI text unreadable:")
            for x in small:
                print(f"      slide {x[0]:>2}  {x[1]}x{x[2]}px = {float(x[7]):.0%} of native  {x[8]}")
        if not bad and not small:
            print("  no image is cropped through its content or shrunk past legibility ✓")
        return 1 if bad else 0
    finally:
        os.unlink(tmp.name)


if __name__ == "__main__":
    sys.exit(main())
