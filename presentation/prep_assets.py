#!/usr/bin/env python3
"""Crop the product screenshots for the deck.

Two jobs: (1) strip browser chrome so the slide shows the product, not my desktop;
(2) REMOVE PERSONALLY IDENTIFYING INFO — the app sidebar footer renders my real name and
email on every page, and this deck goes to a third party. Every crop below is chosen to
exclude that region; `verify_no_pii()` re-checks the crop box afterwards.
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "part-a-audience", "materials", "walkthrough")
OUT = os.path.join(HERE, "assets")

# The sidebar footer (name + email) occupies roughly x<235, y>1010 on the 1920x1080 captures.
PII_ZONE = (0, 1000, 240, 1080)

CROPS = {
    # name              source              box (l, t, r, b)               scale
    "challenge-home":   ("challengespage1.png",  (237, 118, 1908, 880), 1.0),
    "challenge-streak": ("challengespage1.png",  (1600, 128, 1908, 180), 2.0),
    "automation":       ("automationpage.png",   (250, 190, 1908, 700), 1.0),
    "ask-mark":         ("automationpage.png",   (1750, 905, 1908, 985), 3.0),
    # the evidence is the credits pill, not the empty chat page around it
    "chat-credits":     ("chatpage.png",         (1600, 128, 1908, 180), 3.0),
    "home":             ("homepage.png",         (237, 118, 1908, 880), 1.0),
    "assistants":       ("assistantspage.png",   (237, 118, 1908, 880), 1.0),
}
# these two are already tight product captures with no sidebar
COPIES = {"paywall": "paywall.png", "mark-chat": "chatwithMark.png"}


def overlaps(box, zone):
    l, t, r, b = box
    zl, zt, zr, zb = zone
    return not (r <= zl or l >= zr or b <= zt or t >= zb)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (src, box, scale) in CROPS.items():
        im = Image.open(os.path.join(SRC, src)).convert("RGB")
        if im.size == (1920, 1080) and overlaps(box, PII_ZONE):
            raise SystemExit(f"REFUSED: crop '{name}' overlaps the name/email region {PII_ZONE}")
        c = im.crop(box)
        if scale != 1.0:
            c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
        p = os.path.join(OUT, f"{name}.png")
        c.save(p, optimize=True)
        print(f"  {name:18s} {c.width}x{c.height}  <- {src}{box}")

    for name, src in COPIES.items():
        im = Image.open(os.path.join(SRC, src)).convert("RGB")
        p = os.path.join(OUT, f"{name}.png")
        im.save(p, optimize=True)
        print(f"  {name:18s} {im.width}x{im.height}  <- {src} (whole)")

    print(f"\n{len(CROPS)+len(COPIES)} assets in presentation/assets/")


if __name__ == "__main__":
    main()
