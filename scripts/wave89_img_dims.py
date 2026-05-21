"""Wave 89: Add width/height to <img> tags missing dimensions (18 cases).

Wave 42 used PIL to add img dims book-wide. The current 18 residual
cases were missed because the wave's regex couldn't parse <img> tags
whose alt attribute contained HTML/markup (e.g., alt="<strong>Figure
X.Y.Z</strong>: ..."). With the MISSING_IMG_DIMS plugin's regex fix
(commit 87b29bb9 cluster), the actual src is now correctly extracted;
this wave runs PIL on each src and writes width=N height=M into the
<img> tag.

For SVG, we use a small inline parser (read width="..." height="..."
from the SVG root tag, falling back to viewBox).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    from PIL import Image
except ImportError:
    print("PIL not installed; run: pip install Pillow")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]

# Same img-tag regex as the plugin: respects quote boundaries.
IMG_RE = re.compile(
    r'''<img\b((?:[^>"']|"[^"]*"|'[^']*')*)/?>''',
    re.IGNORECASE | re.DOTALL,
)
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']')
VIEWBOX_RE = re.compile(r'viewBox=["\'][^"\']*?(\d+)\s+(\d+)["\']', re.IGNORECASE)
SVG_W_RE = re.compile(r'\bwidth=["\']?(\d+)', re.IGNORECASE)
SVG_H_RE = re.compile(r'\bheight=["\']?(\d+)', re.IGNORECASE)


def get_image_dims(img_path: Path):
    """Return (width, height) or None if unreadable."""
    if not img_path.exists():
        return None
    suffix = img_path.suffix.lower()
    if suffix == ".svg":
        try:
            head = img_path.read_text(encoding="utf-8", errors="replace")[:4096]
        except Exception:
            return None
        # Try width/height attrs on the <svg> root first
        svg_tag = re.search(r'<svg\b([^>]*)>', head, re.IGNORECASE)
        if not svg_tag:
            return None
        attrs = svg_tag.group(1)
        wm = SVG_W_RE.search(attrs)
        hm = SVG_H_RE.search(attrs)
        if wm and hm:
            return int(wm.group(1)), int(hm.group(1))
        # Fall back to viewBox last two numbers
        vb = re.search(r'viewBox=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if vb:
            parts = re.findall(r'\d+', vb.group(1))
            if len(parts) == 4:
                return int(parts[2]), int(parts[3])
        return None
    # Raster image: use PIL
    try:
        with Image.open(img_path) as im:
            return im.width, im.height
    except Exception as e:
        print(f"  ! PIL failed on {img_path}: {e}")
        return None


def resolve_src(file_path: Path, src: str):
    """Resolve a relative src to an absolute Path."""
    if src.startswith("/"):
        # Site-absolute (rare in this book)
        return ROOT / src.lstrip("/")
    # Relative to the HTML file's directory
    return (file_path.parent / src).resolve()


def fix_file(p: Path) -> int:
    html = p.read_text(encoding="utf-8")
    new_chunks = []
    last = 0
    n = 0
    for m in IMG_RE.finditer(html):
        attrs = m.group(1)
        has_width = "width=" in attrs
        has_height = "height=" in attrs
        if has_width and has_height:
            continue
        src_m = SRC_RE.search(attrs)
        if not src_m:
            continue
        src = src_m.group(1)
        img_path = resolve_src(p, src)
        dims = get_image_dims(img_path)
        if not dims:
            continue
        w, h = dims
        new_attrs = attrs
        if not has_width:
            new_attrs += f' width="{w}"'
        if not has_height:
            new_attrs += f' height="{h}"'
        new_tag = f"<img{new_attrs}/>"
        new_chunks.append(html[last:m.start()])
        new_chunks.append(new_tag)
        last = m.end()
        n += 1
    if n == 0:
        return 0
    new_chunks.append(html[last:])
    p.write_text("".join(new_chunks), encoding="utf-8")
    return n


def main():
    n_files = 0
    n_imgs = 0
    skip = {"node_modules", "KDP", "agents", ".git", "_archive",
            "build", "vendor", "templates", "pagefind", ".book-update"}
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & skip:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_imgs += n
            print(f"  + {p.relative_to(ROOT)}: {n} img(s)")
    print(f"\nFiles touched: {n_files}, images updated: {n_imgs}")


if __name__ == "__main__":
    main()
