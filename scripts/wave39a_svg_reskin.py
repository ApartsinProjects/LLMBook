"""Wave 39a: Re-skin Ch 41/56/61 tile-map SVGs to book palette + sans-serif.

The 10 "tile-map template" SVGs in Ch 41/56/61 share an off-book palette:
  #1a2b5c (navy)    #2f6b3a (green)    #5d3c8c (purple)
  #b87000 (amber)   #a73838 (red)      #666 (gray)
  #f7f7f2 (cream background)   Georgia, serif

Re-skin to canonical book palette:
  #1a4078 (book navy)   #1f7a3a (book green)   #6a1b9a (book purple)
  #a67c1a (book amber)  #bf360c (book red)     #555 (book gray)
  #ffffff (white background)  Segoe UI, system-ui, sans-serif

Affected files (per Wave 25 audit):
  section-41.1.html, 41.2.html, 41.3.html, 41.4.html,
  section-56.1.html, section-61.1.html, 61.2.html, 61.3.html, 61.4.html, 61.5.html,
  section-37.3.html (Material flat palette, third variant)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Tile-map palette -> book palette
TILE_PALETTE_MAP = {
    '#1a2b5c': '#1a4078',  # navy
    '#2f6b3a': '#1f7a3a',  # green
    '#5d3c8c': '#6a1b9a',  # purple
    '#b87000': '#a67c1a',  # amber
    '#a73838': '#bf360c',  # red
    '#f7f7f2': '#ffffff',  # background
}

# Material flat palette (section-37.3) -> book palette
MATERIAL_PALETTE_MAP = {
    '#3498db': '#1a4078',  # blue -> navy
    '#8e44ad': '#6a1b9a',  # purple
    '#27ae60': '#1f7a3a',  # green
    '#f39c12': '#a67c1a',  # amber
    '#1a1a2e': '#0d3b66',  # dark
}

FONT_MAP = {
    'Georgia, serif': 'Segoe UI, system-ui, sans-serif',
    'font-family="Georgia"': 'font-family="Segoe UI, system-ui, sans-serif"',
}


# Targeted file list (mechanical sweep limits damage; only known tile-map files)
TARGETS = [
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.1.html',
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.2.html',
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.3.html',
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.4.html',
    'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html',
    'part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html',
    'part-12-llm-systems-at-scale/module-61-scale-tools/section-61.2.html',
    'part-12-llm-systems-at-scale/module-61-scale-tools/section-61.3.html',
    'part-12-llm-systems-at-scale/module-61-scale-tools/section-61.4.html',
    'part-12-llm-systems-at-scale/module-61-scale-tools/section-61.5.html',
    'part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html',
]


def fix(text: str, palette: dict, fonts: dict) -> tuple[str, int]:
    n = 0
    for old, new in palette.items():
        new_text = text.replace(old, new)
        if new_text != text:
            n += text.count(old)
        text = new_text
    for old, new in fonts.items():
        new_text = text.replace(old, new)
        if new_text != text:
            n += text.count(old)
        text = new_text
    return text, n


def main():
    n_total = 0
    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            print(f'  SKIP (missing): {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        # Use Material palette for 37.3, tile-map palette for others
        palette = MATERIAL_PALETTE_MAP if 'module-37' in rel else TILE_PALETTE_MAP
        new, n = fix(text, palette, FONT_MAP)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_total += n
            print(f'  {rel}: {n} palette substitutions')
    print(f'\nTotal: {n_total} SVG palette substitutions across {len(TARGETS)} files')


if __name__ == '__main__':
    main()
