"""v14.2: Replace hard-coded edition/year strings in source HTML with
build-time template placeholders.

Before:
    <footer><p>Fourteenth Edition, 2026 &middot; ...

After:
    <footer><p>{{book.edition}}, {{book.publication_year}} &middot; ...

The matching build hook (_html2epub_hooks.templatize_metadata) substitutes
these placeholders from metadata.yaml at build time. Next edition bump
only touches metadata.yaml + html2epub.toml; no source HTML touch.

Run: python _fix_v14_2_templatize_metadata.py [--dry-run | --apply]
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2epub', 'pagefind', 'temp_epub', 'agents/', 'templates/',
        'source_fix_backups', 'scripts/_exercise_payloads']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# Each tuple: (regex, replacement, description). All capture groups
# preserved via \1, \2... in replacement.
PATTERNS = [
    # Footer text: "Fourteenth Edition, 2026 ·"
    (
        re.compile(r'(Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|'
                   r'Eighteenth|Nineteenth|Twentieth)\s+Edition,\s+'
                   r'(2025|2026|2027|2028|2029|2030)'),
        '{{book.edition}}, {{book.publication_year}}',
        'edition + year (footer)',
    ),
    # Just "Fourteenth Edition" alone
    (
        re.compile(r'\b(Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|'
                   r'Eighteenth|Nineteenth|Twentieth)\s+Edition\b'),
        '{{book.edition}}',
        'edition only',
    ),
]


def fix_file(p: Path, dry_run: bool) -> int:
    try:
        original = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return 0
    text = original
    n_total = 0
    for pattern, replacement, _desc in PATTERNS:
        text, n = pattern.subn(replacement, text)
        n_total += n
    if n_total > 0 and text != original and not dry_run:
        p.write_text(text, encoding='utf-8')
    return n_total


def main():
    dry = '--apply' not in sys.argv
    print('DRY RUN. Pass --apply to write changes.' if dry
          else 'APPLY mode.')
    n_files = 0
    n_subs = 0
    for p in ROOT.rglob('*.html'):
        if is_skip(p):
            continue
        n = fix_file(p, dry)
        if n > 0:
            n_files += 1
            n_subs += n
    print()
    print(f'Files affected: {n_files}')
    print(f'Substitutions:  {n_subs}')


if __name__ == '__main__':
    main()
