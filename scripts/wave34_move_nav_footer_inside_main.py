"""Wave 34g: Move `<nav class="chapter-nav">` AND `<footer>` inside `<main>`.

Canonical (518/543 files now after Wave 34f): main wraps content + chapter-nav + footer.

Outlier pattern (25 files remaining): </main> closes BEFORE the chapter-nav,
leaving nav and footer outside the main element.

Bad:
    ...content...
    </main>
    <nav class="chapter-nav">...</nav>
    <footer>...</footer>
    </body>

Good:
    ...content...
    <nav class="chapter-nav">...</nav>
    <footer>...</footer>
    </main>
    </body>
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

# </main> followed by <nav class="chapter-nav">...</nav> [<footer>...</footer>]?
PATTERN = re.compile(
    r'(</main>\s*)'
    r'(<nav\s+class="chapter-nav"[^>]*>[\s\S]*?</nav>\s*)'
    r'(<footer[^>]*>[\s\S]*?</footer>\s*)?',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        end_main = m.group(1)
        nav = m.group(2)
        footer = m.group(3) or ''
        return nav + footer + end_main
    return PATTERN.subn(repl, text)


def main():
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        # Quick filter
        if not re.search(r'</main>\s*<nav\s+class="chapter-nav"', text, re.IGNORECASE):
            continue
        new, n = fix(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            print(f'  {p.relative_to(ROOT)}: nav+footer moved inside main')
    print(f'\nMoved nav+footer inside main in {n_files} files')


if __name__ == '__main__':
    main()
