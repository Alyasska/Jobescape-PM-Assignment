#!/usr/bin/env python3
"""Merge a set of markdown / text / code files into ONE styled PDF with a contents page.

The reviewer gets a folder over Telegram and wants documents, not a repository. Markdown, .txt
and .py files are not things a person opens — so every deliverable is bundled into a small number
of PDFs, each self-contained and each opening in any viewer.

    python3 build_bundle.py <out.pdf> "<Title>" <spec.json>

spec.json: [{"file": "...", "title": "...", "kind": "md|text|code"}, ...]
"""
import html as htmllib
import json
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
.cover{ height:250mm; display:flex; flex-direction:column; justify-content:space-between;
        page-break-after:always }
.cover .top{ margin-top:70mm }
.cover .eyebrow{ font-family:var(--mono); letter-spacing:.16em; text-transform:uppercase;
                 font-size:8.4pt; color:var(--accent) }
.cover h1{ font-family:var(--display); font-size:34pt; line-height:1.05; letter-spacing:-.028em;
           font-weight:600; margin:.4em 0 .3em }
.cover h1::before{ content:""; display:block; width:46px; height:3px; background:var(--accent);
                   margin-bottom:16px }
.cover .sub{ font-size:12pt; color:var(--muted); max-width:32em; line-height:1.5 }
.cover .meta{ font-family:var(--mono); font-size:8.4pt; color:var(--soft);
              border-top:1.5px solid var(--fg); padding-top:11px }
.toc{ page-break-after:always }
.toc h2{ border:0; margin-top:0 }
.toc ol{ list-style:none; padding:0; margin:0; counter-reset:t }
.toc li{ counter-increment:t; font-family:var(--display); font-size:12pt; font-weight:600;
         padding:9px 0; border-bottom:1px solid var(--rule) }
.toc li::before{ content:counter(t,decimal-leading-zero); font-family:var(--mono);
                 font-size:8.6pt; color:var(--accent); margin-right:14px; font-weight:500 }
.doc{ page-break-before:always }
h1{ font-family:var(--display); font-size:22pt; font-weight:600; letter-spacing:-.022em;
    line-height:1.1; margin:0 0 6px }
h1::before{ content:""; display:block; width:46px; height:3px; background:var(--accent);
            margin-bottom:14px }
h2{ font-family:var(--display); font-size:13.4pt; font-weight:600; letter-spacing:-.012em;
    margin:24px 0 8px; padding-bottom:6px; border-bottom:1px solid var(--rule);
    break-after:avoid }
h3{ font-size:10.4pt; font-weight:600; margin:16px 0 5px }
h4{ font-family:var(--mono); font-size:8.4pt; font-weight:500; letter-spacing:.08em;
    text-transform:uppercase; color:var(--soft); margin:15px 0 5px }
p{ margin:0 0 8px; max-width:44em }
a{ color:var(--accent); text-decoration:none }
ul,ol{ margin:8px 0 12px; padding-left:19px; max-width:44em }
li{ margin:4px 0 } li::marker{ color:var(--soft) }
code{ font-family:var(--mono); font-size:8.6pt; background:var(--fill); padding:1px 4px;
      border-radius:2px }
blockquote{ margin:13px 0; padding:11px 16px; background:var(--fill);
            border-left:2.5px solid var(--accent); break-inside:avoid }
blockquote p{ margin:3px 0 }
table{ border-collapse:collapse; width:100%; margin:12px 0 16px; font-size:8.4pt; }
th{ font-family:var(--mono); font-size:7.4pt; font-weight:500; letter-spacing:.07em;
    text-transform:uppercase; color:var(--soft); text-align:left;
    border-bottom:1.4px solid var(--fg); padding:0 9px 6px 0 }
td{ border:0; border-bottom:1px solid var(--rule); padding:7px 9px 7px 0; vertical-align:top;
    line-height:1.45 }
td:last-child, th:last-child{ padding-right:0 }
tbody tr:last-child td{ border-bottom:1.4px solid var(--fg) }
hr{ border:0; border-top:1px solid var(--rule); margin:18px 0 }
pre{ background:var(--fill); border-left:2.5px solid var(--accent); padding:11px 14px;
     font-family:var(--mono); font-size:7.4pt; line-height:1.45; white-space:pre-wrap;
     word-break:break-word; margin:10px 0 }


/* A table taller than a page cannot honour break-inside:avoid — Chrome pushes it past the
   page edge instead. So let tall tables break, repeat the header on each page, and keep
   individual rows whole. */
table { break-inside:auto; page-break-inside:auto }
thead { display:table-header-group }
tr { break-inside:avoid; page-break-inside:avoid }
td code, th code { font-size:7.1pt; word-break:keep-all; overflow-wrap:normal }
"""


def render(spec_item):
    p = pathlib.Path(spec_item["file"])
    raw = p.read_text(errors="ignore")
    kind = spec_item.get("kind", "md")
    if kind == "md":
        # cross-file links mean nothing in a bundle; keep the words, drop the href
        raw = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"\1", raw)
        # the first H1 is replaced by our own section title
        raw = re.sub(r"\A#\s+.*\n", "", raw)
        body = markdown.markdown(raw, extensions=["tables", "sane_lists", "fenced_code"])
    else:
        body = f"<pre>{htmllib.escape(raw)}</pre>"
    return (f'<div class="doc"><h1>{htmllib.escape(spec_item["title"])}</h1>'
            f'{"<p><em>" + htmllib.escape(spec_item["note"]) + "</em></p>" if spec_item.get("note") else ""}'
            f"{body}</div>")


def main(out, title, sub, spec_path):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    toc = "".join(f"<li>{htmllib.escape(s['title'])}</li>" for s in spec)
    docs = "".join(render(s) for s in spec)
    html = f"""<!doctype html><meta charset="utf-8"><title>{htmllib.escape(title)}</title>
<style>{FONTS}\n{CSS}</style>
<div class="cover"><div class="top">
  <div class="eyebrow">Product Manager Take-Home &middot; Nomad Venture Studio / Jobescape</div>
  <h1>{htmllib.escape(title)}</h1><div class="sub">{htmllib.escape(sub)}</div></div>
  <div class="meta">Aliaskar Bekishev &nbsp;&middot;&nbsp; 2026-07-28</div></div>
<div class="toc"><h2>Contents</h2><ol>{toc}</ol></div>{docs}"""
    out = str(pathlib.Path(out).resolve())
    tmp = pathlib.Path(out).with_suffix(".build.html")
    tmp.write_text(html)
    r = subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}",
                        "--virtual-time-budget=15000", f"file://{tmp.resolve()}"],
                       capture_output=True, timeout=240)
    tmp.unlink()
    size = pathlib.Path(out).stat().st_size
    pages = max(int(m.group(1)) for m in re.finditer(rb"/Count (\d+)",
                                                     pathlib.Path(out).read_bytes()))
    print(f"  {pathlib.Path(out).name:<52} {pages:>3} pages  {size/1048576:.2f} MB "
          f"(exit {r.returncode})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
