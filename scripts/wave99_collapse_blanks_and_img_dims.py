"""Wave 99: Collapse EXCESSIVE_BLANKS and add MISSING_IMG_DIMS.

Two cheap, safe auto-fixes:
  1. Collapse runs of >= 3 consecutive blank lines down to 1 blank line.
     The audit's EXCESSIVE_BLANKS plugin flags 3+ blank lines; collapsing
     to 1 keeps paragraph breaks while removing visual noise.
  2. Add width / height attributes to <img> tags inside <figure
     class="illustration"> that lack them. Reads the actual file
     dimensions where possible (jpg/png/svg). Without explicit width
     and height, the browser reflows the page when the image loads,
     causing CLS (Cumulative Layout Shift).
"""
import re
import sys
import struct
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

BLANK_RE = re.compile(r'(?:^[ \t]*\n){3,}', re.MULTILINE)


def fix_blanks(text: str) -> tuple[str, int]:
    """Collapse 3+ blank lines into 1 blank line (== 2 \\n)."""
    n = 0
    new_text, n = BLANK_RE.subn("\n", text)
    return new_text, n


IMG_RE = re.compile(
    r'<img\s+([^>]*?)/?>',
    re.IGNORECASE | re.DOTALL,
)


def get_image_dims(p: Path) -> tuple[int, int] | None:
    """Return (width, height) for jpg / png / svg, or None."""
    try:
        with p.open("rb") as f:
            head = f.read(32)
            if head.startswith(b"\x89PNG\r\n\x1a\n"):
                # PNG: width and height at offset 16, big-endian
                w, h = struct.unpack(">II", head[16:24])
                return w, h
            if head.startswith(b"\xff\xd8"):
                # JPEG: scan SOF segments
                with p.open("rb") as f2:
                    f2.read(2)
                    while True:
                        b = f2.read(1)
                        while b and b != b"\xff":
                            b = f2.read(1)
                        if not b:
                            return None
                        marker = f2.read(1)
                        while marker == b"\xff":
                            marker = f2.read(1)
                        if marker in (b"\xc0", b"\xc1", b"\xc2"):
                            f2.read(3)
                            h = struct.unpack(">H", f2.read(2))[0]
                            w = struct.unpack(">H", f2.read(2))[0]
                            return w, h
                        seg_len = struct.unpack(">H", f2.read(2))[0]
                        f2.read(seg_len - 2)
        # SVG: parse the root element
        if p.suffix.lower() == ".svg":
            txt = p.read_text(encoding="utf-8", errors="ignore")[:2000]
            wm = re.search(r'\bwidth=["\'](\d+)', txt)
            hm = re.search(r'\bheight=["\'](\d+)', txt)
            if wm and hm:
                return int(wm.group(1)), int(hm.group(1))
            vb = re.search(r'viewBox=["\']\s*[\d.-]+\s+[\d.-]+\s+([\d.]+)\s+([\d.]+)', txt)
            if vb:
                return int(float(vb.group(1))), int(float(vb.group(2)))
    except (OSError, struct.error):
        return None
    return None


def fix_img_dims(text: str, doc_path: Path) -> tuple[str, int]:
    """Add width/height to <img> tags missing them."""
    n = 0

    def replace(m: re.Match) -> str:
        nonlocal n
        attrs = m.group(1)
        has_w = re.search(r'\bwidth=', attrs, re.IGNORECASE)
        has_h = re.search(r'\bheight=', attrs, re.IGNORECASE)
        if has_w and has_h:
            return m.group(0)
        src_m = re.search(r'\bsrc=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if not src_m:
            return m.group(0)
        src = src_m.group(1)
        # Resolve relative to doc
        src_path = (doc_path.parent / src).resolve()
        if not src_path.exists():
            return m.group(0)
        dims = get_image_dims(src_path)
        if not dims:
            return m.group(0)
        w, h = dims
        extra = ""
        if not has_w:
            extra += f' width="{w}"'
        if not has_h:
            extra += f' height="{h}"'
        n += 1
        return f"<img {attrs.rstrip()}{extra}/>"

    new_text = IMG_RE.sub(replace, text)
    return new_text, n


def main():
    n_files_b = n_files_d = 0
    n_blank = n_dims = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding="utf-8")
        original = text

        text, b = fix_blanks(text)
        text, d = fix_img_dims(text, p)

        if text != original:
            p.write_text(text, encoding="utf-8")
            if b:
                n_files_b += 1
                n_blank += b
            if d:
                n_files_d += 1
                n_dims += d
            print(f"  + {p.relative_to(ROOT)}: blanks={b}, dims={d}")
    print(f"\nBlank-collapse: {n_blank} runs in {n_files_b} files. "
          f"Image-dims: {n_dims} adds in {n_files_d} files.")


if __name__ == "__main__":
    main()
