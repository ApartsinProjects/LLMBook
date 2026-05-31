"""Source-HTML fix: strip proprietary fonts from SVG inline-style attrs.

ROOT CAUSE
  Source HTML SVG opening tags like:
    <svg style="font-family:'Segoe UI',sans-serif;max-width:100%;height:auto;" ...>
  pass through html2epub fine BUT then the epub-optimizer step
  (html-minifier-terser, Node.js) mangles them. The minifier gets
  confused by the single-quoted 'Segoe UI' nested inside the double-
  quoted style attr value and truncates everything between the first
  and second `'`, producing:
    <svg style="font-family:&apos;height:auto" ...>
  which is broken CSS. KFX then sees font-family value "height:auto"
  (a bogus family) and fires E06424 ("required font files not present").

  This explains why post-build font-family fixes (fix_kfx_svg_text_attrs.py)
  can't help: by the time they run, the corruption has already happened
  and the original font-family value is unrecoverable.

FIX (source level, runs BEFORE the optimizer)
  Walk all source HTML files. For each SVG opening tag with a style="..."
  attribute containing font-family with single-quoted proprietary fonts,
  rewrite the font-family value to use only safe generic / bundled fonts
  (matching fix_kfx_svg_text_attrs.py's PROPRIETARY_FONTS_MAP).

  The minifier never sees the single quotes -> never mangles -> EPUB
  ends up with clean font-family values -> KFX accepts them.

Idempotent. Source-file edit (commits the cleaned style into git).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Same proprietary-font map as fix_kfx_svg_text_attrs.py
PROPRIETARY_FONTS_MAP = {
    "Segoe UI": "sans-serif",
    "Segoe Print": "sans-serif",
    "Consolas": "monospace",
    "Calibri": "sans-serif",
    "Trebuchet MS": "sans-serif",
    "Lucida Console": "monospace",
    "MS Gothic": "sans-serif",
    "Cambria": "serif",
    "Cambria Math": "serif",
    "Helvetica": "sans-serif",
    "Helvetica Neue": "sans-serif",
    "Arial": "sans-serif",
    "Georgia": "serif",
    "Times New Roman": "serif",
    "Courier": "monospace",
    "Courier New": "monospace",
    "Liberation Mono": "monospace",
    # New ones found in this audit (CSS-only)
    "Fira Code": "monospace",
    "IBM Plex Mono": "monospace",
    "Monaco": "monospace",
    "BlinkMacSystemFont": "sans-serif",
    "PT Serif": "serif",
}

# Match style="..." on any tag (we target SVG-related tags but the pattern
# is generic enough). Capture the entire style value to rewrite font-family
# inside.
STYLE_ATTR_RE = re.compile(
    r'\bstyle="([^"]*font-family[^"]*)"',
    re.IGNORECASE,
)

# Inside a captured style value, find font-family declarations
FF_DECL_RE = re.compile(
    r'(font-family\s*:\s*)([^;]+)',
    re.IGNORECASE,
)


def normalize_family_list(value: str) -> str:
    """Strip proprietary fonts, return clean comma-separated value."""
    items = [s.strip().strip("'\"").strip() for s in value.split(",")]
    items = [s for s in items if s]
    cleaned = [s for s in items if s not in PROPRIETARY_FONTS_MAP]
    if cleaned == items:
        return value  # no change
    if not cleaned:
        # All items were proprietary; map first item via the substitution table
        cleaned = [PROPRIETARY_FONTS_MAP.get(items[0], "sans-serif")]
    # Re-emit WITHOUT quotes (single-name generics don't need quoting and
    # multi-word names won't be present after we strip proprietary ones)
    return ", ".join(cleaned)


def fix_style_value(style_value: str) -> tuple[str, int]:
    """Rewrite font-family declarations inside a style attr value."""
    n_changes = 0
    def repl(m: re.Match) -> str:
        nonlocal n_changes
        prefix = m.group(1)
        value = m.group(2)
        new_value = normalize_family_list(value)
        if new_value != value:
            n_changes += 1
        return prefix + new_value
    new_style = FF_DECL_RE.sub(repl, style_value)
    return new_style, n_changes


def patch_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    total_fixed = 0
    def style_repl(m: re.Match) -> str:
        nonlocal total_fixed
        style_value = m.group(1)
        new_value, n = fix_style_value(style_value)
        if n:
            total_fixed += n
            return f'style="{new_value}"'
        return m.group(0)
    new_text = STYLE_ATTR_RE.sub(style_repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return total_fixed


def main() -> int:
    skip_dirs = {"KDP", "node_modules", ".git", "source_fix_backups", "_archive"}
    total_files = 0
    total_modified = 0
    total_fixes = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if any(part in skip_dirs for part in rel.parts):
            continue
        total_files += 1
        try:
            n = patch_file(path)
        except Exception as e:
            print(f"ERR {rel}: {e}", file=sys.stderr)
            continue
        if n:
            total_modified += 1
            total_fixes += n
            print(f"  {n:3d}  {rel}")
    print()
    print(f"Files scanned:  {total_files}")
    print(f"Files modified: {total_modified}")
    print(f"Total fixes:    {total_fixes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
