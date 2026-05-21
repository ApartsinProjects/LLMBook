"""Wave 42: Add width/height attributes to <img> tags by probing actual image
files on disk. Prevents CLS (Cumulative Layout Shift) on initial page load.

For each <img> without both width= and height=:
  1. Resolve the src relative to the file's directory
  2. Read dimensions from disk (PNG via Pillow, SVG via XML parse)
  3. Inject width="W" height="H" before the closing >

Uses Pillow for raster images. For SVG, parses viewBox or width/height attrs.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

IMG_RE = re.compile(r'<img\b([^>]*?)/?>', re.IGNORECASE)
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']')
WIDTH_RE = re.compile(r'\bwidth\s*=\s*["\']?[^"\'\s>]+')
HEIGHT_RE = re.compile(r'\bheight\s*=\s*["\']?[^"\'\s>]+')

# Cache: src absolute path -> (width, height) or None
DIM_CACHE: dict[Path, tuple[int, int] | None] = {}


def parse_svg_dims(path: Path) -> tuple[int, int] | None:
    """Parse SVG viewBox or width/height attrs."""
    try:
        # Read just the opening svg tag region
        text = path.read_text(encoding='utf-8', errors='ignore')[:4000]
        # Find <svg ...> tag
        m = re.search(r'<svg\b[^>]*>', text, re.IGNORECASE | re.DOTALL)
        if not m:
            return None
        svg_tag = m.group()
        # Prefer width/height attrs (explicit pixel dimensions)
        w_match = re.search(r'\bwidth\s*=\s*["\']?(\d+(?:\.\d+)?)(?:px)?["\']?', svg_tag, re.IGNORECASE)
        h_match = re.search(r'\bheight\s*=\s*["\']?(\d+(?:\.\d+)?)(?:px)?["\']?', svg_tag, re.IGNORECASE)
        if w_match and h_match:
            return (int(float(w_match.group(1))), int(float(h_match.group(1))))
        # Fall back to viewBox
        vb_match = re.search(r'\bviewBox\s*=\s*["\']([-\d.\s]+)["\']', svg_tag, re.IGNORECASE)
        if vb_match:
            parts = vb_match.group(1).split()
            if len(parts) == 4:
                w = float(parts[2]) - float(parts[0])
                h = float(parts[3]) - float(parts[1])
                return (int(w), int(h))
    except Exception:
        pass
    return None


def get_dims(path: Path) -> tuple[int, int] | None:
    if path in DIM_CACHE:
        return DIM_CACHE[path]
    result = None
    try:
        if not path.exists():
            DIM_CACHE[path] = None
            return None
        ext = path.suffix.lower()
        if ext == '.svg':
            result = parse_svg_dims(path)
        elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
            with Image.open(path) as im:
                result = im.size  # (w, h)
    except Exception:
        result = None
    DIM_CACHE[path] = result
    return result


def resolve_src(html_path: Path, src: str) -> Path | None:
    """Resolve image src (which can be relative path or absolute book path) to disk."""
    src = unquote(src.strip())
    if src.startswith(('http://', 'https://', 'data:')):
        return None
    if src.startswith('/'):
        # Absolute from book root
        return ROOT / src.lstrip('/')
    # Strip query string and fragment
    src = src.split('?')[0].split('#')[0]
    if not src:
        return None
    return (html_path.parent / src).resolve()


def fix_html(html_path: Path) -> tuple[int, int, int]:
    """Returns (n_fixed, n_missing_file, n_other_skip)."""
    text = html_path.read_text(encoding='utf-8')
    orig = text
    n_fixed = 0
    n_missing = 0
    n_other = 0

    def replace_img(m: re.Match) -> str:
        nonlocal n_fixed, n_missing, n_other
        attrs = m.group(1)
        full = m.group()
        # Skip if already has width AND height
        has_w = bool(WIDTH_RE.search(attrs))
        has_h = bool(HEIGHT_RE.search(attrs))
        if has_w and has_h:
            return full
        src_m = SRC_RE.search(attrs)
        if not src_m:
            n_other += 1
            return full
        src = src_m.group(1)
        if src.startswith(('http://', 'https://', 'data:')):
            n_other += 1
            return full
        abs_path = resolve_src(html_path, src)
        if not abs_path or not abs_path.exists():
            n_missing += 1
            return full
        dims = get_dims(abs_path)
        if not dims:
            n_other += 1
            return full
        w, h = dims
        # Inject width/height. Where to put them: after src attribute for neatness.
        new_attrs = attrs
        if not has_w:
            new_attrs = re.sub(
                r'(src=["\'][^"\']+["\'])',
                f'\\1 width="{w}"',
                new_attrs,
                count=1,
            )
        if not has_h:
            # Insert after the width we just added (or after src if width preexisted)
            if not has_w:
                new_attrs = re.sub(
                    f'(width="{w}")',
                    f'\\1 height="{h}"',
                    new_attrs,
                    count=1,
                )
            else:
                new_attrs = re.sub(
                    r'(src=["\'][^"\']+["\'])',
                    f'\\1 height="{h}"',
                    new_attrs,
                    count=1,
                )
        n_fixed += 1
        # Reconstruct preserving self-closing slash if present
        closing = '/>' if full.rstrip('>').endswith('/') else '>'
        return f'<img{new_attrs}{closing}'

    text = IMG_RE.sub(replace_img, text)

    if text != orig:
        html_path.write_text(text, encoding='utf-8')
    return n_fixed, n_missing, n_other


def main():
    total_fixed = 0
    total_missing = 0
    total_other = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        f, m, o = fix_html(p)
        total_fixed += f
        total_missing += m
        total_other += o
        if f > 0:
            files_touched += 1
    print(f'<img> dimensions added: {total_fixed}')
    print(f'<img> with missing source file: {total_missing}')
    print(f'<img> skipped (no src / data URI / read error): {total_other}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
