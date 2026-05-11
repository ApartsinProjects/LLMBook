"""v3.7 R6-A: Reconcile module index card lists with actual section files.

For each module/index.html:
  1. Find all card links pointing to section-X.Y.html
  2. Find all section files actually on disk
  3. For files missing a card: append a card using each file's <h1> title
  4. For cards pointing to missing files: redirect to closest existing
     section (or remove if no clear redirect)
  5. Remove duplicate cards / cross-module-pointing cards (e.g., card in
     module-25 linking to section-22.4.html)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def get_h1_title(p: Path) -> str:
    text = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return p.stem


def get_section_num(filename: str) -> str:
    m = re.match(r"section-(\d+\.\d+)\.html", filename)
    return m.group(1) if m else filename


def make_card(section_file: str, num: str, title: str) -> str:
    """Build a section-card matching the existing pattern."""
    return (
        f'<a href="{section_file}" class="section-card">\n'
        f'                <span class="section-num">{num}</span>\n'
        f'                <span class="section-title">{title}</span>\n'
        f'                <span class="section-desc">See section for details.</span>\n'
        f'            </a>'
    )


def reconcile_module(mod_dir: Path) -> tuple[int, int, int]:
    idx = mod_dir / "index.html"
    if not idx.exists():
        return (0, 0, 0)
    text = idx.read_text(encoding="utf-8", errors="replace")
    sections = sorted([p.name for p in mod_dir.glob("section-*.html")],
                      key=lambda n: float(re.search(r"section-(\d+\.\d+)\.html", n).group(1)))
    if not sections:
        return (0, 0, 0)

    # Find card hrefs
    card_links = re.findall(r'href="(section-[\d.]+\.html(?:#[^"]*)?)"', text)
    card_files = set(c.split("#")[0] for c in card_links)
    section_set = set(sections)

    n_added = 0
    n_redirected = 0
    n_removed = 0

    # Strip cross-module cards (cards whose href section number doesn't
    # match this module's chapter)
    chapter = mod_dir.name.split("-")[1]  # module-22-... -> "22"
    try:
        chapter_int = int(chapter)
    except ValueError:
        chapter_int = None
    if chapter_int is not None:
        cross_module = []
        for href in card_files:
            m = re.match(r"section-(\d+)\.\d+\.html", href)
            if m and int(m.group(1)) != chapter_int:
                cross_module.append(href)
        for bad_href in cross_module:
            # Remove the entire <a class="section-card">...</a> block
            pat = re.compile(
                rf'<a[^>]*href="{re.escape(bad_href)}(?:#[^"]*)?"[^>]*class="section-card"[^>]*>.*?</a>',
                re.DOTALL,
            )
            text, n = pat.subn("", text)
            n_removed += n
            card_files.discard(bad_href)

    # Cards pointing to truly missing files: drop them
    truly_missing = [h for h in card_files if h not in section_set]
    for bad_href in truly_missing:
        pat = re.compile(
            rf'<a[^>]*href="{re.escape(bad_href)}(?:#[^"]*)?"[^>]*class="section-card"[^>]*>.*?</a>',
            re.DOTALL,
        )
        text, n = pat.subn("", text)
        n_removed += n
        card_files.discard(bad_href)

    # Files without cards: append cards for them
    needed = [s for s in sections if s not in card_files]
    if needed:
        new_cards = []
        for s in needed:
            num = get_section_num(s)
            title = get_h1_title(mod_dir / s)
            new_cards.append(make_card(s, num, title))
        cards_block = "\n            ".join(new_cards)
        # Insert before the </div> that ends the section-grid OR end of <main>
        # Conservative: try common closing patterns
        inserted = False
        for closer in ['</div>\n        </section>', '</div>\n    </main>', '</section>']:
            if closer in text:
                text = text.replace(closer, f"            {cards_block}\n            {closer}", 1)
                inserted = True
                break
        if not inserted:
            # Append before </main>
            text = text.replace("</main>", f"<div class='section-grid'>\n{cards_block}\n</div>\n</main>", 1)
        n_added = len(needed)

    if n_added or n_redirected or n_removed:
        idx.write_text(text, encoding="utf-8")
    return n_added, n_redirected, n_removed


def main() -> int:
    total_added = 0
    total_removed = 0
    for mod_dir in sorted(ROOT.glob("part-*/module-*/")):
        added, redirected, removed = reconcile_module(mod_dir)
        if added or removed:
            print(f"  {mod_dir.name}: +{added} cards added, -{removed} cards removed")
            total_added += added
            total_removed += removed
    print(f"\nTotal: +{total_added} added, -{total_removed} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
