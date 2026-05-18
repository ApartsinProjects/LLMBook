"""Wave 34c: Swap prerequisites + big-picture to canonical order.

Canonical: epigraph -> big-picture -> prerequisites -> body.

51 pages currently have the order reversed (prerequisites BEFORE big-picture).
Swap them to match the 168-page dominant pattern.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

# Match: prerequisites block immediately followed (with only whitespace) by big-picture block.
SWAP_RE = re.compile(
    r'(<div\s+class="prerequisites"[^>]*>[\s\S]*?</div>\s*'
    r'(?:<figure[\s\S]*?</figure>\s*)?)'  # optional intervening figure (rare)
    r'(<div\s+class="callout\s+big-picture"[^>]*>[\s\S]*?</div>\s*)'
    r'(?=<div|<h[1-6]|<nav|<details|<section|<figure|<p)',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        prereq, bp = m.group(1), m.group(2)
        return bp + prereq
    return SWAP_RE.subn(repl, text)


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        if 'prerequisites' not in text or 'big-picture' not in text:
            continue
        # Only attempt swap if prerequisites appears BEFORE big-picture
        prereq_pos = text.find('class="prerequisites"')
        bp_pos = text.find('class="callout big-picture"')
        if prereq_pos == -1 or bp_pos == -1 or prereq_pos > bp_pos:
            continue
        new, n = fix(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
            print(f'  {p.relative_to(ROOT)}: swapped')
    print(f'\nSwapped prereq <-> big-picture in {n_files} files ({n_total} blocks)')


if __name__ == '__main__':
    main()
