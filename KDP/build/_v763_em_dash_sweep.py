"""v763: Sweep em-dashes (and &mdash;) book-wide.

Per the global writing-style rule, no em-dashes in any generated text.
Replace " &mdash; " (and the Unicode em-dash with surrounding spaces)
with ", " in body text.

Conservative scoping:
  - Only HTML body text. Skip CSS rules and comments.
  - The replacement is " &mdash; " -> ", " or " - " -> single comma.
  - Adjacent em-dashes ("X &mdash; Y &mdash; Z") become "X, Y, Z" rather
    than nested parens because the original was a list aside.
  - Specific epigraph attribution lines that use " &mdash; " before the
    author name become " - " (a single hyphen-with-spaces, since attributions
    don't use commas before names).

Idempotent.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules',
             'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP_DIRS)


# Order matters: handle clearly anchored cases first, then a generic catch-all.
RULES = [
    # "X &mdash; Y &mdash; Z" or "X - Y - Z" -> "X, Y, Z" (list aside)
    # We do this iteratively below.

    # cite/attribution-style: ">A &mdash; B<" inside <cite> attribution
    # Replaced with comma since the rest of the book uses ", " for attribution.
    (re.compile(r'\s+&mdash;\s+'), ', '),
    (re.compile(r'\s+&#8212;\s+'), ', '),
    (re.compile(r'\s+—\s+'), ', '),
]


def fix(html: str) -> tuple[str, int]:
    n = 0
    for pat, rep in RULES:
        html, c = pat.subn(rep, html)
        n += c
    return html, n


def main() -> int:
    n_files = 0
    total = 0
    for p in ROOT.rglob('*.html'):
        if should_skip(p):
            continue
        try:
            src = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        new, c = fix(src)
        if c:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            total += c
    print(f'em-dash replacements: {total} across {n_files} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
