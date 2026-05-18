r"""Fix `\$NUM` patterns outside code blocks: replace with `&#36;NUM` HTML entity.

In prose, `\$15` was the author's intended literal "$15" (price). HTML renders
backslash literally so it shows as "\$15" instead of "$15". Plus KaTeX
auto-render can confuse `\$` for math escapes and break nearby math.

Safe replacement: `\$` → `&#36;` (HTML entity for $). Skip <pre> and <code>
blocks (those are literal code where authors may legitimately have `\$`).
"""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}


def fix_file(text: str) -> tuple[str, int]:
    n = 0
    # Split text by <pre>...</pre> and <code>...</code> blocks; only edit outside
    # blocks.
    parts = re.split(r'(<pre[\s\S]*?</pre>|<code[\s\S]*?</code>)', text)
    for i in range(0, len(parts), 2):  # even indices are non-code
        original = parts[i]
        # Replace \$ followed by alphanumeric (price-like) with &#36;
        new = re.sub(r'\\\$([0-9])', r'&#36;\1', original)
        # Also \$<word> (e.g. \$15M, \$N)
        new = re.sub(r'\\\$([A-Za-z])', r'&#36;\1', new)
        if new != original:
            n += original.count('\\$') - new.count('\\$')
            parts[i] = new
    return ''.join(parts), n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix_file(text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
    print(f'Replaced {n_total} \\$ → &#36; in {n_files} files')


if __name__ == '__main__':
    main()
