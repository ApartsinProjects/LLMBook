"""Wave 35a: Install Google Analytics (gtag.js) with measurement ID G-PWPHBQL2VL.

Inserts the GA4 snippet into the <head> of every book page. The snippet is
placed RIGHT AFTER <meta charset="utf-8"/> so it loads as early as possible
(GA recommends placing it as high in <head> as practical).

Idempotent: detects existing snippet via the measurement ID and skips files
already containing it.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

MEASUREMENT_ID = "G-PWPHBQL2VL"

GA_SNIPPET = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{MEASUREMENT_ID}');
</script>
'''

# Insert after <meta charset="..."/>
INSERT_AFTER = re.compile(r'(<meta\s+charset="[^"]*"\s*/?>)', re.IGNORECASE)


def fix(text: str) -> tuple[str, int]:
    # Idempotent: skip if measurement ID already present
    if MEASUREMENT_ID in text:
        return text, 0
    new, n = INSERT_AFTER.subn(
        lambda m: m.group(1) + '\n' + GA_SNIPPET,
        text,
        count=1,
    )
    return new, n


def main():
    n_files = 0
    n_skipped = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
        elif MEASUREMENT_ID in text:
            n_skipped += 1
    print(f'Installed GA4 (id={MEASUREMENT_ID}) on {n_files} pages')
    if n_skipped:
        print(f'Skipped {n_skipped} pages already containing the snippet')


if __name__ == '__main__':
    main()
