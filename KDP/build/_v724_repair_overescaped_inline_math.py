"""Repair over-escaped \\$ inside <span class="math">...</span> blocks.

v722 escaped some $-amounts that were actually inline math content
because the inline-math heuristic missed patterns like $2N$ (digit-led).
This script repairs the damage by reverting \\$ to $ ONLY inside
<span class="math">...</span> blocks.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

# Match <span class="math">...</span> and repair \$ -> $ inside.
SPAN_MATH = re.compile(
    r'(<span\s+class="math">)([\s\S]*?)(</span>)', re.IGNORECASE)


def repair_block(text: str) -> tuple[str, int]:
    n = [0]

    def repl(m: re.Match) -> str:
        head, body, tail = m.group(1), m.group(2), m.group(3)
        new_body = body.replace('\\$', '$')
        if new_body != body:
            n[0] += body.count('\\$')
        return head + new_body + tail

    return SPAN_MATH.sub(repl, text), n[0]


def main() -> int:
    fix = '--fix' in sys.argv
    n_files = 0
    n_repairs = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if '\\$' not in text:
            continue
        new_text, local = repair_block(text)
        if local:
            n_files += 1
            n_repairs += local
            if fix:
                p.write_text(new_text, encoding='utf-8')
    print(f'Files {"repaired" if fix else "needing repair"}: {n_files}')
    print(f'\\$ -> $ repairs inside <span class="math">: {n_repairs}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
