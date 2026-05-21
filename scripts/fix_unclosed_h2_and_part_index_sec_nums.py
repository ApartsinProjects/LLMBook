"""Two related fixes after the renumber pass:

1. Unclosed <h2 id="..."> tags book-wide. The renumber script's stale-num
   fix only caught some; many h2s remain unclosed. Browsers auto-close
   them but the HEADING_HIERARCHY audit flags h1->h3 skips because the
   h2 isn't recognized.

2. Stale <span class="sec-num">XX.Y</span> values in PART index files
   (separate from the chapter-index fix that already ran). Pattern:
   part-15/index.html has chapter cards showing "80.1", "80.2", ...
   which should be "75.1", "75.2", ...
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Map of old chapter numbers to new (after Part 14 was dropped)
MAP = {72: 67, 73: 68, 74: 69, 75: 70, 76: 71, 77: 72, 78: 73,
       79: 74, 80: 75, 81: 76, 82: 77, 83: 78}


def fix_unclosed_h2(text: str) -> tuple[str, int]:
    """Close any h2 that opens but isn't closed before the next block element."""
    fixed = 0
    # We need to walk h2 openings in file order. For each, look ahead for the
    # FIRST occurrence of either </h2> or another block opener. If a block
    # opener (h1-6, p, div, ul, ol, section, nav, figure) appears before
    # </h2>, insert </h2> right before it.
    h2_open_re = re.compile(r'<h2(?:\s[^>]*)?>', re.IGNORECASE)
    block_or_close_re = re.compile(
        r'</h2>|<(h[1-6]|p|div|ul|ol|section|nav|figure|details|table|pre|blockquote|aside)\b',
        re.IGNORECASE,
    )
    out = []
    last = 0
    for m in h2_open_re.finditer(text):
        out.append(text[last:m.end()])
        last = m.end()
        # Look for </h2> or next block opener
        next_m = block_or_close_re.search(text, m.end())
        if not next_m:
            continue
        if next_m.group(0).lower() == '</h2>':
            # Properly closed
            continue
        # Unclosed: insert </h2> at the next block opener position,
        # stripping trailing whitespace/newline from the h2 body.
        body = text[m.end():next_m.start()].rstrip()
        out.append(body + '</h2>\n')
        last = next_m.start()
        fixed += 1
    out.append(text[last:])
    return ''.join(out), fixed


def fix_part_index_sec_nums(text: str) -> tuple[str, int]:
    """In part-NN/index.html chapter cards, update stale sec-num values
    based on the chapter-card's href (which already points to the NEW
    module dir)."""
    fixed = 0
    # Pattern: <a href="module-NEW-..."><span class="sec-num">OLD.Y</span>...
    # We use the href to derive NEW, then look at the displayed OLD.Y
    chapter_card_re = re.compile(
        r'<a\s+href="module-(\d+)-[^/]+/section-\d+\.[\w]+\.html">'
        r'<span class="sec-num">(\d+)\.(\d+)</span>',
        re.IGNORECASE,
    )

    def replace(m):
        nonlocal fixed
        new_mod = int(m.group(1))
        stale_chap = int(m.group(2))
        sec = m.group(3)
        # If stale_chap maps to new_mod via MAP, fix it
        if MAP.get(stale_chap) == new_mod:
            fixed += 1
            return m.group(0).replace(
                f'>{stale_chap}.{sec}</span>',
                f'>{new_mod}.{sec}</span>',
            )
        return m.group(0)

    new_text = chapter_card_re.sub(replace, text)
    return new_text, fixed


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY' if apply else 'DRY-RUN'}")
    h2_total = 0
    sn_total = 0
    h2_files = 0
    sn_files = 0
    for f in ROOT.rglob('*.html'):
        if any(s in f.parts for s in ('_archive', 'node_modules', '.git',
                                       'pagefind', 'KDP', 'build', 'vendor',
                                       '.claude', '__pycache__', 'templates')):
            continue
        text = f.read_text(encoding='utf-8')
        orig = text
        if f.name.startswith('section-'):
            text, n = fix_unclosed_h2(text)
            if n:
                h2_total += n
                h2_files += 1
                print(f'  H2-close {f.relative_to(ROOT)}: {n}')
        if f.name == 'index.html' and 'module-' not in str(f) and 'part-' in str(f):
            text, n = fix_part_index_sec_nums(text)
            if n:
                sn_total += n
                sn_files += 1
                print(f'  SEC-NUM {f.relative_to(ROOT)}: {n}')
        if text != orig and apply:
            f.write_text(text, encoding='utf-8')
    print(f'\nUnclosed h2 fixed: {h2_total} ({h2_files} files)')
    print(f'Part-index sec-num fixed: {sn_total} ({sn_files} files)')


if __name__ == '__main__':
    main()
