"""Reproduce EPUB rendering of specific pages in headless Chromium.

Wraps a source page's <body> with the SAME stylesheets the EPUB bundles
(book.css then epub_overrides.css, in that order) and screenshots a target
element, so we can see how a chapter heading / table renders in a
Blink/WebKit reader (Thorium, Apple Books, Kindle's web view) and test CSS
fixes without a full EPUB rebuild.
"""
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BOOK_CSS = (ROOT / "styles/book.css").read_text(encoding="utf-8", errors="replace")
OVR_CSS = (ROOT / "KDP/build/epub_overrides.css").read_text(encoding="utf-8", errors="replace")
OUT = Path("C:/Users/apart/AppData/Local/Temp")


def body_of(p: Path) -> str:
    t = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<body[^>]*>(.*?)</body>", t, re.S)
    return m.group(1) if m else t


def page_html(body: str) -> str:
    # Inline both stylesheets (book.css then epub_overrides.css, the EPUB order)
    # so they actually apply in set_content (external file:// links don't load).
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<style>{BOOK_CSS}</style><style>{OVR_CSS}</style>'
            f'</head><body>{body}</body></html>')


def main():
    jobs = [
        ("h1", ROOT / "part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html",
         ".chapter-header"),
        ("table", ROOT / "part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html",
         None),  # locate the comparison table dynamically
    ]
    with sync_playwright() as p:
        br = p.chromium.launch()
        for name, src, sel in jobs:
            pg = br.new_page(viewport={"width": 700, "height": 1000}, device_scale_factor=2)
            pg.set_content(page_html(body_of(src)), wait_until="networkidle")
            if name == "table":
                el = pg.query_selector("table")
            else:
                el = pg.query_selector(sel)
            if el is None:
                print(f"  {name}: target not found"); pg.close(); continue
            el.scroll_into_view_if_needed()
            shot = OUT / f"diag-{name}.png"
            try:
                el.screenshot(path=str(shot))
            except Exception:
                pg.screenshot(path=str(shot))
            # report computed text-align of the h1 / display of th
            if name == "h1":
                ta = pg.eval_on_selector(".chapter-header h1", "e => getComputedStyle(e).textAlign")
                print(f"  h1 computed text-align: {ta}")
            else:
                disp = pg.eval_on_selector("table th", "e => getComputedStyle(e).display")
                tdisp = pg.eval_on_selector("table", "e => getComputedStyle(e).display")
                bg = pg.eval_on_selector("table th", "e => getComputedStyle(e).backgroundColor")
                print(f"  table display: {tdisp} | th display: {disp} | th bg: {bg}")
            print(f"  wrote {shot}")
            pg.close()
        br.close()


if __name__ == "__main__":
    main()
