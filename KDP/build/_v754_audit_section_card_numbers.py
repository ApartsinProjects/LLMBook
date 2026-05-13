"""Audit + auto-fix stale section-card numbers in module index pages.

After the chapter renumber, module-index pages still use the OLD
chapter number in their section-card prefixes. For example, the file
part-3-working-with-llms/module-12-prompt-engineering/index.html has
section cards labeled "11.1, 11.2..." even though the chapter is now
Chapter 12.

Pattern (broken):
  <a href="section-12.1.html">
    <span class="section-num">11.1</span>    <-- BUG: 11.1, should be 12.1
    ...
  </a>

The URL is correct (section-12.1.html); only the visible display
prefix is wrong.

Algorithm: for each module-XX-NAME/index.html, find every
<a href="...section-X.Y.html">...<span class="section-num">N.M</span>
where X != N. Replace N.M with X.M (and similarly for X.Y.Z).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

LINK_AND_NUM_RE = re.compile(
    r'(<a\s+[^>]*href="[^"]*section-(\d+)\.(\d+)(?:\.(\d+))?\.html"[^>]*>'
    r'[\s\S]*?<span class="section-num">)'
    r'(\d+)\.(\d+)(?:\.(\d+))?'
    r'(</span>)',
    re.IGNORECASE)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    n_fixed = [0]

    def repl(m: re.Match) -> str:
        prefix = m.group(1)
        url_ch, url_sub, url_subsub = m.group(2), m.group(3), m.group(4)
        disp_ch, disp_sub, disp_subsub = m.group(5), m.group(6), m.group(7)
        suffix = m.group(8)
        if url_ch == disp_ch and url_sub == disp_sub and (url_subsub or '') == (disp_subsub or ''):
            return m.group(0)
        new_num = f'{int(url_ch)}.{int(url_sub)}'
        if url_subsub is not None:
            new_num += f'.{int(url_subsub)}'
        n_fixed[0] += 1
        return f'{prefix}{new_num}{suffix}'

    new_text = LINK_AND_NUM_RE.sub(repl, text)
    if n_fixed[0]:
        path.write_text(new_text, encoding='utf-8')
    return n_fixed[0]


def main() -> int:
    total_files = 0
    total_fixed = 0
    # Search all part-X/module-Y/index.html files
    for p in sorted(ROOT.rglob('index.html')):
        sp = str(p).replace('\\', '/')
        if '/module-' not in sp:
            continue
        n = fix_file(p)
        if n:
            total_files += 1
            total_fixed += n
            print(f'  + {n:3d}  {p.relative_to(ROOT)}')
    print(f'\nFiles touched: {total_files}')
    print(f'Section-card numbers fixed: {total_fixed}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
