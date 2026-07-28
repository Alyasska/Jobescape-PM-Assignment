#!/usr/bin/env python3
"""Assemble the Jobescape research report: markdown sections -> styled HTML -> (chrome) PDF."""
import markdown, pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "presentation"))
try:                                    # reuse the deck's embedded typefaces so the two
    from deck_assets import font_face_css   # documents read as one system
    FONTS = font_face_css()
except Exception as e:                  # the dossier must still build without them
    print(f"  (fonts unavailable, falling back to system faces: {e})", file=sys.stderr)
    FONTS = ""

HERE = pathlib.Path(__file__).parent
SEC = HERE / "sections"

# Order of the report. Files that don't exist yet are skipped (with a warning), so the
# report can be built incrementally as deep-research sections land.
ORDER = [
    "01-exec.md",
    "02-method.md",
    "03-partA-audience.md",
    "04-partB-competitors.md",
    "05-partC-challenge.md",
    "06-partD-economics.md",
    "07-economics-thesis.md",
    "08-appendix.md",
]

CSS = """
@page { size: A4; margin: 19mm 18mm 20mm; }
* { box-sizing: border-box; }
:root {
  --bg:#FCFBF8; --fg:#14120F; --muted:#605B52; --soft:#8A8478;
  --accent:#C2461F; --rule:#DED9CF; --fill:#F2EEE5;
  --sans:'Inter',system-ui,sans-serif; --mono:'IBM Plex Mono',ui-monospace,monospace;
  --display:'Inter Tight','Inter',sans-serif;
}
body { font-family:var(--sans); color:var(--fg); background:var(--bg);
       font-size:10.2pt; line-height:1.62; margin:0; -webkit-font-smoothing:antialiased; }

/* ── cover ─────────────────────────────────────────── */
.cover { height:252mm; display:flex; flex-direction:column; justify-content:space-between;
         page-break-after:always; }
.cover .top { margin-top:62mm; }
.cover .eyebrow { font-family:var(--mono); letter-spacing:.16em; text-transform:uppercase;
                  font-size:8.4pt; color:var(--accent); font-weight:500; }
.cover h1 { font-family:var(--display); font-size:33pt; line-height:1.06; letter-spacing:-.025em;
            color:var(--fg); margin:.42em 0 .34em; font-weight:600; }
.cover .sub { font-size:12.5pt; color:var(--muted); max-width:34em; line-height:1.5; }
.cover .meta { font-family:var(--mono); font-size:8.6pt; line-height:1.75; color:var(--soft);
               border-top:1.5px solid var(--fg); padding-top:11px; }
.cover .meta strong { color:var(--fg); font-weight:500; }

/* ── section openers: the main flip-through anchor ── */
section { page-break-before:always; }
section:first-of-type { page-break-before:avoid; }
h1 { font-family:var(--display); font-size:23pt; font-weight:600; letter-spacing:-.022em;
     line-height:1.12; margin:0 0 4px; padding-bottom:0; border:0; }
h1::before { content:""; display:block; width:46px; height:3px; background:var(--accent);
             margin-bottom:14px; }
/* a blockquote straight after H1 is the section takeaway — the thing a skimmer reads */
h1 + blockquote { margin:14px 0 20px; padding:13px 0 13px 18px; background:none;
                  border:0; border-left:2.5px solid var(--accent); }
h1 + blockquote p { font-family:var(--display); font-size:13pt; line-height:1.42;
                    font-weight:500; color:var(--fg); margin:0; }

h2 { font-family:var(--display); font-size:13.6pt; font-weight:600; letter-spacing:-.012em;
     margin:26px 0 8px; padding-bottom:6px; border-bottom:1px solid var(--rule); }
h3 { font-family:var(--sans); font-size:10.6pt; font-weight:600; margin:18px 0 5px;
     color:var(--fg); }
h4 { font-family:var(--mono); font-size:8.6pt; font-weight:500; letter-spacing:.08em;
     text-transform:uppercase; color:var(--soft); margin:16px 0 5px; }

p { margin:0 0 9px; max-width:40em; }
/* run-in heads carry the scan, so give them their own weight and colour */
p > strong:first-child { color:var(--fg); font-weight:600; }
strong { font-weight:600; }
em { color:var(--muted); }
a { color:var(--accent); text-decoration:none; border-bottom:1px solid var(--rule); }
ul,ol { margin:8px 0 12px; padding-left:19px; max-width:40em; }
li { margin:4px 0; }
li::marker { color:var(--soft); }

code { font-family:var(--mono); font-size:8.8pt; background:var(--fill);
       padding:1px 4px; border-radius:2px; }
pre { background:var(--fill); border:0; border-left:2.5px solid var(--accent);
      padding:12px 15px; font-size:8.5pt; line-height:1.5; overflow-x:auto;
      break-inside:avoid; }
pre code { background:none; padding:0; }

/* ── quotes elsewhere in a section ─────────────────── */
blockquote { margin:14px 0; padding:11px 16px; background:var(--fill);
             border-left:2.5px solid var(--accent); break-inside:avoid; }
blockquote p { margin:3px 0; color:var(--fg); }

/* ── tables: rules, not boxes ──────────────────────── */
table { border-collapse:collapse; width:100%; margin:13px 0 16px; font-size:8.9pt; }
th { font-family:var(--mono); font-size:7.6pt; font-weight:500; letter-spacing:.07em;
     text-transform:uppercase; color:var(--soft); text-align:left;
     border-bottom:1.4px solid var(--fg); padding:0 10px 6px 0; }
td { border:0; border-bottom:1px solid var(--rule); padding:7px 10px 7px 0;
     vertical-align:top; line-height:1.45; }
td:last-child, th:last-child { padding-right:0; }
tbody tr:last-child td { border-bottom:1.4px solid var(--fg); }
td strong { color:var(--fg); }
/* figures read as figures */
td:not(:first-child) { font-variant-numeric:tabular-nums; }

hr { border:0; border-top:1px solid var(--rule); margin:20px 0; }
small { color:var(--soft); font-size:8.6pt; }

/* ── contents ──────────────────────────────────────── */
.toc { page-break-after:always; }
.toc ul { list-style:none; padding-left:0; margin:0; }
.toc > ul > li { margin:13px 0 0; font-weight:600; font-size:11pt;
                 font-family:var(--display); letter-spacing:-.01em; }
.toc ul ul { padding-left:0; margin:5px 0 0; }
.toc ul ul li { font-family:var(--sans); font-weight:400; font-size:9.3pt;
                color:var(--muted); margin:3px 0; padding-left:16px;
                border-left:1px solid var(--rule); }

.tag { display:inline-block; font-family:var(--mono); font-size:7.2pt; font-weight:500;
       letter-spacing:.06em; text-transform:uppercase; padding:1.5px 6px; border-radius:2px;
       vertical-align:middle; }
.tag-fact { background:#E6EFE6; color:#2C6B3C; }
.tag-inf  { background:#FAEEDC; color:#8A5A12; }
.tag-blk  { background:#F7E2DA; color:var(--accent); }

/* running footer, repeated on every printed page */


/* A table taller than a page cannot honour break-inside:avoid — Chrome pushes it past the
   page edge instead. So let tall tables break, repeat the header on each page, and keep
   individual rows whole. */
table { break-inside:auto; page-break-inside:auto }
thead { display:table-header-group }
tr { break-inside:avoid; page-break-inside:avoid }
td code, th code { font-size:7.1pt; word-break:keep-all; overflow-wrap:normal }
"""

