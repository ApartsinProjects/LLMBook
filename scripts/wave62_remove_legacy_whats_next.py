"""Wave 62: When a section has BOTH <div class="callout whats-next"> (canonical)
and <div class="whats-next"> (legacy), keep the canonical and remove the legacy.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match the LEGACY <div class="whats-next"> ... </div> block (where the
# attribute is exactly "whats-next", no preceding callout class)
LEGACY_WN_RE = re.compile(
    r'<div\s+class="whats-next"[^>]*>(?:(?!</div>).)*?</div>',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    # If file has BOTH forms, remove the legacy one
    has_canonical = 'class="callout whats-next"' in text
    has_legacy = re.search(r'<div\s+class="whats-next"', text, re.IGNORECASE)
    if not (has_canonical and has_legacy):
        return 0

    # Remove legacy form (keep first match, remove if exists)
    n_removed = 0

    def repl(m: re.Match) -> str:
        nonlocal n_removed
        n_removed += 1
        return ''

    new_text = LEGACY_WN_RE.sub(repl, text, count=1)
    # If multiple legacies, keep iterating
    while LEGACY_WN_RE.search(new_text):
        new_text = LEGACY_WN_RE.sub(repl, new_text, count=1)

    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n_removed


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
            print(f'  {p.relative_to(ROOT)}: removed {n} legacy whats-next')
    print(f'\nTotal: {n_total} across {files_touched} files')


if __name__ == '__main__':
    main()
