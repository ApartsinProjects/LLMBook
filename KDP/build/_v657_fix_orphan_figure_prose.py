"""Fix paragraphs that start with a bare verb (e.g. '<p> shows the layered
memory architecture.</p>'). These are leftovers from an early script that
stripped '[Figure X.Y]' references but left the verb behind, producing
sentences with no subject.

Strategy: for each match, look at the next ~25 lines for a <figcaption>
or <div class="diagram-caption"> that names a figure number. Use that
as the new subject. If no nearby figure number exists, fall back to
'The diagram below' as a safe generic.

Idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Match: <p> followed by whitespace then a "showing" verb
ORPHAN_PATTERN = re.compile(
    r'<p>\s+(presents|illustrates|shows|outlines|depicts|demonstrates|visualizes|traces)\s',
    re.MULTILINE,
)
FIGURE_REF_PATTERN = re.compile(
    r'<(?:figcaption|div class="diagram-caption")>\s*<strong>\s*(?:Figure\s+)?'
    r'([\d]+(?:\.[\d]+)+(?:[a-z])?)\s*</strong>',
)


def main() -> int:
    n_fixed = 0
    files_changed = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        original = text
        out_chunks = []
        last_idx = 0
        for m in ORPHAN_PATTERN.finditer(text):
            verb = m.group(1)
            # Look ahead 1500 chars for the next figure caption
            window = text[m.end(): m.end() + 1500]
            cap = FIGURE_REF_PATTERN.search(window)
            if cap:
                subject = f'Figure {cap.group(1)}'
            else:
                subject = 'The diagram below'
            replacement = f'<p>{subject} {verb} '
            out_chunks.append(text[last_idx: m.start()])
            out_chunks.append(replacement)
            last_idx = m.end()
            n_fixed += 1
        out_chunks.append(text[last_idx:])
        new_text = ''.join(out_chunks)
        if new_text != original:
            p.write_text(new_text, encoding='utf-8')
            files_changed += 1
            print(f'  fixed: {p.relative_to(ROOT)}')

    print(f'\nFixed {n_fixed} orphan-prose paragraphs across {files_changed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