COVER = """
<div class="cover">
  <div class="top">
    <div class="eyebrow">Product Manager Take-Home &middot; Nomad Venture Studio / Jobescape</div>
    <h1>Jobescape: Audience, Competitors,<br>the Challenge &amp; the Economics</h1>
    <div class="sub">A research dossier &mdash; the evidence, the thesis, and the plan behind Parts A&ndash;D.</div>
  </div>
  <div class="meta">
    Prepared by <strong>Aliaskar Bekishev</strong> &nbsp;&middot;&nbsp; 2026-07-28 &nbsp;&middot;&nbsp;
    Built with a team of AI research agents (on-brand: Jobescape teaches working <em>with</em> AI)<br>
    <small>Three-step method: broad research (scientific &middot; social &middot; market) &rarr; synthesis &rarr; deep-dive. Every external claim carries a source; internal-data gaps are flagged, not faked.</small>
  </div>
</div>
"""

def build():
    parts = [COVER, '<div class="toc">\n', markdown.markdown("# Contents\n\n[TOC]", extensions=["toc"]), "</div>\n"]
    # Real TOC is generated per-section below; simpler: build one big doc with toc.
    body_md = []
    for name in ORDER:
        f = SEC / name
        if not f.exists():
            print(f"  (skip, not yet written: {name})", file=sys.stderr); continue
        body_md.append(f.read_text())
    full_md = "\n\n".join(body_md)
    md = markdown.Markdown(extensions=["tables","fenced_code","sane_lists","toc","attr_list"])
    body_html = md.convert(full_md)
    toc_html = md.toc  # generated from headings
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Jobescape Research Dossier</title><style>{FONTS}\n{CSS}</style></head><body>\n{COVER}
<div class="toc"><h1>Contents</h1>{toc_html}</div>
{body_html}
</body></html>"""
    out = HERE / "report.html"
    out.write_text(html)
    print(f"wrote {out} ({len(html)} bytes)")
    return out

def to_pdf(html_path):
    pdf = HERE / "Jobescape-Research-Dossier.pdf"
    cmd = ["google-chrome","--headless=new","--disable-gpu","--no-sandbox",
           "--no-pdf-header-footer", f"--print-to-pdf={pdf}", str(html_path)]
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    print("pdf exit", r.returncode, "->", pdf if pdf.exists() else "FAILED")
    return pdf

if __name__ == "__main__":
    h = build()
    if "--pdf" in sys.argv:
        to_pdf(h)
