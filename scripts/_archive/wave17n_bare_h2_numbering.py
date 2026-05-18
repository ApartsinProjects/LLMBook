"""Wave 17N: convert bare H2 numbering ("1. Foo", "2. Bar") to canonical
"ch.sec.N Foo" format. Found 413 bare H2s across 59 section files.

For each section file at .../module-NN-slug/section-N.M.html:
  - Canonical chapter = N (from filename); section = M
  - For each <h2 id="K-slug">K. Text</h2> where K is a single integer:
    rewrite to <h2 id="N-M-K-slug">N.M.K Text</h2>
  - Same for h3 with bare 1-level numbering ("1.1. Foo")
  - Same for href="#K-slug" anchor refs
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def fix_file(sf):
    sm = re.match(r'section-(\d+)\.(\d+)\.html', sf.name)
    if not sm:
        return False
    ch = sm.group(1)
    sec = sm.group(2)

    text = sf.read_text(encoding='utf-8')
    orig = text

    # Pattern: <h2 id="N-slug">N. Text</h2>
    # where N is a single integer and the slug starts with "N-"
    def rewrite_h2(m):
        h_id = m.group(1)
        visible = m.group(2)
        rest = m.group(3)
        # If id is "K-slug" where K matches visible
        id_parts = h_id.split('-', 1)
        if len(id_parts) >= 2 and id_parts[0].isdigit():
            sub_n = id_parts[0]
            slug = id_parts[1]
            if visible == sub_n:
                # Rewrite to canonical
                new_id = f'{ch}-{sec}-{sub_n}-{slug}'
                new_vis = f'{ch}.{sec}.{sub_n}'
                return f'<h2 id="{new_id}">{new_vis}{rest}</h2>'
        return m.group(0)

    text = re.sub(
        r'<h2 id="([^"]+)">(\d+)\.([^<]*)</h2>',
        rewrite_h2,
        text
    )

    # H3 with 2-level bare "1.1. Foo"
    def rewrite_h3(m):
        h_id = m.group(1)
        v_n1 = m.group(2)
        v_n2 = m.group(3)
        rest = m.group(4)
        id_parts = h_id.split('-', 2)
        if (len(id_parts) >= 3 and id_parts[0].isdigit() and id_parts[1].isdigit()
                and id_parts[0] == v_n1 and id_parts[1] == v_n2):
            slug = id_parts[2]
            new_id = f'{ch}-{sec}-{v_n1}-{v_n2}-{slug}'
            new_vis = f'{ch}.{sec}.{v_n1}.{v_n2}'
            return f'<h3 id="{new_id}">{new_vis}{rest}</h3>'
        return m.group(0)

    text = re.sub(
        r'<h3 id="([^"]+)">(\d+)\.(\d+)\.([^<]*)</h3>',
        rewrite_h3,
        text
    )

    # Same-page anchor href="#N-slug" where N is single int → "#ch-sec-N-slug"
    def rewrite_anchor(m):
        prefix = m.group(1)
        anchor = m.group(2)
        # Match "K-slug" where K is digit only
        parts = anchor.split('-', 1)
        if len(parts) >= 2 and parts[0].isdigit() and not parts[1][0].isdigit():
            # Only one numeric component — bare
            return f'{prefix}#{ch}-{sec}-{anchor}'
        return m.group(0)

    text = re.sub(
        r'(href=")#(\d+-[^"]+)',
        rewrite_anchor,
        text
    )

    if text != orig:
        sf.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for sf in sorted(ROOT.rglob('section-*.html')):
        if set(sf.parts) & SKIP:
            continue
        if fix_file(sf):
            n += 1
    print(f'Fixed bare H2/H3 numbering in {n} section files')


if __name__ == '__main__':
    main()
