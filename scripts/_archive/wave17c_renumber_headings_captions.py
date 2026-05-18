"""Wave 17c: book-wide H2/H3 visible numbering + heading IDs + figure / code-fragment
caption number sync to each file's canonical chapter and section number.

For each section file at .../module-NN-slug/section-N.M.html:
  - Canonical chapter = N (matches module-NN, since Wave 12 normalized them)
  - Canonical section = M

For each:
  - <h2 id="A-B-C-slug">V.W.X TITLE</h2>
    Rewrite id to "N-M-C-slug", visible to "N.M.X TITLE"
  - <h3 id="A-B-C-D-slug">V.W.X.Y TITLE</h3>
    Rewrite id to "N-M-C-D-slug", visible to "N.M.X.Y TITLE"
  - <h4 ...> same pattern with 5 components
  - <strong>Figure A.B.C</strong> → "Figure N.M.C"
  - Same for Table, Code Fragment captions

Also rewrites references to these IDs in hrefs (e.g. href="#34-1-1-foo" → "#42-1-1-foo").

This pass handles ~hundreds of stale numbering artifacts left from old
chapter numbering (current waves 11-16 only fixed titles, breadcrumbs,
and section descriptions; the visible H2 / H3 inside section bodies was
left alone, causing readers to see "44.8.1" inside a "Chapter 42" section).
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def get_section_canonical(file_path):
    """Determine canonical (ch, sec) from filename, e.g. section-42.1.html → (42, 1)."""
    m = re.match(r'section-(\d+)\.(\d+)\.html', file_path.name)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def renumber_section_file(file_path, ch, sec):
    """Rewrite headings, anchor IDs, and captions to use (ch, sec) as the prefix."""
    text = file_path.read_text(encoding='utf-8')
    orig = text
    ch_str = str(ch)
    sec_str = str(sec)

    # H2: <h2 id="A-B-C-slug">V.W.X ...</h2>
    # Replace id A-B-C-slug with ch-sec-C-slug
    # Replace visible V.W.X with ch.sec.X (preserving X position)
    def rewrite_h2(m):
        h2_id = m.group(1)
        h2_visible = m.group(2)
        h2_rest = m.group(3)
        # Extract third+ component from id (X-slug part) by splitting on first 2 dashes
        id_parts = h2_id.split('-', 2)
        if len(id_parts) >= 3 and id_parts[0].isdigit() and id_parts[1].isdigit():
            new_id = f'{ch_str}-{sec_str}-{id_parts[2]}'
        else:
            new_id = h2_id  # leave non-numeric IDs alone
        # Extract X from visible "V.W.X" — keep the third numeric component
        vis_parts = h2_visible.split('.')
        if len(vis_parts) >= 3 and vis_parts[0].isdigit() and vis_parts[1].isdigit() and vis_parts[2].isdigit():
            new_vis = f'{ch_str}.{sec_str}.{vis_parts[2]}'
        else:
            new_vis = h2_visible
        return f'<h2 id="{new_id}">{new_vis}{h2_rest}</h2>'

    text = re.sub(
        r'<h2 id="([^"]+)">(\d+\.\d+\.\d+)([^<]*)</h2>',
        rewrite_h2,
        text
    )

    # H3: <h3 id="A-B-C-D-slug">V.W.X.Y ...</h3>
    def rewrite_h3(m):
        h3_id = m.group(1)
        h3_visible = m.group(2)
        h3_rest = m.group(3)
        id_parts = h3_id.split('-', 3)
        if len(id_parts) >= 4 and id_parts[0].isdigit() and id_parts[1].isdigit():
            new_id = f'{ch_str}-{sec_str}-{id_parts[2]}-{id_parts[3]}'
        else:
            new_id = h3_id
        vis_parts = h3_visible.split('.')
        if len(vis_parts) >= 4 and all(p.isdigit() for p in vis_parts[:4]):
            new_vis = f'{ch_str}.{sec_str}.{vis_parts[2]}.{vis_parts[3]}'
        else:
            new_vis = h3_visible
        return f'<h3 id="{new_id}">{new_vis}{h3_rest}</h3>'

    text = re.sub(
        r'<h3 id="([^"]+)">(\d+\.\d+\.\d+\.\d+)([^<]*)</h3>',
        rewrite_h3,
        text
    )

    # H4: 5 components
    def rewrite_h4(m):
        h4_id = m.group(1)
        h4_visible = m.group(2)
        h4_rest = m.group(3)
        id_parts = h4_id.split('-', 4)
        if len(id_parts) >= 5 and id_parts[0].isdigit() and id_parts[1].isdigit():
            new_id = f'{ch_str}-{sec_str}-{id_parts[2]}-{id_parts[3]}-{id_parts[4]}'
        else:
            new_id = h4_id
        vis_parts = h4_visible.split('.')
        if len(vis_parts) >= 5 and all(p.isdigit() for p in vis_parts[:5]):
            new_vis = f'{ch_str}.{sec_str}.{vis_parts[2]}.{vis_parts[3]}.{vis_parts[4]}'
        else:
            new_vis = h4_visible
        return f'<h4 id="{new_id}">{new_vis}{h4_rest}</h4>'

    text = re.sub(
        r'<h4 id="([^"]+)">(\d+\.\d+\.\d+\.\d+\.\d+)([^<]*)</h4>',
        rewrite_h4,
        text
    )

    # Figure / Table / Code Fragment captions: <strong>Figure A.B.C</strong>
    def rewrite_caption(m):
        kind = m.group(1)
        num = m.group(2)
        parts = num.split('.')
        if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
            new_num = f'{ch_str}.{sec_str}.{parts[2]}'
            if len(parts) > 3:
                new_num += '.' + '.'.join(parts[3:])
            return f'<strong>{kind} {new_num}</strong>'
        return m.group(0)

    text = re.sub(
        r'<strong>(Figure|Table|Code Fragment) (\d+\.\d+\.\d+(?:\.\d+)?)</strong>',
        rewrite_caption,
        text
    )

    # Same patterns inside <figcaption> and similar without <strong> wrapping
    text = re.sub(
        r'\b(Figure|Table|Code Fragment)\s+(\d+\.\d+\.\d+(?:\.\d+)?)\b',
        rewrite_caption,
        text
    )

    # Same-page anchor refs: href="#A-B-C-slug" → "#ch-sec-C-slug"
    def rewrite_anchor(m):
        prefix = m.group(1)
        anchor_id = m.group(2)
        id_parts = anchor_id.split('-')
        if len(id_parts) >= 3 and id_parts[0].isdigit() and id_parts[1].isdigit():
            rest = '-'.join(id_parts[2:])
            return f'{prefix}#{ch_str}-{sec_str}-{rest}'
        return m.group(0)

    text = re.sub(
        r'(href=")#(\d+-\d+-[^"]+)',
        rewrite_anchor,
        text
    )

    if text != orig:
        file_path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    n_files = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        ch, sec = get_section_canonical(p)
        if ch is None:
            continue
        if renumber_section_file(p, ch, sec):
            n_files += 1
    print(f'Renumbered headings / captions in {n_files} section files')


if __name__ == '__main__':
    main()
