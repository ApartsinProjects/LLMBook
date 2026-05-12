"""v6.36: Build a catalogue of every figure in the book.

For each figure (figure ID like 6.3.2 or 23.2.1):
  - Source generator (matplotlib script, mermaid .mmd, Gemini-generated PNG)
  - File path of the rendered image
  - Caption text
  - Alt text
  - Containing section
  - SVG sibling (if any)

Output: KDP/validation/figure_catalogue.csv

This is the source of truth for re-running diagrams when the diagram skill
or design conventions change. Future "regenerate every chart" passes can
iterate over this CSV.
"""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'KDP' / 'validation' / 'figure_catalogue.csv'

ALL_HTML = sorted(list(ROOT.glob('part-*/module-*/section-*.html')) +
                  list(ROOT.glob('part-*/module-*/index.html')) +
                  list(ROOT.glob('appendices/appendix-*/section-*.html')) +
                  list(ROOT.glob('appendices/appendix-*/index.html')))


def find_generator(image_path: Path) -> str | None:
    """Look for a sibling .mmd, or matching gen_figure_X_Y_Z.py."""
    if not image_path:
        return None
    img_dir = image_path.parent
    stem = image_path.stem
    # Mermaid sibling
    mmd = img_dir / f'{stem}.mmd'
    if mmd.exists():
        return str(mmd.relative_to(ROOT)).replace('\\', '/')
    # matplotlib generator: scripts/svg_to_matplotlib/gen_figure_<digits>.py
    m = re.match(r'fig-(\d+)\.(\d+)\.(\d+)', stem)
    if m:
        c, s, n = m.groups()
        candidate = ROOT / 'scripts' / 'svg_to_matplotlib' / f'gen_figure_{c}_{s}_{n}.py'
        if candidate.exists():
            return str(candidate.relative_to(ROOT)).replace('\\', '/')
    # Gemini original — no generator script, the PNG IS the source
    if (img_dir / stem).with_suffix('.png').exists() and not stem.startswith('fig-'):
        return f'gemini:{img_dir.relative_to(ROOT)}/{stem}.png'.replace('\\', '/')
    return None


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in ALL_HTML:
        text = p.read_text(encoding='utf-8', errors='replace')
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        # Match every <img> referencing images/ — we will look for adjacent
        # caption context.
        for m in re.finditer(r'<img\b[^>]*src="(images/[^"]+)"[^>]*?(?:alt="([^"]*)")?[^>]*/?>', text):
            src = m.group(1)
            alt = m.group(2) or ''
            # Look ahead 600 chars for a figcaption or "Figure X.Y" pattern
            tail = text[m.end():m.end() + 600]
            cap_m = re.search(r'<figcaption[^>]*>(.+?)</figcaption>', tail, re.DOTALL)
            if cap_m:
                caption = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip()
            else:
                # Look for nearby Figure label in alt, or scan further
                label_in_tail = re.search(
                    r'<strong>Figure\s+([A-Z]?\d+\.\d+(?:\.\d+)?)</strong>',
                    tail,
                )
                caption = ''
            label_m = re.match(r'Figure\s+([A-Z]?\d+\.\d+(?:\.\d+)?)', caption)
            label = label_m.group(1) if label_m else ''
            img_path = (p.parent / src).resolve()
            img_disk = str(img_path.relative_to(ROOT)).replace('\\', '/') if img_path.exists() else ''
            generator = find_generator(img_path) if img_path.exists() else None
            rows.append({
                'figure_label': label,
                'section': rel,
                'image_path': img_disk,
                'image_kind': image_kind(img_path),
                'generator': generator or '',
                'alt_text': alt[:200],
                'caption': caption[:400],
            })

    with OUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
                           ['figure_label', 'section', 'image_path', 'image_kind',
                            'generator', 'alt_text', 'caption'])
        w.writeheader()
        w.writerows(rows)
    print(f'Catalogued {len(rows)} figures -> {OUT}')

    # Quick stats
    from collections import Counter
    kinds = Counter(r['image_kind'] for r in rows)
    has_gen = sum(1 for r in rows if r['generator'])
    print(f'\nBy image kind:')
    for k, v in kinds.most_common():
        print(f'  {k}: {v}')
    print(f'\nFigures with a regeneration source: {has_gen} / {len(rows)}')
    return 0


def image_kind(p: Path) -> str:
    if not p.exists():
        return 'missing'
    name = p.name
    if name.endswith('.svg'):
        return 'svg'
    if name.startswith('fig-') and name.endswith('.png'):
        # could be matplotlib or mermaid
        if (p.parent / (p.stem + '.mmd')).exists():
            return 'mermaid-png'
        return 'matplotlib-png'
    if name.endswith('.png') or name.endswith('.jpg'):
        return 'gemini-png'
    return 'other'


if __name__ == '__main__':
    sys.exit(main())
