"""Post-build EPUB patch: strip CSS properties that KFX silently ignores.

WHY POST-BUILD (NOT SOURCE)
  The source `styles/book.css` is shared with the web rendering of the book.
  Stripping `box-sizing` / `@media` / etc. from source would harm the web
  layout. So we patch the COPY of these stylesheets inside the built EPUB.
  The web site keeps its full CSS; the EPUB ships a slimmed version.

WHAT THIS REMOVES (each emits W00015 / W10023 / W11007 in KFX log)
  W00015 noise (KFX ignores these; main goal is to slim the log from ~70 MB to ~1 MB):
    - box-sizing: <any>
    - line-height: <any>           (KFX overrides per device)
    - -webkit-column-*             (no CSS columns on Kindle)
    - -webkit-print-color-adjust   (print-only)
    - print-color-adjust           (print-only)
    - caption-side                 (KFX places captions in fixed location)

  W10023 (unsupported media queries):
    - @media (max-width: ...)       (KFX uses device profiles, not viewport widths)
    - @media (min-width: ...)
    - @media print                  (irrelevant for digital reading)

  W11007 (float on table elements):
    - any CSS rule whose selector targets `table` AND declares `float: ...`

Usage:
  python KDP/build/fix_kfx_epub_css.py <epub_path>
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path


# Properties to strip from any declaration block
STRIP_PROPS = (
    "box-sizing", "line-height",
    "-webkit-column-break-inside", "-webkit-column-span", "-webkit-column-count",
    "-webkit-column-width", "-webkit-column-gap", "-webkit-column",
    "-webkit-print-color-adjust", "print-color-adjust",
    "caption-side",
)

# Match a single CSS declaration like `prop: value;` or `prop:value` (no semi at end)
DECL_RE = re.compile(
    r"(^|[\s;{])\s*(" + "|".join(re.escape(p) for p in STRIP_PROPS) + r")\s*:\s*[^;}]+;?",
    re.IGNORECASE | re.MULTILINE,
)

# Match an entire @media at-rule (with its full body)
MEDIA_RE = re.compile(r"@media[^{]*\{(?:[^{}]|\{[^{}]*\})*\}", re.IGNORECASE)

# Match float declarations in a rule that selects table
# (rule selector contains "table" OR class on a table element)
# Simpler: drop any `float: <left|right>;` declarations whose containing block
# selector mentions table. Cheap heuristic: scan rule-by-rule.
RULE_RE = re.compile(r"([^{}]*)\{([^{}]*)\}", re.DOTALL)
FLOAT_DECL = re.compile(r"\bfloat\s*:\s*(left|right)\s*;?\s*", re.IGNORECASE)


def strip_props(css: str) -> tuple[str, int]:
    """Strip unsupported property declarations. Return (new_css, removed_count)."""
    count = 0
    def repl(m):
        nonlocal count
        count += 1
        return m.group(1)  # keep the boundary char (`;` or `{` or space)
    new_css = DECL_RE.sub(repl, css)
    return new_css, count


def strip_media(css: str) -> tuple[str, int]:
    """Strip entire @media blocks."""
    count = len(MEDIA_RE.findall(css))
    new_css = MEDIA_RE.sub("", css)
    return new_css, count


def strip_table_floats(css: str) -> tuple[str, int]:
    """Strip `float:` declarations in any rule whose selector mentions table."""
    count = 0
    def replace_rule(m: re.Match) -> str:
        nonlocal count
        selector, body = m.group(1), m.group(2)
        if "table" in selector.lower():
            new_body, n = FLOAT_DECL.subn("", body)
            count += n
            return f"{selector}{{{new_body}}}"
        return m.group(0)
    new_css = RULE_RE.sub(replace_rule, css)
    return new_css, count


def patch_epub(epub_path: Path) -> dict:
    stats = {"css_files": 0, "props_removed": 0, "media_removed": 0,
             "table_floats_removed": 0, "bytes_saved": 0}
    tmp = epub_path.with_suffix(epub_path.suffix + ".tmp")
    with zipfile.ZipFile(epub_path, "r") as zin, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename.lower().endswith(".css"):
                stats["css_files"] += 1
                orig_bytes = len(data)
                text = data.decode("utf-8", errors="replace")
                text, n1 = strip_props(text)
                text, n2 = strip_media(text)
                text, n3 = strip_table_floats(text)
                stats["props_removed"] += n1
                stats["media_removed"] += n2
                stats["table_floats_removed"] += n3
                new = text.encode("utf-8")
                stats["bytes_saved"] += max(0, orig_bytes - len(new))
                data = new
            # mimetype stays uncompressed
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
    print(f"  CSS files scanned:        {s['css_files']}")
    print(f"  KFX-ignored props removed: {s['props_removed']}")
    print(f"  @media rules removed:      {s['media_removed']}")
    print(f"  Float-on-table fixed:      {s['table_floats_removed']}")
    print(f"  CSS bytes saved:           {s['bytes_saved']:,}")
    print("DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
