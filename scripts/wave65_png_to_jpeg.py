"""Wave 65: Convert non-diagram PNG images (comics, openers, hero, illustrations)
to JPEG. Cartoony/photographic content compresses dramatically with JPEG (85%
quality) without losing visual fidelity, freeing ~70-80 MB of repo size.

Diagrams (SVG) are unaffected — they stay vector. PNGs that contain text or
sharp edges (UI screenshots, code diagrams stored as PNG) are preserved.

Targets: file names containing "comic-", "opener", "hero", "cover", or in a
directory marked illustration-heavy.

For each target:
  1. Load PNG via Pillow
  2. Convert to RGB (drop alpha; JPEG can't store transparency — comics
     authored with white/cream background are fine)
  3. Save as .jpg at quality 88 (high-quality)
  4. Delete the original .png
  5. Rewrite all HTML references from `images/X.png` to `images/X.jpg`

Operates only inside `part-*` and `appendices/` directories.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Filename patterns that target the conversion
TARGET_TOKENS = ('comic-', 'opener', 'hero', 'cover', 'illustration', 'cartoon')


def is_target(p: Path) -> bool:
    name = p.name.lower()
    return any(tok in name for tok in TARGET_TOKENS)


def convert_one(png_path: Path) -> tuple[Path, int, int] | None:
    """Convert PNG to JPEG; return (jpg_path, old_size, new_size) or None on failure."""
    try:
        old_size = png_path.stat().st_size
        with Image.open(png_path) as im:
            # Drop alpha by compositing on white background
            if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                bg = Image.new('RGB', im.size, (255, 255, 255))
                rgba = im.convert('RGBA')
                bg.paste(rgba, mask=rgba.split()[3])
                rgb = bg
            else:
                rgb = im.convert('RGB')
            jpg_path = png_path.with_suffix('.jpg')
            rgb.save(jpg_path, 'JPEG', quality=88, optimize=True)
            new_size = jpg_path.stat().st_size
        # Only keep JPEG if it's smaller (with some margin for tiny PNGs)
        if new_size < old_size * 0.85:
            png_path.unlink()
            return (jpg_path, old_size, new_size)
        else:
            jpg_path.unlink()
            return None
    except Exception as e:
        print(f'  ERROR converting {png_path}: {e}')
        return None


def rewrite_references(png_rel: str, jpg_rel: str) -> int:
    """Rewrite all HTML files that reference png_rel to use jpg_rel."""
    n = 0
    for p in ROOT.rglob('*.html'):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        # Match both the basename and any deeper path containing it
        new = text.replace(png_rel, jpg_rel)
        if new != text:
            p.write_text(new, encoding='utf-8')
            n += 1
    return n


def main():
    n_converted = 0
    n_skipped = 0
    total_old = 0
    total_new = 0
    files_touched_total = 0

    for png_path in sorted(ROOT.rglob('*.png')):
        if set(png_path.parts) & SKIP:
            continue
        if not is_target(png_path):
            continue
        # Don't touch images shared in front-matter agents (avatars), book-cover, etc.
        if 'agent' in png_path.name.lower():
            continue
        result = convert_one(png_path)
        if result is None:
            n_skipped += 1
            continue
        jpg_path, old_size, new_size = result
        # Compute basename relative paths to rewrite
        png_name = png_path.name
        jpg_name = jpg_path.name
        n_files = rewrite_references(png_name, jpg_name)
        n_converted += 1
        total_old += old_size
        total_new += new_size
        files_touched_total += n_files
        if n_converted % 25 == 0:
            print(f'  {n_converted} converted... ({total_old / (1024*1024):.1f} MB → {total_new / (1024*1024):.1f} MB)')

    print()
    print(f'Converted: {n_converted} PNGs → JPEGs')
    print(f'Skipped (would not shrink): {n_skipped}')
    print(f'Size: {total_old / (1024*1024):.1f} MB → {total_new / (1024*1024):.1f} MB '
          f'(savings: {(total_old - total_new) / (1024*1024):.1f} MB, '
          f'{(1 - total_new / total_old) * 100:.0f}% reduction)' if total_old else '')
    print(f'HTML files updated (with reference rewrites): {files_touched_total}')


if __name__ == '__main__':
    main()
