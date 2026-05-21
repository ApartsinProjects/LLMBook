"""Wave 54: Add target="_blank" rel="noopener" to external <a> tags that
lack one or both attributes.

External = href starts with http:// or https:// or //.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

EXT_LINK_RE = re.compile(
    r'<a\s+([^>]*\bhref="(?:https?:)?//[^"]+"[^>]*)>',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        attrs = m.group(1)
        new_attrs = attrs
        if 'target=' not in attrs.lower():
            new_attrs = new_attrs.rstrip() + ' target="_blank"'
        if 'rel=' not in attrs.lower():
            new_attrs = new_attrs.rstrip() + ' rel="noopener"'
        if new_attrs == attrs:
            return m.group()
        n += 1
        return f'<a {new_attrs}>'

    new_text = EXT_LINK_RE.sub(repl, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
    print(f'External links fixed: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
