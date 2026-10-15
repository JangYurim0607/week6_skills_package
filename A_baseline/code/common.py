import os
from playwright.sync_api import sync_playwright

BASE = '/home/claude/week6_skills_package'
DATA = f'{BASE}/data'
OUT = f'{BASE}/A_baseline/output'
WORK = f'{BASE}/A_baseline/code/_work'
os.makedirs(WORK, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

BASE_CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; font-family: 'Noto Sans CJK JP', sans-serif; color:#1f2430; font-size:10pt; line-height:1.5; word-break: keep-all; overflow-wrap: anywhere; }
"""

def html_to_pdf(html, pdf_path, name):
    p = f'{WORK}/{name}.html'
    open(p, 'w', encoding='utf-8').write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto('file://' + p)
        pg.wait_for_timeout(300)
        pg.pdf(path=pdf_path, format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
