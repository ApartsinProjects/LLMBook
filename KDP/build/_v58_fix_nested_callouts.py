"""v5.8: Move <aside class="callout..."> blocks that are nested inside
<blockquote class="epigraph"> back OUTSIDE the epigraph.

Epigraphs are supposed to contain only:
  <p>   the quotation
  <cite> the speaker / attribution

Some authoring round dropped Reader's-shortcut and Related-coverage
callouts INSIDE the epigraph, between the quote and the cite. They
render as ugly nested boxes and confuse the attribution.

Audit found 7 affected files (identical structure). Fix:
  - Extract the <aside class="callout...">...</aside> block
  - Place it AFTER </blockquote>, with one blank line of separation
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Match: <blockquote class="...epigraph...">
#   ...
#   (aside callout block we want to extract)
#   ...
#   <cite>...</cite>
#   </blockquote>
EPI_WITH_NESTED = re.compile(
    r'(?P<epi_open><blockquote\s+class="[^"]*epigraph[^"]*"[^>]*>\s*'
    r'<p>(?:.|\n)*?</p>\s*)'
    r'(?P<aside><aside\s+class="callout[^"]*"[^>]*>(?:.|\n)*?</aside>)\s*'
    r'(?P<rest><cite>(?:.|\n)*?</cite>\s*</blockquote>)',
    re.IGNORECASE
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")

    def repl(m: re.Match) -> str:
        return m.group('epi_open') + m.group('rest') + '\n\n' + m.group('aside')

    new, n = EPI_WITH_NESTED.subn(repl, text)
    if n:
        p.write_text(new, encoding="utf-8")
    return n


def main() -> int:
    SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
            'chapter_review', 'downloads', '_archive',
            '_lab_fragments', 'templates'}
    total = 0
    files = 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        n = fix_file(p)
        if n:
            files += 1
            total += n
            print(f'  fixed {n} epigraph(s) in {rel}')
    print(f'\nTotal: {total} extractions across {files} files')
    return 0


if __name__ == "__main__":
    sys.exit(main())
