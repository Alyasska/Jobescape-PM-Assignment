#!/usr/bin/env python3
"""Enforce the one-accent-per-slide rule.

Counts accent regions per slide: each `class="acc"` in the HTML counts one, and a chart
containing the accent fill counts one (the highlighted series is a single region).
Section dividers are exempt — they are full-bleed accent by design.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "Jobescape-PM-Deck.html")
ACCENT = "#C2461F"


def main():
    doc = open(DECK).read()
    body = doc[doc.index("<body>"):]
    sections = re.findall(r'<section class="([^"]*)"[^>]*>(.*?)</section>', body, re.S)
    bad = []
    for i, (cls, s) in enumerate(sections, 1):
        if "divider" in cls or "title" in cls:
            continue
        body_wo_refs = re.sub(r'<sup class="ref">.*?</sup>', "", s)
        html_acc = len(re.findall(r'class="[^"]*\bacc\b[^"]*"', body_wo_refs))
        svg_acc = 1 if ACCENT.lower() in s.lower() else 0
        total = html_acc + svg_acc
        label = re.search(r'<span>([^<]*)</span>', s)
        name = label.group(1) if label else "?"
        if total != 1:
            bad.append((i, name, total, html_acc, svg_acc))
    if not bad:
        print("  every content slide carries exactly one accent region ✓")
        return 0
    print(f"  {len(bad)} slide(s) off the one-accent rule:")
    for i, name, tot, hh, sv in bad:
        print(f"    slide {i:02d}  {tot} accents  (html {hh}, chart {sv})   {name}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
