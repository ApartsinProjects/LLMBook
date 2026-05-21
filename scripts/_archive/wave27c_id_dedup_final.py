"""Wave 27c: fix double-prefix IDs that Wave 27 missed because visible text
didn't match the strict 5-component dotted pattern.

For each <h2 id="A-B-A-B-C-..."> or <h3 id="A-B-A-B-C-D-...">, strip the
double prefix and resync visible.

Same for anchor href="#A-B-A-B-...".
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}


def dedup_id(h_id: str) -> str:
    """A-B-A-B-C-slug → A-B-C-slug (also A-B-A-B-C-D-slug → A-B-C-D-slug)."""
    parts = h_id.split('-')
    if (len(parts) >= 5 and parts[0].isdigit() and parts[1].isdigit()
            and parts[2] == parts[0] and parts[3] == parts[1]):
        return '-'.join([parts[0], parts[1]] + parts[4:])
    return h_id


def fix_file(text: str) -> tuple[str, int]:
    n = 0

    def rewrite_heading(m):
        nonlocal n
        tag = m.group(1)
        h_id = m.group(2)
        inner = m.group(3)
        new_id = dedup_id(h_id)
        if new_id == h_id:
            return m.group(0)
        # Also fix visible number prefix
        # Inner starts with optional number sequence
        id_parts = new_id.split('-')
        numeric_prefix = []
        for part in id_parts:
            if part.isdigit():
                numeric_prefix.append(part)
            else:
                break
        canonical_vis = '.'.join(numeric_prefix)
        m_vis = re.match(r'^([\d.]+)(\s|$)', inner)
        if m_vis:
            new_inner = canonical_vis + inner[len(m_vis.group(1)):]
        else:
            new_inner = inner
        n += 1
        return f'<{tag} id="{new_id}">{new_inner}</{tag}>'

    text = re.sub(
        r'<(h[234])\s+id="([^"]+)">([\s\S]*?)</\1>',
        rewrite_heading,
        text,
    )

    # Anchors
    def rewrite_anchor(m):
        nonlocal n
        prefix = m.group(1)
        anchor_id = m.group(2)
        new = dedup_id(anchor_id)
        if new == anchor_id:
            return m.group(0)
        n += 1
        return f'{prefix}#{new}'

    text = re.sub(
        r'(href=")#([\d-][^"]+)',
        rewrite_anchor,
        text,
    )
    return text, n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix_file(text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
    print(f'Deduped {n_total} heading IDs / anchors in {n_files} files')


if __name__ == '__main__':
    main()
