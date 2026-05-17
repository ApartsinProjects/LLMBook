"""Wave 27b: force visible heading number to match the canonical ID.

After Wave 27 fixed double-prefix IDs, some visible text remained drifted
(e.g. "71.1.711.1" where 711 is a corrupt concat of two prefix attempts).
The ID is the canonical source of truth: if id="71-1-1-...", visible
should be "71.1.1 ...".

Strategy: for each <h2 id="..."> or <h3 id="..."> matching the canonical
"N-M-..." pattern, if the visible text starts with a number sequence
that doesn't match the ID's numeric prefix, rewrite the visible.

Only rewrites visible text where the existing visible numbering is
clearly NOT just the slug — i.e. the visible starts with digits.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}


def fix_file(text: str) -> tuple[str, int]:
    n = 0

    def rewrite(m):
        nonlocal n
        tag = m.group(1)
        h_id = m.group(2)
        visible = m.group(3)
        rest = m.group(4)

        # ID parts; need at least 3 numeric
        id_parts = h_id.split('-')
        numeric_prefix = []
        for part in id_parts:
            if part.isdigit():
                numeric_prefix.append(part)
            else:
                break
        if len(numeric_prefix) < 3:
            return m.group(0)

        canonical_visible_num = '.'.join(numeric_prefix)
        # Parse the visible's leading number sequence
        vis_m = re.match(r'^([\d.]+)(\s|$)', visible)
        if not vis_m:
            return m.group(0)
        vis_num = vis_m.group(1).rstrip('.')
        if vis_num == canonical_visible_num:
            return m.group(0)
        # Replace
        n += 1
        new_visible = canonical_visible_num + visible[len(vis_m.group(1)):]
        return f'<{tag} id="{h_id}">{new_visible}{rest}</{tag}>'

    new_text = re.sub(
        r'<(h[234])\s+id="([^"]+)">([\d.]+\s[^<]*)((?:</\1>)?)',
        rewrite,
        text,
    )
    # Note: above regex needs cleanup; do it with a more careful pattern
    text2 = text
    text2 = re.sub(
        r'<(h[234])\s+id="([^"]+)">([\d.]+)(\s[^<]*)</\1>',
        rewrite,
        text2,
    )

    def rewrite2(m):
        nonlocal n
        tag = m.group(1)
        h_id = m.group(2)
        vis_num = m.group(3)
        rest = m.group(4)
        id_parts = h_id.split('-')
        numeric_prefix = []
        for part in id_parts:
            if part.isdigit():
                numeric_prefix.append(part)
            else:
                break
        if len(numeric_prefix) < 3:
            return m.group(0)
        canonical = '.'.join(numeric_prefix)
        if vis_num.rstrip('.') == canonical:
            return m.group(0)
        n += 1
        return f'<{tag} id="{h_id}">{canonical}{rest}</{tag}>'

    text2 = re.sub(
        r'<(h[234])\s+id="([^"]+)">([\d.]+)(\s[^<]*)</\1>',
        rewrite2,
        text,
    )

    return text2, n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix_file(text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
    print(f'Synced visible heading numbers to IDs: {n_total} in {n_files} files')


if __name__ == '__main__':
    main()
