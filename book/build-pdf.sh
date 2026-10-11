#!/usr/bin/env bash
# Build the print/publishing PDF of A Hacker's Guide to Survive from the canonical HTML.
# Strips all web chrome (part-nav, backlinks, chapter nav, footer, the web hub), adds
# book front matter (title / copyright / contents), and renders at 6x9" trim with headless Chromium.
# Output (gitignored): book/docx/A-Hackers-Guide-to-Survive-PUBLISH.pdf
set -euo pipefail
export LANG=C.UTF-8 LC_ALL=C.UTF-8
BOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
mkdir -p "${BOOK_DIR}/print" "${BOOK_DIR}/docx"

BOOK_DIR="${BOOK_DIR}" python3 - <<'PY'
import re, os, pathlib
BASE = pathlib.Path(os.environ["BOOK_DIR"])
chapters = ["ch01-the-word-and-the-fire","ch02-the-people","ch03-the-tribes",
    "ch04-the-gatherings","ch05-the-machine-you-own","ch06-compendium-of-attacks",
    "ch07-the-field-manual","ch08-the-machines-that-hack","ch09-the-law-and-the-line",
    "ch10-the-news-and-the-reckoning","appendices"]
styles=[]; sections=[]; toc=[]
for item in chapters:
    html=(BASE/item/"index.html").read_text(encoding="utf-8")
    for m in re.finditer(r"<style>(.*?)</style>", html, re.S): styles.append(m.group(1))
    main=re.search(r"<main>(.*?)</main>", html, re.S).group(1)
    main=re.sub(r'<p class="backlink">.*?</p>','',main,flags=re.S)
    main=re.sub(r'<nav class="partnav[^"]*">.*?</nav>','',main,flags=re.S)
    main=re.sub(r'<nav class="chapnav">.*?</nav>','',main,flags=re.S)
    main=main.replace('src="assets/', 'src="file://'+str(BASE)+'/'+item+'/assets/')
    sections.append('<section class="chapter">\n'+main+'\n</section>')
    k=re.search(r'<p class="kicker">(.*?)</p>',html); t=re.search(r'<h1>(.*?)</h1>',html)
    toc.append((re.sub('<[^>]+>','',k.group(1)) if k else '', re.sub('<[^>]+>','',t.group(1)) if t else item))
title='''<section class="frontpage titlepage"><div class="tp-kicker">SAVVY SECURITY LLC &middot; A LIVING COMPENDIUM</div>
<h1 class="tp-title">A Hacker&rsquo;s Guide to Survive</h1>
<div class="tp-sub">The history, the people, the tribes, the lab you own, the compendium of attacks, the field manual, the machines that hack, the law, and the reckoning &mdash; for the person walking in cold, and for the veteran who stayed.</div>
<div class="tp-author">Malcolm R. Smith</div><div class="tp-ed">Edition One &middot; 2026</div></section>'''
copyr='''<section class="frontpage copypage"><p><strong>A Hacker&rsquo;s Guide to Survive</strong> &mdash; Edition One (2026).</p>
<p>Copyright &copy; 2026 Malcolm R. Smith / Savvy Security LLC. All rights reserved. No part of this book may be reproduced without permission, except brief quotations in reviews and scholarship.</p>
<p>This is a <em>living compendium</em>, revised and republished once a year. Every quotation is attributed to its source, and every factual claim is traceable to the sources listed at the end of each chapter. All cover art and diagrams are original vector work by Savvy Security LLC.</p>
<p><strong>Nothing in this book is legal advice.</strong> Chapter 9 explains the law for defenders and authorized testers; consult a qualified attorney in your jurisdiction before acting. Every technique in this book is documented for defense and for testing you are explicitly authorized to perform.</p>
<p class="imprint">Savvy Security LLC &middot; First printing, 2026</p></section>'''
toc_items="\n".join(f'<li><span class="toc-ch">{k}</span><span class="toc-ti">{t}</span></li>' for k,t in toc)
toc_page=f'<section class="frontpage tocpage"><h2 class="toc-h">Contents</h2><ol class="toc">{toc_items}</ol></section>'
pub_css='''
@page { size: 6in 9in; margin: 16mm 15mm 18mm; }
:root{color-scheme:light}
html,body{background:#fff!important;color:#1a1712;font-family:Georgia,'Times New Roman',serif!important;font-size:10.6pt;line-height:1.5}
.mono,code,pre,.kicker,.byline,dl.fm dt,.panel,.att,.cvss,.rr,.refs-group,.law .cite,.verdict,table.jobs th,table.cal th,.recipe pre,h4,.framing h3,.danger .tag,.lessons h3,.dos h3,.donts h3,.stat .big,blockquote cite,figcaption .credit,.incident .meta,.incident .lesson b,.attack .fix b,.secread b,.role,dl.gloss dt,table.cal td.when,.tp-kicker,.tp-ed,.imprint,.toc-ch{font-family:'DejaVu Sans Mono','Liberation Mono',monospace!important}
main{max-width:none;padding:0}
.partnav,.backlink,.chapnav,footer{display:none!important}
.chapter,.frontpage{break-before:page}.titlepage{break-before:avoid}
h1,h2,h3{break-after:avoid}h1{font-size:1.7rem}h2{font-size:1.25rem}h3{font-size:1.02rem}
figure,.panel,.law,.incident,blockquote,.recipe,.dos,.donts,.lessons,.framing,.danger,.note,.stat,.case{break-inside:avoid}
img{max-width:100%}
.titlepage{text-align:center;padding-top:30%}
.tp-kicker{letter-spacing:.14em;font-size:8.5pt;color:#a86a22;text-transform:uppercase;margin-bottom:28px}
.tp-title{font-size:2.5rem;border:none;margin:0 0 18px;line-height:1.1}
.tp-sub{font-style:italic;color:#5d5545;font-size:11pt;max-width:4in;margin:0 auto 60px;line-height:1.5}
.tp-author{font-size:14pt;font-weight:700;margin-bottom:6px}
.tp-ed{font-size:9pt;letter-spacing:.1em;color:#5d5545;text-transform:uppercase}
.copypage{font-size:9.5pt;color:#3a362e;padding-top:18%}.copypage p{margin-bottom:12px}.imprint{font-size:8pt;color:#8a8275;margin-top:30px}
.tocpage .toc-h{border:none;font-size:1.8rem;margin-bottom:18px}
ol.toc{list-style:none;padding:0}ol.toc li{display:flex;flex-direction:column;gap:2px;padding:9px 0;border-bottom:1px solid #ddd6c4}
.toc-ch{font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:#a86a22}.toc-ti{font-size:12.5pt;font-weight:700}
'''
doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><style>'+''.join(styles)+'</style><style>'+pub_css+'</style></head><body><main>'+title+copyr+toc_page+''.join(sections)+'</main></body></html>'
(BASE/"print"/"publish.html").write_text(doc,encoding="utf-8")
print("publish.html built:",len(doc),"bytes")
PY

echo "rendering PDF with Chromium..."
"${CHROME}" --headless --disable-gpu --no-sandbox --hide-scrollbars --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw --virtual-time-budget=40000 \
  --print-to-pdf="${BOOK_DIR}/docx/A-Hackers-Guide-to-Survive-PUBLISH.pdf" \
  "file://${BOOK_DIR}/print/publish.html" 2>/dev/null
echo "done -> ${BOOK_DIR}/docx/A-Hackers-Guide-to-Survive-PUBLISH.pdf"
