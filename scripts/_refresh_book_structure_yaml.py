"""Refresh book_structure.yaml from current disk state.

Run this after any structural change to bring the manifest back in sync.
The next restructure's structure_diff.py compares against this manifest.

Idempotent: running twice on a clean state produces identical output.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print('ERROR: pyyaml not installed', file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]

ROMAN_MAP = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII',
             8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII', 13: 'XIII',
             14: 'XIV', 15: 'XV', 16: 'XVI', 17: 'XVII', 18: 'XVIII',
             19: 'XIX', 20: 'XX'}


def slug_from_dir(dirname, prefix):
    m = re.match(rf'{prefix}-(\d+)-(.+)$', dirname)
    return (int(m.group(1)), m.group(2)) if m else (None, None)


def get_h1(p):
    if not p.exists(): return ''
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    if not m: return ''
    t = m.group(1).strip()
    t = re.sub(r'^Chapter\s+\d+\s*:?\s*', '', t)
    return t.replace('&amp;', '&').replace('&quot;', '"').replace('&apos;', "'")


def get_part_title(idx):
    if not idx.exists(): return ''
    text = idx.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>Part [IVXLCDM]+:\s*([^<]+)</h1>', text)
    if m: return m.group(1).strip().replace('&amp;', '&')
    return ''


def get_subtitle(idx):
    if not idx.exists(): return ''
    text = idx.read_text(encoding='utf-8')
    m = re.search(r'<p class="chapter-subtitle">([^<]+)</p>', text)
    if m: return m.group(1).strip()
    return ''


def build():
    book = {
        'book': {
            'title': 'Building Conversational AI with LLMs and Agents',
            'edition': 'Fifteenth Edition',
            'year': 2026,
        },
        'parts': [],
    }

    for part_dir in sorted(ROOT.glob('part-*/'),
                           key=lambda p: slug_from_dir(p.name, 'part')[0] or 999):
        pnum, pslug = slug_from_dir(part_dir.name, 'part')
        if pnum is None: continue
        part_entry = {
            'num': pnum,
            'roman': ROMAN_MAP.get(pnum, str(pnum)),
            'slug': pslug,
            'title': get_part_title(part_dir / 'index.html'),
            'subtitle': get_subtitle(part_dir / 'index.html') or None,
            'opener_image': 'images/part-opener.png',
            'chapters': [],
        }

        for mod_dir in sorted(part_dir.glob('module-*/'),
                              key=lambda p: slug_from_dir(p.name, 'module')[0] or 999):
            cnum, cslug = slug_from_dir(mod_dir.name, 'module')
            if cnum is None: continue
            ch_entry = {
                'num': cnum,
                'slug': cslug,
                'title': get_h1(mod_dir / 'index.html'),
                'subtitle': get_subtitle(mod_dir / 'index.html') or None,
                'opener_image': 'images/chapter-opener.png',
                'sections': [],
            }

            for sec in sorted(mod_dir.glob('section-*.html'),
                              key=lambda p: tuple(int(x) for x in re.match(r'section-(\d+)\.(\d+)\.html', p.name).groups())):
                sm = re.match(r'section-(\d+)\.(\d+)\.html', sec.name)
                ch_entry['sections'].append({
                    'num': f'{sm.group(1)}.{sm.group(2)}',
                    'slug': sec.stem,
                    'title': get_h1(sec),
                })

            part_entry['chapters'].append(ch_entry)
        book['parts'].append(part_entry)

    # Appendices
    appendices = []
    for ap_dir in sorted((ROOT / 'appendices').glob('appendix-*/'), key=lambda p: p.name):
        m = re.match(r'appendix-([a-z])-(.+)$', ap_dir.name)
        if not m: continue
        letter = m.group(1).upper()
        title = get_h1(ap_dir / 'index.html')
        title = re.sub(rf'^Appendix\s+{letter}\s*:?\s*', '', title, flags=re.IGNORECASE)
        appendices.append({
            'letter': letter,
            'slug': m.group(2),
            'title': title,
        })
    book['appendices'] = {'group': 'appendices', 'items': appendices}

    return book


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='book_structure.yaml',
                    help='Output yaml path (default: book_structure.yaml)')
    ap.add_argument('--dry-run', action='store_true',
                    help='Print to stdout, don\'t write')
    args = ap.parse_args()

    book = build()
    output = yaml.safe_dump(book, sort_keys=False, allow_unicode=True, width=120)
    if args.dry_run:
        # stdout may be cp1252 on Windows; write bytes directly
        sys.stdout.buffer.write(output.encode('utf-8'))
    else:
        (ROOT / args.out).write_text(output, encoding='utf-8')
        n_parts = len(book['parts'])
        n_ch = sum(len(p['chapters']) for p in book['parts'])
        n_sec = sum(len(c['sections']) for p in book['parts'] for c in p['chapters'])
        n_ap = len(book['appendices']['items'])
        print(f'Refreshed {args.out}: {n_parts} parts, {n_ch} chapters, '
              f'{n_sec} sections, {n_ap} appendices')


if __name__ == '__main__':
    sys.exit(main() or 0)
