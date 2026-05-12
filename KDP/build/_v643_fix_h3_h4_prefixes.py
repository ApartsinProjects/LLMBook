"""v6.43: Fix h3/h4 numeric prefixes that don't match their section file.

The v6.40 renumber rewrote h2/h3 prefixes but missed deeper sub-headings
like '<h3>18.1.1.1 Title</h3>' inside section-31.1.html (was section-18.1).
This script normalizes any h3/h4 prefix to match the section file's chapter
and section number.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Pattern: <h3 ...>NN.M.K(.L)? Title</h3> or <h4...>NN.M.K(.L)? Title</h4>
PREFIX_RE = re.compile(
    r'(<h[34][^>]*>)\s*(\d+)\.(\d+)\.(\d+)(\.\d+)?(\s)'
)


def main() -> int:
    fixed = 0
    files_changed = 0
    for p in sorted(ROOT.glob('part-*/module-*/section-*.html')):
        text = p.read_text(encoding='utf-8', errors='replace')
        fn_m = re.match(r'section-(\d+)\.(\d+)', p.stem)
        if not fn_m:
            continue
        chap, sec = fn_m.group(1), fn_m.group(2)

        def repl(m: re.Match) -> str:
            nonlocal fixed
            h_chap, h_sec = m.group(2), m.group(3)
            # Only rewrite if the existing prefix doesn't match
            if h_chap == chap and h_sec == sec:
                return m.group(0)
            fixed += 1
            tail = m.group(4) + (m.group(5) or '')
            return f'{m.group(1)}{chap}.{sec}.{tail}{m.group(6)}'

        new_text = PREFIX_RE.sub(repl, text)
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            files_changed += 1
    print(f'Fixed {fixed} h3/h4 prefix mismatches across {files_changed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
