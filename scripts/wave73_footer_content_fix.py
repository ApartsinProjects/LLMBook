"""Wave 73: Move misplaced content from after </footer> back to before
<nav class="chapter-nav">.

For each affected file:
  pattern: ...content... <nav class="chapter-nav">...</nav>\n<footer>...</footer>\n<MISPLACED>\n</main>
  fix:     ...content... <MISPLACED>\n<nav class="chapter-nav">...</nav>\n<footer>...</footer>\n</main>

Affected files (from cycle 39 scan):
  - section-37.3 (See Also callout after footer)
  - section-72.1 (See Also callout after footer)
  - section-66.1 (Pagefind init script — actually OK if outside </main>; this
    is a special case handled separately)
  - index.html (different structure; leave alone unless flagged)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Pattern: capture <nav chapter-nav>...</nav><footer>...</footer> then orphaned content
# then </main>. Move the orphan to BEFORE <nav class="chapter-nav">.
FOOTER_ORPHAN_RE = re.compile(
    r'(<nav\s+class="chapter-nav">.*?</nav>\s*'
    r'<footer\b[^>]*>.*?</footer>)\s*\n'
    r'((?:(?!</main>).)*?)\s*\n?(</main>)',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    orig = text

    m = FOOTER_ORPHAN_RE.search(text)
    if not m:
        return 0

    nav_footer = m.group(1)
    orphan = m.group(2).strip()
    end_main = m.group(3)

    if not orphan:
        return 0

    # Filter out trailing <script>/<style> blocks (those are OK after </main> for HTML5,
    # but the book's convention is </main> first then script). If the orphan is
    # ONLY a script block, leave it where it is.
    orphan_stripped = re.sub(r'<script\b[\s\S]*?</script>', '', orphan).strip()
    if not orphan_stripped:
        return 0  # only scripts, leave alone

    # Move orphan to BEFORE chapter-nav
    nav_start = m.start(1)
    # Find the position just before the chapter-nav opens
    new_text = (
        text[:nav_start]
        + orphan + '\n'
        + nav_footer + '\n'
        + end_main
        + text[m.end():]
    )

    if new_text == orig:
        return 0
    p.write_text(new_text, encoding='utf-8')
    return 1


def main():
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if fix_file(p):
            n += 1
            print(f'  Fixed: {p.relative_to(ROOT)}')
    print(f'\nPages with content-after-footer repaired: {n}')


if __name__ == '__main__':
    main()
