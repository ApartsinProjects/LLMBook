"""Root-cause fixes for v15.5 — multiple Kindle rendering issues.

This script makes book-wide source edits to address user-reported issues:

1. Bibliography double header: every <section class="bibliography"> has BOTH
   <h3>Bibliography and Further Reading</h3>
   <div class="bibliography-title">References & Further Reading</div>
   The div is a stylistic ghost of an older theme; drop it so the section
   has a single semantic heading.

2. About Authors page: source uses inline <style> with display:flex which
   reflows badly on narrow Kindle viewports (huge empty column). Replace
   the flex container with a block flow that lets the photo+bio stack
   vertically on narrow screens.

3. <img> inline style attributes: KPV E21018 trips on
   <img ... style="max-width: 100%; height: auto;"/>
   in some chapters. Strip the inline style; the .img / figure wrapper
   styles handle responsive sizing.

4. <figure> illustrations with <img> children: ensure responsive without
   relying on inline styles.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = {"KDP", "node_modules", ".git", "pagefind", "scripts", "styles"}


def fix_bibliography_double_header(soup: BeautifulSoup) -> int:
    """Remove the redundant <div class="bibliography-title"> in bibliography sections."""
    n = 0
    for div in soup.find_all("div", class_="bibliography-title"):
        div.decompose()
        n += 1
    return n


def fix_img_inline_style(soup: BeautifulSoup) -> int:
    """Strip the inline style="max-width:..." from <img> tags. KPV E21018
    flags some imgs with this attribute. Responsive sizing is handled by
    figure/img CSS in epub_overrides.css."""
    n = 0
    target_styles = (
        "max-width: 100%; height: auto;",
        "max-width:100%; height:auto;",
        "max-width: 100%;height:auto;",
        "max-width:100%;height:auto;",
    )
    for img in soup.find_all("img"):
        style = img.get("style", "").strip()
        if not style:
            continue
        # Normalize whitespace for comparison
        norm = re.sub(r"\s+", " ", style)
        if norm in target_styles or "max-width" in style:
            del img.attrs["style"]
            n += 1
    return n


def fix_about_authors_flex(html: str, p: Path) -> str:
    """In front-matter/about-authors.html, replace the inline <style>'s
    display:flex with block flow + auto-wrapping. The CSS is in an inline
    <style> in this single file; we rewrite the block so the photo sits
    above the bio on narrow viewports."""
    if p.name != "about-authors.html":
        return html
    # Replace display: flex; with display: block; (the gap and other flex
    # properties become harmless on block)
    # Also reset the photo to inline-block float so it sits above text but
    # text wraps if there's room.
    new = re.sub(
        r"\.author-card\s*\{\s*display:\s*flex;",
        ".author-card { display: block;",
        html,
    )
    # Adjust the photo to be a centered block (was flex-shrink)
    new = re.sub(
        r"\.author-photo\s*\{\s*flex-shrink:\s*0;\s*",
        ".author-photo { display: block; margin: 0 auto 1.2rem auto; ",
        new,
    )
    # Drop the flex:1 rule on .author-info
    new = re.sub(
        r"\.author-info\s*\{\s*flex:\s*1;\s*\}",
        ".author-info { display: block; }",
        new,
    )
    return new


def main():
    apply = "--apply" in sys.argv
    n_bib = 0
    n_img = 0
    files_touched_bib = 0
    files_touched_img = 0
    fixed_about_authors = False

    for p in ROOT.rglob("*.html"):
        if any(part in SKIP for part in p.parts):
            continue
        text = p.read_text(encoding="utf-8")

        # About Authors flex fix (textual)
        if p.name == "about-authors.html":
            new_text = fix_about_authors_flex(text, p)
            if new_text != text:
                fixed_about_authors = True
                if apply:
                    p.write_text(new_text, encoding="utf-8")
                text = new_text

        # Bibliography + img fixes (soup-based)
        if (
            'class="bibliography-title"' in text
            or ('<img' in text and 'style=' in text)
        ):
            soup = BeautifulSoup(text, "html.parser")
            bib_count = fix_bibliography_double_header(soup)
            img_count = fix_img_inline_style(soup)
            if bib_count or img_count:
                if bib_count:
                    n_bib += bib_count
                    files_touched_bib += 1
                if img_count:
                    n_img += img_count
                    files_touched_img += 1
                if apply:
                    p.write_text(str(soup), encoding="utf-8")

    print(f"Bibliography double-header divs removed: {n_bib} in {files_touched_bib} files")
    print(f"<img> inline 'style' attrs stripped:     {n_img} in {files_touched_img} files")
    print(f"About Authors flex layout fixed:         {fixed_about_authors}")
    print()
    print("APPLIED" if apply else "DRY RUN (--apply to write)")


if __name__ == "__main__":
    main()
