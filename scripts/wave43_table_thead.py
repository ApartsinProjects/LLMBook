"""Wave 43: Wrap the first <tr> of each <table> in <thead> if the first row
contains only <th> cells (i.e. it's a header row, not a data row).

Pattern observed:
    <table>
      <tr><th>A</th><th>B</th></tr>   <!-- header row -->
      <tr><td>1</td><td>2</td></tr>   <!-- data row -->
    </table>

Fix:
    <table>
      <thead>
        <tr><th>A</th><th>B</th></tr>
      </thead>
      <tr><td>1</td><td>2</td></tr>
    </table>

This is a non-destructive transform: it only adds the <thead> wrapper, leaving
all <th>/<td> content untouched. Skips tables that already have <thead>.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

TABLE_RE = re.compile(r'(<table\b[^>]*>)(\s*)(.*?)(</table>)', re.DOTALL | re.IGNORECASE)
TR_RE = re.compile(r'<tr\b[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
TD_RE = re.compile(r'<td\b', re.IGNORECASE)
TH_RE = re.compile(r'<th\b', re.IGNORECASE)
THEAD_RE = re.compile(r'<thead\b', re.IGNORECASE)


def fix_table(table_full: str) -> tuple[str, bool]:
    """Return (new_table, changed)."""
    m = TABLE_RE.match(table_full)
    if not m:
        return table_full, False
    open_tag = m.group(1)
    leading_ws = m.group(2)
    inner = m.group(3)
    close_tag = m.group(4)

    if THEAD_RE.search(inner):
        return table_full, False  # already has thead

    # Find first <tr>
    tr_m = TR_RE.search(inner)
    if not tr_m:
        return table_full, False

    first_tr_text = tr_m.group()
    first_tr_inner = tr_m.group(1)
    # Header row must contain at least one <th> and zero <td>
    if not TH_RE.search(first_tr_inner) or TD_RE.search(first_tr_inner):
        return table_full, False  # not a header row, skip

    # Wrap the first <tr> in <thead>...</thead>
    new_inner = (
        inner[:tr_m.start()]
        + '<thead>\n'
        + first_tr_text
        + '\n</thead>'
        + inner[tr_m.end():]
    )
    return open_tag + leading_ws + new_inner + close_tag, True


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    orig = text
    n = 0

    def replace_table(m: re.Match) -> str:
        nonlocal n
        full = m.group()
        new, changed = fix_table(full)
        if changed:
            n += 1
        return new

    new_text = TABLE_RE.sub(replace_table, text)
    if new_text != orig:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            n_files += 1
    print(f'Tables wrapped in <thead>: {n_total}')
    print(f'Files touched: {n_files}')


if __name__ == '__main__':
    main()
