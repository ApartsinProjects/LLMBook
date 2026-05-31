"""Post-build EPUB patch: fix SVG text attributes that KFX rejects.

WHY (field-discovered)
  Mermaid (and other SVG diagram tools) emit SVG <text> elements with:
    1. `font-size="11"` (bare numeric = pixels per SVG spec; KFX wants em/rem)
    2. `font-family="Segoe UI"` (Windows-default proprietary font not in EPUB)

  KFX errors emitted per occurrence:
    E02208 "Font size other than EM or REM not supported"
    E06424 "Required font files not present"

  EPUBCheck does not flag either of these because both are valid SVG.

WHAT THIS FIXES
  - Replaces `font-size="<N>"` and `font-size="<N>px"` with `font-size="<N/16>em"`
  - Replaces `font-family="Segoe UI"` (or any Windows-only font not bundled)
    with `font-family="sans-serif"`
  - Also fixes SVG `style="font-size: Npx"` inline-style variants

Idempotent.

Usage:
  python KDP/build/fix_kfx_svg_text_attrs.py path/to/book.epub
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path


# Fonts unlikely to be present in the EPUB bundle. KFX (Kindle Format X)
# erroring with E06424 ("Required font files not present") fires when any
# font-family token does not resolve to either a generic name or a bundled
# @font-face declaration, EVEN IF the list has a generic fallback last. We
# therefore strip every non-bundled named font from font-family lists.
#
# Map: proprietary name -> safe generic substitute. If a list collapses to
# nothing after stripping, normalize_family() falls back to the substitute
# of the FIRST original item.
PROPRIETARY_FONTS_MAP = {
    # Windows-only / desktop-default fonts
    "Segoe UI":        "sans-serif",
    "Segoe Print":     "sans-serif",
    "Consolas":        "monospace",
    "Calibri":         "sans-serif",
    "Trebuchet MS":    "sans-serif",
    "Lucida Console":  "monospace",
    "MS Gothic":       "sans-serif",
    "Cambria":         "serif",
    "Cambria Math":    "serif",
    # Cross-platform system fonts (commonly listed as CSS fallbacks)
    "Helvetica":       "sans-serif",
    "Helvetica Neue":  "sans-serif",
    "Arial":           "sans-serif",
    "Georgia":         "serif",
    "Times New Roman": "serif",
    "Courier":         "monospace",
    "Courier New":     "monospace",
    "Liberation Mono": "monospace",
}

# Match `font-size="<NUMBER>"` or `font-size="<NUMBER>px"`
FONT_SIZE_ATTR_RE = re.compile(
    r'(font-size=)(["\'])\s*(\d+(?:\.\d+)?)\s*(?:px)?\s*(["\'])',
    re.IGNORECASE,
)
# Match style="...font-size: Npx..." (within style attr)
FONT_SIZE_STYLE_RE = re.compile(
    r'(font-size\s*:\s*)(\d+(?:\.\d+)?)\s*px',
    re.IGNORECASE,
)
# Match `font-family="X"` (SVG attribute form) where X is a font list
FONT_FAMILY_ATTR_RE = re.compile(
    r'(font-family=)(["\'])([^"\']+)(["\'])',
    re.IGNORECASE,
)
# Match `font-family: X, Y, Z` inside CSS declarations (rule body OR inline style).
# Captures the FULL family list value so we can scan it for proprietary names.
#
# Terminators are `;` (declaration end), `}` (rule end), `>` (attribute end in
# inline style="..." within a tag), or `!` (start of `!important`). Quotes
# (single and double) are INTENTIONALLY allowed inside the capture because real
# CSS values look like `font-family: 'Segoe UI', system-ui, sans-serif` and an
# earlier regex that excluded quotes silently skipped every quoted proprietary
# name (5348 Segoe UI / 1265 Cambria Math / 14753 Helvetica slipped through).
FONT_FAMILY_CSS_RE = re.compile(
    r'(font-family\s*:\s*)([^;}>!]+)',
    re.IGNORECASE,
)


def normalize_family(value: str) -> str | None:
    """Rewrite font-family list to remove proprietary fonts.

    Scans ALL items in the comma-separated list (not just the first), drops
    any proprietary entries, and returns the cleaned list. If the cleaned
    list is empty, falls back to the proprietary-to-generic mapping of the
    first item. Returns None if no change is needed.
    """
    items = [s.strip().strip("'\"").strip() for s in value.split(",")]
    items = [s for s in items if s]
    cleaned = [s for s in items if s not in PROPRIETARY_FONTS_MAP]
    if cleaned == items:
        return None  # nothing proprietary; leave alone
    if not cleaned:
        # all items were proprietary; map first item via the substitution table
        cleaned = [PROPRIETARY_FONTS_MAP.get(items[0], "sans-serif")]
    return ", ".join(cleaned)


def patch_xhtml(text: str) -> tuple[str, int, int, int]:
    """Returns (new_text, font_size_attr_fixes, font_size_style_fixes, font_family_fixes)."""
    fs_attr = 0
    fs_style = 0
    ff_attr = 0

    def replace_fs(m: re.Match) -> str:
        nonlocal fs_attr
        val = float(m.group(3))
        em = val / 16
        fs_attr += 1
        return f'{m.group(1)}{m.group(2)}{em:g}em{m.group(4)}'
    text = FONT_SIZE_ATTR_RE.sub(replace_fs, text)

    def replace_fs_style(m: re.Match) -> str:
        nonlocal fs_style
        val = float(m.group(2))
        em = val / 16
        fs_style += 1
        return f'{m.group(1)}{em:g}em'
    text = FONT_SIZE_STYLE_RE.sub(replace_fs_style, text)

    def replace_ff(m: re.Match) -> str:
        nonlocal ff_attr
        value = m.group(3)
        repl = normalize_family(value)
        if repl is None:
            return m.group(0)
        ff_attr += 1
        return f'{m.group(1)}{m.group(2)}{repl}{m.group(4)}'
    text = FONT_FAMILY_ATTR_RE.sub(replace_ff, text)

    # Also fix CSS-form font-family in inline style attributes + stylesheets
    def replace_ff_css(m: re.Match) -> str:
        nonlocal ff_attr
        value = m.group(2)
        repl = normalize_family(value)
        if repl is None:
            return m.group(0)
        ff_attr += 1
        return f'{m.group(1)}{repl}'
    text = FONT_FAMILY_CSS_RE.sub(replace_ff_css, text)

    return text, fs_attr, fs_style, ff_attr


def patch_epub(epub_path: Path) -> dict:
    stats = {"files_scanned": 0, "files_modified": 0,
             "font_size_attr_fixed": 0, "font_size_style_fixed": 0,
             "font_family_fixed": 0}
    tmp = epub_path.with_suffix(epub_path.suffix + ".tmp")
    with zipfile.ZipFile(epub_path, "r") as zin, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename.lower().endswith((".xhtml", ".html", ".svg", ".css")):
                stats["files_scanned"] += 1
                text = data.decode("utf-8", errors="replace")
                new_text, n1, n2, n3 = patch_xhtml(text)
                if new_text != text:
                    stats["files_modified"] += 1
                    stats["font_size_attr_fixed"] += n1
                    stats["font_size_style_fixed"] += n2
                    stats["font_family_fixed"] += n3
                    data = new_text.encode("utf-8")
            comp = zipfile.ZIP_STORED if info.filename == "mimetype" else zipfile.ZIP_DEFLATED
            zout.writestr(info.filename, data, compress_type=comp)
    os.replace(tmp, epub_path)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    args = ap.parse_args()
    if not args.epub.exists():
        print(f"ERROR: {args.epub} not found", file=sys.stderr); return 1
    print(f"Patching {args.epub}")
    s = patch_epub(args.epub)
    print(f"  Files scanned (xhtml/html/svg):    {s['files_scanned']}")
    print(f"  Files modified:                    {s['files_modified']}")
    print(f"  font-size=\"Npx\" -> em conversions: {s['font_size_attr_fixed']}")
    print(f"  style=\"font-size:Npx\" -> em:       {s['font_size_style_fixed']}")
    print(f"  Proprietary font-family swapped:   {s['font_family_fixed']}")
    print("DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
