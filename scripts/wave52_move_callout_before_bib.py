"""Wave 52: Move callouts that were appended AFTER the bibliography back to
BEFORE the bibliography. The FM4_PROMISE agent appended Research Frontier
callouts at the end of section files (after </details>), which violates the
canonical structural order.

For each affected file:
  1. Find the bibliography <details class="bibliography-collapsible"> open tag
  2. Find its matching </details> close
  3. Scan after that for any <div class="callout ..."> ... </div> blocks
     (before chapter-nav)
  4. Move each such callout to just BEFORE the bibliography open tag

The 9 affected files are known from the audit; we operate on those + any
other file that has the same pattern as a defensive sweep.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

BIB_OPEN_RE = re.compile(
    r'<details\s+class="bibliography-collapsible[^"]*"[^>]*>',
    re.IGNORECASE,
)
BIB_CLOSE_TOKEN = '</details>'
# Match a complete <div class="callout TYPE">...</div> block, accounting for
# nested divs by counting opens/closes naively (works because callouts have a
# fixed two-level structure: outer div + callout-title div).
CALLOUT_OPEN_RE = re.compile(r'<div\s+class="callout\s+[a-z-]+"[^>]*>', re.IGNORECASE)


def extract_balanced_div(text: str, start: int) -> int:
    """Given position of `<div ...>` opening, return position just past matching </div>."""
    pos = start
    depth = 0
    while pos < len(text):
        next_open = text.find('<div', pos)
        next_close = text.find('</div>', pos)
        if next_close == -1:
            return -1
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                return pos
    return -1


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    bib_open_m = BIB_OPEN_RE.search(text)
    if not bib_open_m:
        return 0
    # Find the closing </details>
    bib_close = text.find(BIB_CLOSE_TOKEN, bib_open_m.end())
    if bib_close == -1:
        return 0
    after_bib = bib_close + len(BIB_CLOSE_TOKEN)

    # Scan for callouts AFTER bibliography close, BEFORE chapter-nav
    nav_pos = text.find('<nav class="chapter-nav"', after_bib)
    if nav_pos == -1:
        nav_pos = len(text)
    region = text[after_bib:nav_pos]

    callouts_to_move: list[tuple[int, int]] = []  # absolute positions
    rel_pos = 0
    while rel_pos < len(region):
        m = CALLOUT_OPEN_RE.search(region, rel_pos)
        if not m:
            break
        abs_start = after_bib + m.start()
        # Find matching </div>
        abs_end = extract_balanced_div(text, abs_start)
        if abs_end == -1:
            break
        callouts_to_move.append((abs_start, abs_end))
        rel_pos = (abs_end - after_bib)
    if not callouts_to_move:
        return 0

    # Build new text: bibliography stays in place; callouts get inserted
    # immediately BEFORE the bibliography open tag.
    bib_open_pos = bib_open_m.start()
    callout_blocks = []
    for s, e in callouts_to_move:
        callout_blocks.append(text[s:e])

    # Remove callouts from their original location (after bib)
    # Iterate right-to-left so positions stay valid
    new_text = text
    for s, e in reversed(callouts_to_move):
        # Also consume trailing whitespace/newline so we don't leave blank lines
        end_extended = e
        while end_extended < len(new_text) and new_text[end_extended] in ' \t\n':
            end_extended += 1
        new_text = new_text[:s] + new_text[end_extended:]
        # Update bib_open_pos if it's after this deletion (no — bib is before, won't shift)

    # Now insert callouts before bibliography open
    insert_text = '\n'.join(callout_blocks) + '\n'
    new_text = new_text[:bib_open_pos] + insert_text + new_text[bib_open_pos:]

    p.write_text(new_text, encoding='utf-8')
    return len(callouts_to_move)


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
            print(f'  {p.relative_to(ROOT)}: moved {n} callout(s) before bib')
    print(f'\nTotal callouts repositioned: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
