"""Find redesigned SVGs whose book PNG is older than the redesign — i.e., never wired."""
from pathlib import Path
ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
SVG_DIR = ROOT / 'KDP/diagrams/svg'

svgs = sorted(SVG_DIR.glob('*.svg'))
gaps = []
for svg in svgs:
    base = svg.stem
    matches = list(ROOT.rglob(f'{base}.png'))
    matches = [m for m in matches if 'KDP' not in m.parts and 'source_fix_backups' not in m.parts]
    for m in matches:
        svg_png = SVG_DIR / f'{base}.png'
        if not svg_png.exists():
            continue
        if m.stat().st_mtime < svg_png.stat().st_mtime - 60:
            sep = chr(92)
            gaps.append((svg.name, str(m.relative_to(ROOT)).replace(sep, '/')))

print(f'Found {len(gaps)} gaps (book PNG older than redesign):')
for s, d in gaps:
    print(f'  {s}  ->  {d}')
