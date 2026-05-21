"""Wave 38e: Strip stale numeric prefixes from comparison-table-title <em> elements.

Audit finding: 14 comparison-tables have a stale "N.M.K " prefix inside their
`<em>` element, like:

    <div class="comparison-table-title">
      <strong>Table 0.2.1</strong>: <em>1.3 Activation Functions Comparison (as of 2026).</em>
    </div>

The "1.3 " is leftover from the previous chapter numbering and serves no purpose.
Strip it. Result:

    <div class="comparison-table-title">
      <strong>Table 0.2.1</strong>: <em>Activation Functions Comparison (as of 2026).</em>
    </div>
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match the comparison-table-title containing strong + em with stale prefix
PATTERN = re.compile(
    r'(<div class="comparison-table-title"><strong>Table\s+\d+(?:\.\d+){1,2}</strong>:\s*<em>)(\d+(?:\.\d+){1,2}\s+)([^<]+)(</em>)',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    n = 0
    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        return f'{m.group(1)}{m.group(3)}{m.group(4)}'
    new = PATTERN.sub(repl, text)
    return new, n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
            print(f'  {p.relative_to(ROOT)}: stripped {n} stale prefix(es)')
    print(f'\nStripped {n_total} stale em-prefixes across {n_files} files')


if __name__ == '__main__':
    main()
