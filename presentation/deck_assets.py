#!/usr/bin/env python3
"""Embeddable assets for the deck: latin-subset webfonts + right-sized screenshots.

Everything is returned as a base64 data URI so the built deck is a single
self-contained HTML file with zero external requests.
"""
import base64
import functools
import io
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
ASSET_DIR = os.path.join(HERE, "assets")

FONTS = [
    ("Inter", 400, "Inter-400.woff2"),
    ("Inter", 600, "Inter-600.woff2"),
    ("Inter Tight", 600, "InterTight-600.woff2"),
    ("IBM Plex Mono", 400, "IBMPlexMono-400.woff2"),
]


@functools.lru_cache(maxsize=None)
def font_face_css():
    out = []
    for family, weight, fn in FONTS:
        p = os.path.join(FONT_DIR, fn)
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        out.append(
            f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(out)


@functools.lru_cache(maxsize=None)
def img(name, max_w=1100, quality=82):
    """Downscale to what the slide actually needs, then embed as a JPEG data URI."""
    im = Image.open(os.path.join(ASSET_DIR, name)).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


if __name__ == "__main__":
    css = font_face_css()
    print(f"fonts   {len(css)/1024:8.0f} KB of base64 CSS")
    for n, w in [("paywall.png", 620), ("mark-chat.png", 460), ("chat-credits.png", 980),
                 ("proto-phone-gate.png", 520), ("automation.png", 1100),
                 ("challenge-streak.png", 620)]:
        print(f"  {n:26s} @{w:>5}px -> {len(img(n, w))/1024:7.0f} KB")
