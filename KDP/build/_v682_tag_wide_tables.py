"""Tag wide comparison tables with the 'complex-table' CSS class so the
EPUB renders them at smaller font + tighter padding instead of
flattening cells on Kindle.

The user reported the serverless comparison table (section-28.1, 5
columns) rendering as flattened inline text on Kindle. The EPUB CSS
already has a complex-table class designed for this case but the
tables were not tagged. This script adds the class to every <table>
inside a .comparison-table div that has 4+ columns.

Idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Find: <div class="comparison-table">...<table>...</table>...</div>
# Replace: <table class="complex-table"> if 4+ <th> cols and not already tagged
BLOCK_RE = re.compile(
    r'<div class="comparison-table">[\s\S]*?<table([^>]*)>[\s\S]*?</table>[\s\S]*?</div>',
)


def col_count(table_html: str) -> int:
    """Count <th> cells in the first row of the table."""
    first_tr = re.search(r'<tr[^>]*>([\s\S]*?)</tr>', table_html)
    if not first_tr:
        return 0
    return len(re.findall(r'<th\b', first_tr.group(1)))


def add_complex_class(attrs: str) -> str:
    """Add complex-table to the class attribute of a <table>."""
    if 'class="' in attrs or "class='" in attrs:
        # Existing class attribute -> append
        new = re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} complex-table"' if 'complex-table' not in m.group(1) else m.group(0), attrs)
        return new
    return attrs + ' class="complex-table"'


def main() -> int:
    n_files = 0
    n_tagged = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        original = text
        local_tagged = 0

        def maybe_tag(m: re.Match) -> str:
            nonlocal local_tagged
            block = m.group(0)
            # Find the <table ...> opening within the block
            table_open_m = re.search(r'<table([^>]*)>', block)
            if not table_open_m:
                return block
            attrs = table_open_m.group(1)
            if 'complex-table' in attrs:
                return block  # already tagged
            cols = col_count(block)
            if cols < 4:
                return block  # narrow table; standard styles work
            new_attrs = add_complex_class(attrs)
            new_open = f'<table{new_attrs}>'
            local_tagged += 1
            return block[:table_open_m.start()] + new_open + block[table_open_m.end():]

        new_text = BLOCK_RE.sub(maybe_tag, text)
        if new_text != original:
            p.write_text(new_text, encoding='utf-8')
            n_files += 1
            n_tagged += local_tagged
            print(f'  tagged {local_tagged}x: {p.relative_to(ROOT)}')
    print(f'\nTagged {n_tagged} wide tables (4+ columns) with complex-table class '
          f'across {n_files} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
