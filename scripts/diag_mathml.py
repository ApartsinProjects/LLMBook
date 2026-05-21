"""Diagnose MathML rendering: render a built EPUB chapter in headless Chromium
(same engine as Thorium/Readium) as-is, and again with the MathML
`display:inline !important` overrides neutralized, then screenshot the
cross-entropy equation region for visual comparison.
"""
import re
import sys
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
EPUB = ROOT / "KDP/output/building-conversational-ai-llms-agents.epub"
TMP = Path("C:/Users/apart/AppData/Local/Temp/mathml_diag")


def extract():
    if TMP.exists():
        import shutil
        shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(EPUB) as z:
        z.extractall(TMP)
    return TMP


def main():
    base = extract()
    chap = next(base.glob("EPUB/chapters/*module-00*section-0-1*.xhtml"))
    css = base / "EPUB/styles/epub_overrides.css"
    print("chapter:", chap.name)

    with sync_playwright() as p:
        br = p.chromium.launch()
        for variant in ("asis", "fixed"):
            if variant == "fixed":
                # Neutralize the MathML display:inline overrides so the
                # browser's native MathML layout is used again.
                t = css.read_text(encoding="utf-8")
                # Drop rules that set display:inline on bare MathML elements.
                t2 = re.sub(r'[^{}]*\bmrow\b[^{}]*\{[^}]*display:\s*inline[^}]*\}', '', t)
                t2 = re.sub(r'math\[display=block\][^{}]*\{[^}]*\}', '', t2)
                t2 = re.sub(r'[^{}]*\bmath\b[^{}]*\{[^}]*overflow[^}]*\}', '', t2)
                css.write_text(t2, encoding="utf-8")
            pg = br.new_page(viewport={"width": 760, "height": 1200})
            pg.goto(chap.as_uri())
            shot = Path(f"C:/Users/apart/AppData/Local/Temp/mathml-{variant}.png")
            # screenshot the math-block container that holds the cross-entropy eq
            el = pg.query_selector("div.math-block")
            if el is None:
                el = pg.query_selector("math[display='block']")
            if el:
                el.scroll_into_view_if_needed()
                box = el.bounding_box()
                print(f"  {variant}: container bbox = {box}")
                try:
                    el.screenshot(path=str(shot))
                except Exception as e:
                    print("   element shot failed:", e, "-> full page")
                    pg.screenshot(path=str(shot), full_page=True)
            else:
                print(f"  {variant}: no math container found")
                pg.screenshot(path=str(shot), full_page=True)
            print("  wrote", shot)
            pg.close()
        br.close()


if __name__ == "__main__":
    main()
