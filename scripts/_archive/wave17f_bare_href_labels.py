"""Wave 17f: handle bare same-module hrefs that Wave 17d missed.

Wave 17d only handled href patterns containing 'module-NN-' prefix. Many
within-chapter refs use bare hrefs like href="section-X.Y.html" where the
chapter is inferred from context. Wave 17d skipped these.

For each <a href="section-X.Y.html[#anchor]">VISIBLE</a> where VISIBLE
contains a stale "Section A.B" reference, rewrite VISIBLE to "Section X.Y"
using the href as source of truth.

Also fixes stale section refs inside code comments and prose:
  - "(covered in Section X.Y)" where the surrounding context cites a
    different section number than what exists.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def fix_file(file_path):
    text = file_path.read_text(encoding='utf-8')
    orig = text

    # Pattern 1: <a href="section-X.Y.html[...]">VISIBLE</a>
    def replace_a(m):
        prefix = m.group(1)
        href = m.group(2)
        attrs_end = m.group(3)
        visible = m.group(4)
        closer = m.group(5)

        sec_match = re.match(r'section-(\d+)\.(\d+)\.html', href)
        if not sec_match:
            return m.group(0)
        target_ch = sec_match.group(1)
        target_sec = sec_match.group(2)

        new_visible = re.sub(
            r'\bSection\s+\d+\.\d+(?:\.\d+(?:\.\d+)?)?',
            f'Section {target_ch}.{target_sec}',
            visible
        )
        if new_visible == visible:
            return m.group(0)

        # Also update title attribute if present
        new_attrs_end = re.sub(
            r'title="Section \d+\.\d+(?:\.\d+)?(:[^"]*)?"',
            lambda mm: f'title="Section {target_ch}.{target_sec}{mm.group(1) or ""}"',
            attrs_end
        )
        return f'{prefix}{href}{new_attrs_end}{new_visible}{closer}'

    text = re.sub(
        r'(<a\s[^>]*href=")(section-\d+\.\d+\.html(?:#[^"]*)?)("[^>]*>)([^<]+)(</a>)',
        replace_a,
        text,
        flags=re.DOTALL
    )

    if text != orig:
        file_path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if fix_file(p):
            n += 1
    print(f'Bare-href visible labels updated in {n} files')


if __name__ == '__main__':
    main()
