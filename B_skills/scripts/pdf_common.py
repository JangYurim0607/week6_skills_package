"""HTML -> PDF 공통 도구 (Playwright Chromium). 폰트는 Noto Sans CJK JP."""
from pathlib import Path

BASE_CSS = """
@page { size: A4; margin: 12mm 12mm 13mm 12mm; }
:root { --ink:#1f2937; --mute:#6b7280; --rule:#e5e7eb; --soft:#f3f4f6; --accent:#2563eb; --warn:#b45309; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Noto Sans CJK JP','Noto Sans CJK KR',sans-serif; color: var(--ink); font-size: 9.4pt; line-height: 1.55; margin: 0; word-break: keep-all; overflow-wrap: break-word; }
h1 { font-size: 20pt; line-height: 1.25; margin: 0 0 4pt; letter-spacing: -0.01em; }
h2 { font-size: 13pt; margin: 14pt 0 5pt; padding-bottom: 3pt; border-bottom: 1.5pt solid var(--accent); }
h3 { font-size: 10.5pt; margin: 10pt 0 3pt; }
p { margin: 3pt 0 5pt; }
ul { margin: 2pt 0 5pt; padding-left: 14pt; } li { margin: 1.5pt 0; }
.page { page-break-after: always; break-after: page; }
.page:last-child { page-break-after: auto; break-after: auto; }
.mute { color: var(--mute); } .small { font-size: 8pt; } .tiny { font-size: 7.4pt; }
table { border-collapse: collapse; width: 100%; }
th, td { border-bottom: .6pt solid var(--rule); padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: var(--soft); font-size: 8.2pt; font-weight: 700; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
.pill { display:inline-block; padding: 0 5pt; border-radius: 8pt; font-size: 7.6pt; background: var(--soft); color: var(--ink); }
.pill.warn { background:#fef3c7; color:#92400e; }
.box { border: .8pt solid var(--rule); border-radius: 4pt; padding: 6pt 8pt; background: #fff; }
.box.accent { border-color: var(--accent); background: #f5f8ff; }
.box.warn { border-color:#f59e0b; background:#fffbeb; }
.note { font-size: 8pt; color: var(--mute); }
img { max-width: 100%; }
"""


def render_pdf(html_text: str, out_pdf: str, extra_wait_ms: int = 300):
    from playwright.sync_api import sync_playwright
    hd = Path(out_pdf).parent / "artifacts" / "html"
    hd.mkdir(parents=True, exist_ok=True)
    tmp = hd / (Path(out_pdf).stem + ".html")
    tmp.write_text(html_text, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(f"file://{tmp}")
        pg.wait_for_timeout(extra_wait_ms)
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    return tmp
