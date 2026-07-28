#!/usr/bin/env python3
"""Render the submission entry document to PDF, styled like the dossier.

The reviewer receives a folder over Telegram. Markdown is the wrong format to *lead* with — it
renders as raw asterisks in a plain text viewer — so the entry document ships as both: the .md
keeps the working links between files, the .pdf opens anywhere.

    python3 build_submission_pdf.py <submission.md> <out.pdf>
"""
import pathlib
import re
import subprocess
import sys

import markdown

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "presentation"))
try:
    from deck_assets import font_face_css
    FONTS = font_face_css()
except Exception:
    FONTS = ""

CSS = """
@page { size: A4; margin: 17mm 16mm 18mm; }
* { box-sizing:border-box }
:root{ --bg:#FCFBF8; --fg:#14120F; --muted:#605B52; --soft:#8A8478;
       --accent:#C2461F; --rule:#DED9CF; --fill:#F2EEE5;
       --sans:'Inter',system-ui,sans-serif; --mono:'IBM Plex Mono',ui-monospace,monospace;
       --display:'Inter Tight','Inter',sans-serif; }
body{ font-family:var(--sans); color:var(--fg); background:var(--bg);
      font-size:9.8pt; line-height:1.55; margin:0 }
h1{ font-family:var(--display); font-size:25pt; font-weight:600; letter-spacing:-.025em;
    line-height:1.08; margin:0 0 6px }
h1::before{ content:""; display:block; width:46px; height:3px; background:var(--accent);
            margin-bottom:14px }
h1 + p em, h1 + em { color:var(--muted) }
h2{ font-family:var(--display); font-size:14pt; font-weight:600; letter-spacing:-.012em;
    margin:24px 0 8px; padding-bottom:6px; border-bottom:1px solid var(--rule);
    break-after:avoid }
h3{ font-size:10.4pt; font-weight:600; margin:16px 0 5px }
p{ margin:0 0 8px; max-width:44em }
p > strong:first-child{ font-weight:600 }
a{ color:var(--accent); text-decoration:none; border-bottom:1px solid var(--rule) }
ul,ol{ margin:8px 0 12px; padding-left:19px; max-width:44em }
li{ margin:4px 0 } li::marker{ color:var(--soft) }
code{ font-family:var(--mono); font-size:8.6pt; background:var(--fill); padding:1px 4px;
      border-radius:2px }
blockquote{ margin:14px 0; padding:11px 16px; background:var(--fill);
            border-left:2.5px solid var(--accent); break-inside:avoid }
blockquote p{ margin:3px 0 }
table{ border-collapse:collapse; width:100%; margin:12px 0 16px; font-size:8.5pt }
th{ font-family:var(--mono); font-size:7.4pt; font-weight:500; letter-spacing:.07em;
    text-transform:uppercase; color:var(--soft); text-align:left;
    border-bottom:1.4px solid var(--fg); padding:0 9px 6px 0 }
td{ border:0; border-bottom:1px solid var(--rule); padding:7px 9px 7px 0; vertical-align:top;
    line-height:1.45 }
td:first-child{ white-space:nowrap; font-weight:600 }
td:last-child, th:last-child{ padding-right:0 }
tbody tr:last-child td{ border-bottom:1.4px solid var(--fg) }
hr{ border:0; border-top:1px solid var(--rule); margin:18px 0 }


/* A table taller than a page cannot honour break-inside:avoid — Chrome pushes it past the
   page edge instead. So let tall tables break, repeat the header on each page, and keep
   individual rows whole. */
table { break-inside:auto; page-break-inside:auto }
thead { display:table-header-group }
tr { break-inside:avoid; page-break-inside:avoid }
td code, th code { font-size:7.1pt; word-break:keep-all; overflow-wrap:normal }
"""


def main(src, out):
    md = pathlib.Path(src).read_text()
    # links between files in the folder are meaningless in a PDF — keep the label, drop the href
    md = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"\1", md)
    body = markdown.markdown(md, extensions=["tables", "sane_lists", "fenced_code"])
    html = (f'<!doctype html><meta charset="utf-8"><title>PM Test Assignment — Aliaskar Bekishev'
            f'</title><style>{FONTS}\n{CSS}</style>'
            f''
            f"{body}")
    out = str(pathlib.Path(out).resolve())          # Chrome needs an absolute file:// path
    tmp = pathlib.Path(out).with_suffix(".html")
    tmp.write_text(html)
    r = subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        "--virtual-time-budget=12000", f"file://{tmp.resolve()}"],
                       capture_output=True, timeout=180)
    tmp.unlink()
    print(f"  {out} ({pathlib.Path(out).stat().st_size/1024:.0f} KB, chrome exit {r.returncode})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
