"""Wave 27: fix two systematic root-cause bugs.

ROOT CAUSE 1 — Double-prefixed H2/H3 headings (2,610 across 320 files).
Wave 17c renumbered visible H2 numbering and IDs from "X.Y" form to
"ch.sec.X" form. Then Wave 17N (bare H2 sweep) ran on the already-
prefixed headings, prepending the chapter.section prefix AGAIN. Result:
  <h2 id="22-7-22-7-5-fusion-and-generation">22.7.227.5 Fusion and Generation</h2>
where the canonical should be:
  <h2 id="22-7-5-fusion-and-generation">22.7.5 Fusion and Generation</h2>

Strategy: for any heading id matching "A-B-A-B-C-slug" where the first
four components have A==A AND B==B, strip the duplicate prefix from
both the id and the visible text.

ROOT CAUSE 2 — 75 tables have an adjacent <figcaption> labeled "Figure"
when the book policy is "Table X.Y.Z" for table captions. Convert
"Figure X.Y.Z" → "Table X.Y.Z" when the figcaption is attached to a
<table>.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}


def fix_double_prefix_headings(text: str) -> tuple[str, int]:
    """Strip A-B-A-B-C- → A-B-C- in IDs and A.B.A.B.C → A.B.C in visible text.
    Also handle 5-deep variants (A-B-A-B-C-D)."""
    n = 0

    def rewrite_h(m):
        nonlocal n
        tag = m.group(1)
        h_id = m.group(2)
        visible = m.group(3)
        rest = m.group(4)
        # id parts
        parts = h_id.split('-')
        if (len(parts) >= 5 and parts[0].isdigit() and parts[1].isdigit()
                and parts[2] == parts[0] and parts[3] == parts[1]):
            new_id = '-'.join([parts[0], parts[1]] + parts[4:])
        else:
            new_id = h_id

        # visible: "A.B.A.B.C..." → "A.B.C..."
        vis_m = re.match(r'^(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+(?:\.\d+)?)(\s|$)', visible)
        if vis_m and vis_m.group(1) == vis_m.group(3) and vis_m.group(2) == vis_m.group(4):
            new_vis = f'{vis_m.group(1)}.{vis_m.group(2)}.{vis_m.group(5)}'
            # Preserve any trailing space or what follows
            new_vis_full = new_vis + visible[vis_m.end(5):]
        else:
            new_vis_full = visible

        if new_id != h_id or new_vis_full != visible:
            n += 1
        return f'<{tag} id="{new_id}">{new_vis_full}{rest}</{tag}>'

    text = re.sub(
        r'<(h[234])\s+id="([^"]+)">(\d+\.\d+\.\d+\.\d+\.\d+(?:\.\d+)?)([^<]*)</\1>',
        rewrite_h,
        text,
    )

    # Also fix same-page anchor references that point at the old double-prefix IDs
    def rewrite_anchor(m):
        nonlocal n
        prefix = m.group(1)
        anchor = m.group(2)
        parts = anchor.split('-')
        if (len(parts) >= 5 and parts[0].isdigit() and parts[1].isdigit()
                and parts[2] == parts[0] and parts[3] == parts[1]):
            new_anchor = '-'.join([parts[0], parts[1]] + parts[4:])
            n += 1
            return f'{prefix}#{new_anchor}'
        return m.group(0)

    text = re.sub(
        r'(href=")#(\d+-\d+-\d+-\d+-\d+(?:-[^"]+)?)',
        rewrite_anchor,
        text,
    )

    return text, n


def fix_table_figure_captions(text: str) -> tuple[str, int]:
    """For each <table>...</table>, if there is an adjacent <figcaption> saying
    "Figure X.Y.Z", convert to "Table X.Y.Z"."""
    n = 0
    # Iterate table positions
    out = text
    new_text_parts = []
    last_end = 0
    for m in re.finditer(r'<table[\s\S]*?</table>', out):
        new_text_parts.append(out[last_end:m.end()])
        # Look at the next ~400 chars after the table for a figcaption
        rest = out[m.end():m.end() + 400]
        fc_m = re.search(r'(<figcaption[^>]*>)(\s*)(?:<strong>)?Figure(\s*\d[\d.]*)', rest)
        if fc_m:
            # Replace "Figure" with "Table" only inside this figcaption
            # Compute absolute position
            abs_start = m.end() + fc_m.start()
            abs_end = m.end() + fc_m.end()
            new_text_parts[-1] = (
                new_text_parts[-1] + out[m.end():abs_start]
                + fc_m.group(1) + fc_m.group(2)
                + ('<strong>' if '<strong>' in fc_m.group(0) else '')
                + 'Table' + fc_m.group(3)
            )
            last_end = abs_end
            n += 1
        else:
            last_end = m.end()
    new_text_parts.append(out[last_end:])
    return ''.join(new_text_parts), n


def main():
    n_files_hdr = 0
    n_files_tbl = 0
    n_hdr_fixed = 0
    n_tbl_fixed = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text

        text, hdr_n = fix_double_prefix_headings(text)
        if hdr_n > 0:
            n_files_hdr += 1
            n_hdr_fixed += hdr_n

        text, tbl_n = fix_table_figure_captions(text)
        if tbl_n > 0:
            n_files_tbl += 1
            n_tbl_fixed += tbl_n

        if text != orig:
            p.write_text(text, encoding='utf-8')

    print(f'Double-prefix headings fixed: {n_hdr_fixed} headings in {n_files_hdr} files')
    print(f'Table captions converted Figure→Table: {n_tbl_fixed} captions in {n_files_tbl} files')


if __name__ == '__main__':
    main()
