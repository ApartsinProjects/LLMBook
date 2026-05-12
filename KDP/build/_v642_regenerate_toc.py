"""v6.42: Regenerate the detailed ToC entries from disk truth.

The 157 ToC label/href mismatches are off-by-one and stale-target bugs in
toc.html (e.g. label "13.4" but href section-13.3.html). Rather than fix
each individually, regenerate every <div class="dense-sections"> row by
walking the actual filesystem and using each section's H1 as its label.

The page structure is preserved (parts, chapter rows, etc.). Only the
<div class="dense-sections"> rows that list sections are rewritten.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOC = ROOT / 'toc.html'

PARTS_ORDER = [
    'part-1-foundations', 'part-2-understanding-llms', 'part-3-working-with-llms',
    'part-4-training-adapting', 'part-5-retrieval-conversation', 'part-6-agentic-ai',
    'part-7-multimodal-applications', 'part-8-evaluation-production',
    'part-9-safety-strategy', 'part-10-frontiers', 'part-11-idea-to-product',
]


def chap_num(d):
    m = re.match(r'module-(\d+)-', d.name)
    return int(m.group(1)) if m else 9999


def section_key(p):
    m = re.match(r'section-(\d+)\.(\d+)(?:\.(\d+))?', p.stem)
    if not m:
        return (9999, 9999, 9999)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)) if m.group(3) else 0)


def get_h1(p):
    text = p.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<h1[^>]*>(.+?)</h1>', text, re.DOTALL)
    if not m:
        return p.stem
    return re.sub(r'<[^>]+>', '', m.group(1)).strip()


def section_label(p):
    """Return 'X.Y' for section-X.Y.html."""
    m = re.match(r'section-(\d+)\.(\d+)', p.stem)
    if m:
        return f'{m.group(1)}.{m.group(2)}'
    return p.stem


def section_href_from_chapter(part_dir: str, mod_dir: str, sec: Path) -> str:
    """Path FROM toc.html TO section page."""
    return f'{part_dir}/{mod_dir}/{sec.name}'


def main() -> int:
    text = TOC.read_text(encoding='utf-8')

    # For each chapter dense-sections block, regenerate its content.
    # A chapter row looks like:
    #   <div class="dense-chapter"><span class="dense-ch-num">Ch NN</span> <a href="..."> Title</a></div>
    #   <div class="dense-sections">...sections list with separators...</div>
    #
    # We find each dense-chapter row, identify the chapter via the href,
    # then walk the chapter's directory and rewrite the FOLLOWING dense-sections
    # block.

    chap_pat = re.compile(
        r'(<div class="dense-chapter">'
        r'<span class="dense-ch-num">Ch\s+(\d+)</span>\s*'
        r'<a href="(part-\d+-[^"]+/module-(\d+)-[^"]+)/index\.html">[^<]+</a>'
        r'</div>)'
    )

    new_text = text
    rewrites = 0
    cursor = 0
    parts = []
    for m in chap_pat.finditer(text):
        chap_label = m.group(2)
        path_prefix = m.group(3)  # part-X-name/module-NN-name
        # Find the matching dense-sections block immediately after this chapter row
        after = text[m.end():]
        ds_m = re.match(r'\s*\n?<div class="dense-sections">(.*?)</div>', after, re.DOTALL)
        if not ds_m:
            parts.append(text[cursor:m.end()])
            cursor = m.end()
            continue
        # Build new dense-sections content from disk
        chap_dir = ROOT / path_prefix
        if not chap_dir.exists():
            parts.append(text[cursor:m.end()])
            cursor = m.end()
            continue
        sections = sorted(chap_dir.glob('section-*.html'), key=section_key)
        if not sections:
            parts.append(text[cursor:m.end()])
            cursor = m.end()
            continue
        anchors = []
        for sec in sections:
            label = section_label(sec)
            title = get_h1(sec)
            href = f'{path_prefix}/{sec.name}'
            anchors.append(f'<a href="{href}">{label} {title}</a>')
        new_block = '<div class="dense-sections">' + ' &middot; '.join(anchors) + '</div>'
        # Stitch: text up to end of dense-chapter row + newline + new_block
        parts.append(text[cursor:m.end()])
        parts.append('\n')
        parts.append(new_block)
        cursor = m.end() + ds_m.end()
        rewrites += 1
    parts.append(text[cursor:])
    new_text = ''.join(parts)

    if new_text == text:
        print('No changes')
        return 0
    TOC.write_text(new_text, encoding='utf-8')
    print(f'Regenerated {rewrites} dense-sections blocks in toc.html')
    return 0


if __name__ == '__main__':
    sys.exit(main())
