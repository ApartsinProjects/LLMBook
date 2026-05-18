"""Phase 8: rebuild Part 8 + Part 10 index.html chapter-card lists.

After the restructure, part indexes still list old module slugs in their
chapter-card sections. This script walks the current module dirs in each
restructured part and regenerates the chapter card list.

Targeted at parts 8, 9, 10 since those are the parts touched by the Part 8
restructure. Skips other parts.

DRY-RUN by default.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def get_chapter_title(mod_dir: Path) -> str:
    idx = mod_dir / "index.html"
    if not idx.exists():
        return "?"
    t = idx.read_text(encoding="utf-8")
    m = re.search(r"<h1>([^<]+)</h1>", t)
    return m.group(1) if m else "?"


def get_chapter_subtitle(mod_dir: Path) -> str:
    """Extract a 1-2 sentence overview from the chapter's overview/big-picture callout."""
    idx = mod_dir / "index.html"
    if not idx.exists():
        return ""
    t = idx.read_text(encoding="utf-8")
    # Look for <div class="overview">...<p>...</p>
    m = re.search(r'<div class="overview">[\s\S]*?<p>([^<]+)</p>', t)
    if m:
        return m.group(1)
    # Or big-picture
    m = re.search(r'<div class="callout big-picture">[\s\S]*?<p>([^<]+)</p>', t)
    if m:
        return m.group(1)
    # Or meta description
    m = re.search(r'<meta content="(?:Chapter \d+: )?[^.]+\. ([^"]+)"', t)
    if m:
        return m.group(1)
    return ""


def get_chapter_num(slug: str) -> int | None:
    m = re.match(r"module-(\d+)-", slug)
    if m:
        return int(m.group(1))
    return None


def regenerate_part_index(part_dir: Path, dry_run: bool) -> int:
    idx = part_dir / "index.html"
    if not idx.exists():
        return 0
    text = idx.read_text(encoding="utf-8")

    # Build new chapter-card list
    modules = sorted(part_dir.glob("module-*/"), key=lambda p: get_chapter_num(p.name) or 999)
    cards = []
    for mod in modules:
        if not mod.is_dir():
            continue
        ch_num = get_chapter_num(mod.name)
        if ch_num is None:
            continue
        title = get_chapter_title(mod)
        subtitle = get_chapter_subtitle(mod)
        # Trim subtitle if too long
        if len(subtitle) > 250:
            subtitle = subtitle[:240].rsplit(" ", 1)[0] + "..."
        card = (
            f'<a class="chapter-card" href="{mod.name}/index.html">\n'
            f'<span class="chapter-num">Chapter {ch_num}</span>\n'
            f'<span class="chapter-title">{title}</span>\n'
            f'<span class="chapter-desc">{subtitle}</span>\n'
            f'</a>'
        )
        cards.append(card)
    new_card_list = "\n".join(cards)

    # Replace the existing chapter-card list block
    # Pattern: find <div class="chapter-card-list"> ... </div> or similar wrapper
    # Some part indexes use <ul class="chapter-card-list"> instead.
    patterns = [
        (r'<div class="chapter-card-list">[\s\S]*?</div>',
         f'<div class="chapter-card-list">\n{new_card_list}\n</div>'),
        (r'<ul class="chapter-card-list">[\s\S]*?</ul>',
         f'<ul class="chapter-card-list">\n{new_card_list}\n</ul>'),
    ]
    new_text = text
    for pat, repl in patterns:
        if re.search(pat, new_text):
            new_text = re.sub(pat, repl, new_text)
            break
    if new_text == text:
        # No chapter-card-list found — append after first <h2>Chapters</h2> or similar
        # For safety, just print and move on
        print(f"  WARN: no chapter-card-list block found in {idx.relative_to(ROOT)}")
        return 0
    if new_text != text and not dry_run:
        idx.write_text(new_text, encoding="utf-8")
    return 1 if new_text != text else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    print(f"=== Phase 8: rebuild part-index chapter cards ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)")
    print()
    n = 0
    for part_name in ["part-8-evaluation-production",
                      "part-9-safety-security-ethics",
                      "part-10-idea-to-product"]:
        part_dir = ROOT / part_name
        if not part_dir.exists():
            continue
        if regenerate_part_index(part_dir, dry_run):
            print(f"  REGEN: {part_name}/index.html")
            n += 1
    print(f"=== Summary ===")
    print(f"Part indexes rebuilt: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
