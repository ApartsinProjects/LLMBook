"""Wave 34f: Move <footer> inside <main> in 69 index pages.

Canonical (474/543 files): <footer> sits inside <main>, immediately before </main>.
Outlier pattern (69 files, all index.html): </main> appears BEFORE <footer>.

Fix pattern:
  Before:
    ...content...
    </main>
    <footer><p>...</p></footer>
    </body>

  After:
    ...content...
    <footer><p>...</p></footer>
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

# </main> ... <footer>...</footer>  ->  <footer>...</footer> ... </main>
PATTERN = re.compile(
    r'(</main>\s*)(<footer[^>]*>[\s\S]*?</footer>\s*)',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        end_main, footer = m.group(1), m.group(2)
        return footer + end_main
    return PATTERN.subn(repl, text)


def main():
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        # Quick filter: must have </main> followed by <footer>
        if not re.search(r'</main>\s*<footer', text, re.IGNORECASE):
            continue
        new, n = fix(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            print(f'  {p.relative_to(ROOT)}: footer moved inside main')
    print(f'\nMoved <footer> inside <main> in {n_files} files')


if __name__ == '__main__':
    main()
