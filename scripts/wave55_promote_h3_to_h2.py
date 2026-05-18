"""Wave 55: Promote numbered <h3>X.Y.Z Title</h3> subsections to <h2> in
files that have NO <h2> elements at all (only h1 + h3+).

This applies to the new section-44.1, 44.2, 44.3 (created from section-45.2
split) and a handful of other files where the agent used h3 throughout.

Strategy:
  1. Check if file has zero <h2> elements (except for navigation, callouts, etc.)
  2. If so, find all numbered <h3 id="X-Y-Z-..."> tags and promote them to <h2>
  3. ALSO promote the matching closing </h3> tags
  4. Renumber subsubsections (if any h4 exist that should become h3) - optional

Conservative: only acts when the file has zero <h2> in the main content area
(checked between <main> and </main>, excluding callout/whats-next blocks).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

H2_RE = re.compile(r'<h2\b', re.IGNORECASE)
# Match numbered h3: <h3 id="X-Y-Z-..."> with content starting with X.Y.Z
H3_NUMBERED_RE = re.compile(
    r'<h3(\s+id="\d+(?:-\d+)+-[^"]+")[^>]*>(\d+(?:\.\d+)+\s+[^<]+)</h3>',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    # Extract main content
    main_open = re.search(r'<main\b[^>]*>', text, re.IGNORECASE)
    main_close = re.search(r'</main>', text, re.IGNORECASE)
    if not main_open or not main_close:
        return 0
    main_text = text[main_open.end():main_close.start()]
    # Check for any h2 in main content
    if H2_RE.search(main_text):
        return 0

    # Promote numbered h3 to h2
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        attrs = m.group(1)
        content = m.group(2)
        return f'<h2{attrs}>{content}</h2>'

    new_main = H3_NUMBERED_RE.sub(repl, main_text)
    if n == 0:
        return 0
    new_text = text[:main_open.end()] + new_main + text[main_close.start():]
    p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if not p.name.startswith('section-'):
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
            print(f'  {p.relative_to(ROOT)}: promoted {n} h3 -> h2')
    print(f'\nTotal h3 -> h2 promotions: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
