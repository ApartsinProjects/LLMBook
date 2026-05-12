"""v6.49: Fix section-card numeric labels in chapter index pages.

Pattern: chapter index pages contain section-card blocks like
   <a href="section-18.1.html" class="section-card">
       <span class="section-num">20.1</span>   <-- wrong, file is 18.1
       ...
   </a>

The v6.40 renumber updated the hrefs but the visible labels in
<span class="section-num">X.Y</span> were not. This script reads the
href of each card, parses the section file's actual number, and
overwrites the span's content to match.

Idempotent: runs only when there's a mismatch.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def fix_index(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    original = text
    # Match: <a href="section-N.M.html" class="section-card"> ... <span class="section-num">XXX</span>
    # Extract href's section number and rewrite the span.
    pattern = re.compile(
        r'(<a\s+href="section-(\d+)\.(\d+)\.html"\s+class="section-card"[^>]*>'
        r'(?:[^<]|<(?!span))*?<span class="section-num">)\s*([^<]+?)\s*(</span>)',
        re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        href_chap = m.group(2)
        href_sec = m.group(3)
        new_num = f'{href_chap}.{href_sec}'
        return f'{m.group(1)}{new_num}{m.group(5)}'

    new_text, n = pattern.subn(repl, text)
    if n > 0 and new_text != original:
        p.write_text(new_text, encoding='utf-8')
        return n
    return 0


def main() -> int:
    fixed_total = 0
    files_changed = 0
    for p in sorted(list(ROOT.glob('part-*/module-*/index.html')) +
                    list(ROOT.glob('appendices/appendix-*/index.html'))):
        n = fix_index(p)
        if n > 0:
            fixed_total += n
            files_changed += 1
            print(f'  {p.relative_to(ROOT)}: rewrote {n} section-num labels')
    print(f'\nFixed {fixed_total} section-num labels across {files_changed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
