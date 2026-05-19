"""Strip broken cross-references to the dropped Part 14.

When Part 14 (Designing LLM Agent Products) was dropped, links like:
  <a href="../../part-14-designing-llm-agent-products/...">link text</a>

became dangling. This script unwraps each such anchor, keeping the visible
text but removing the dead link.

We also remove leading whitespace/punctuation that creates orphan
"in Chapter Z" snippets when the surrounding sentence depended on the link
existing. Specifically, common patterns we handle:
  - `(see <a>...</a>)` -> remove the entire parenthetical
  - `, see <a>...</a>` -> drop the clause
  - bare `<a>...</a>` -> just unwrap

Run with --apply to write; default is dry-run.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DROPPED_PART14_HREF = re.compile(
    r'href="[^"]*part-14-designing-llm-agent-products/[^"]*"',
    re.IGNORECASE,
)

# Pattern A: parenthetical "see / cf / e.g." with the dropped link only
#   (see <a href="part-14-...">label</a>) -> remove entire parenthetical
PAREN_SEE = re.compile(
    r'\s*\((?:see also|see|cf\.|cf|e\.g\.|i\.e\.)[^()<]*'
    r'<a\s+(?:[^>]*?)href="[^"]*part-14-designing-llm-agent-products/[^"]*"[^>]*>'
    r'([^<]+)</a>'
    r'[^()<]*\)',
    re.IGNORECASE,
)

# Pattern B: comma-prefixed clause:  ", see <a>label</a>" -> drop clause
COMMA_SEE = re.compile(
    r',\s*(?:see also|see|cf\.|cf|e\.g\.|i\.e\.)\s+'
    r'<a\s+(?:[^>]*?)href="[^"]*part-14-designing-llm-agent-products/[^"]*"[^>]*>'
    r'([^<]+)</a>',
    re.IGNORECASE,
)

# Pattern C: bare anchor → unwrap to its text
BARE_ANCHOR = re.compile(
    r'<a\s+(?:[^>]*?)href="[^"]*part-14-designing-llm-agent-products/[^"]*"[^>]*>'
    r'([^<]*)</a>',
    re.IGNORECASE,
)

SKIP_DIRS = {'_archive', 'node_modules', '.git', '.book-update', 'pagefind',
             'KDP', 'build', 'vendor', '.claude', '__pycache__'}


def walk():
    for path in ROOT.rglob('*.html'):
        if any(s in path.parts for s in SKIP_DIRS):
            continue
        yield path


def fix_file(filepath):
    text = filepath.read_text(encoding='utf-8')
    orig = text
    counts = {'paren': 0, 'comma': 0, 'bare': 0}

    text, n = PAREN_SEE.subn('', text)
    counts['paren'] = n

    text, n = COMMA_SEE.subn('', text)
    counts['comma'] = n

    # Whatever's left, just unwrap
    text, n = BARE_ANCHOR.subn(r'\1', text)
    counts['bare'] = n

    if text != orig:
        return text, counts
    return None, counts


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY MODE' if apply else 'DRY RUN'}\n")
    total_files = 0
    totals = {'paren': 0, 'comma': 0, 'bare': 0}
    for f in walk():
        new_text, c = fix_file(f)
        if new_text is None:
            continue
        total_files += 1
        for k, v in c.items():
            totals[k] += v
        rel = f.relative_to(ROOT)
        print(f"  {rel}: paren={c['paren']} comma={c['comma']} bare={c['bare']}")
        if apply:
            f.write_text(new_text, encoding='utf-8')

    print(f"\nFiles modified: {total_files}")
    print(f"Totals: paren={totals['paren']}, comma={totals['comma']}, bare={totals['bare']}")
    if not apply:
        print("\n(dry-run; pass --apply to actually write)")


if __name__ == '__main__':
    main()
