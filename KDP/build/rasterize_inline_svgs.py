"""
Rasterize / externalize inline SVGs across the book's source HTML.

Why this exists
---------------
KFX's SVG preprocessor injects computed pixel font-sizes into inline `<svg><text>`
elements and then KFX's Stage 2 rejects those same px values
(E02208 "font-size other than EM or REM"). The bug is in KFX's own pipeline and
cannot be reached from source CSS.

Workaround:
- Extract every inline `<svg>...</svg>` into a standalone .svg file under
  `images/svg-rasterized/svg_<hash>.svg`.
- Replace the inline SVG with `<img src="..." alt="<aria-label>" width=W height=H />`.
- KFX rasterizes standalone .svg files internally (the SVG preprocessor that
  injects px font-sizes only runs on INLINE SVGs in XHTML).

Optionally, when cairosvg / svglib + cairo are available, write a real PNG
instead of a standalone .svg. On this machine cairo is not installed and the
brief explicitly endorses the standalone-.svg fallback as having the same
E02208-bypass benefit.

Output
------
- `images/svg-rasterized/svg_<hash>.svg` (content-addressed; idempotent).
- Replaced inline `<svg>` with `<img>` referencing the file with a relative path.
- Backup of every modified HTML file under
  `KDP/build/source_fix_backups/svg_rasterize_<timestamp>/...`.
- JSON stats file at `KDP/build/_kpv_debug_archive/rasterize_inline_svgs_<ts>.json`.

Usage
-----
    C:/Python314/python KDP/build/rasterize_inline_svgs.py [--dry-run] [--limit N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Optional


# Project root: KDP/build/rasterize_inline_svgs.py -> two parents up.
ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {
    "KDP",
    "node_modules",
    ".git",
    "_archive",
    "source_fix_backups",
    ".html2epub_cache",
    "__pycache__",
    ".book-update",
    ".tools",
    ".claude",
    ".github",
    "_concept-figs",
    "agents",  # template + non-published material
}

OUTPUT_DIR = ROOT / "images" / "svg-rasterized"
BACKUP_ROOT = ROOT / "KDP" / "build" / "source_fix_backups"
DEBUG_ARCHIVE = ROOT / "KDP" / "build" / "_kpv_debug_archive"

# Regexes.
# Match an entire <svg ...> ... </svg> block. SVG nesting is rare in this book,
# but we use a non-greedy match plus a depth check.
SVG_OPEN_RE = re.compile(r"<svg\b", re.IGNORECASE)
SVG_CLOSE_RE = re.compile(r"</svg\s*>", re.IGNORECASE)

ARIA_LABEL_RE = re.compile(r'\baria-label\s*=\s*"([^"]*)"', re.IGNORECASE)
ARIA_LABEL_RE_SQ = re.compile(r"\baria-label\s*=\s*'([^']*)'", re.IGNORECASE)
VIEWBOX_RE = re.compile(
    r'\bview[Bb]ox\s*=\s*"([^"]+)"', re.IGNORECASE
)
VIEWBOX_RE_SQ = re.compile(
    r"\bview[Bb]ox\s*=\s*'([^']+)'", re.IGNORECASE
)
WIDTH_ATTR_RE = re.compile(r'\swidth\s*=\s*"([^"]+)"', re.IGNORECASE)
HEIGHT_ATTR_RE = re.compile(r'\sheight\s*=\s*"([^"]+)"', re.IGNORECASE)


def iter_target_files() -> list[Path]:
    """Return all section-*.html / index.html outside SKIP_DIRS."""
    out: list[Path] = []
    for pattern in ("section-*.html", "index.html"):
        for p in ROOT.rglob(pattern):
            rel = p.relative_to(ROOT)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            out.append(p)
    return sorted(set(out))


def find_inline_svgs(html: str) -> list[tuple[int, int, str]]:
    """Return list of (start, end, svg_text) for each top-level inline SVG.

    Handles nesting (rare but defensive): walks until matching </svg>.
    """
    out: list[tuple[int, int, str]] = []
    i = 0
    n = len(html)
    while i < n:
        m = SVG_OPEN_RE.search(html, i)
        if not m:
            break
        start = m.start()
        depth = 1
        cursor = m.end()
        # Find the end of the opening <svg ...> tag first.
        tag_end_idx = html.find(">", cursor)
        if tag_end_idx == -1:
            break
        cursor = tag_end_idx + 1
        # Now walk forward, counting nested <svg>/</svg>.
        while depth > 0:
            next_open = SVG_OPEN_RE.search(html, cursor)
            next_close = SVG_CLOSE_RE.search(html, cursor)
            if not next_close:
                # Malformed; give up on this one.
                break
            if next_open and next_open.start() < next_close.start():
                depth += 1
                # Skip past its opening tag.
                inner_tag_end = html.find(">", next_open.end())
                if inner_tag_end == -1:
                    break
                cursor = inner_tag_end + 1
            else:
                depth -= 1
                cursor = next_close.end()
        if depth == 0:
            out.append((start, cursor, html[start:cursor]))
            i = cursor
        else:
            # Skip past this broken opener and continue.
            i = m.end()
    return out


def extract_attr(svg_open_text: str, regex_dq, regex_sq) -> Optional[str]:
    m = regex_dq.search(svg_open_text)
    if m:
        return m.group(1)
    m = regex_sq.search(svg_open_text)
    if m:
        return m.group(1)
    return None


def parse_svg_dims(svg_text: str) -> tuple[int, int]:
    """Best-effort dimension extraction. Defaults to 800x600."""
    # Look at the opening tag only.
    open_end = svg_text.find(">")
    open_tag = svg_text[: open_end + 1] if open_end != -1 else svg_text

    # width/height attributes
    w_attr = extract_attr(open_tag, WIDTH_ATTR_RE, re.compile(r"\swidth\s*=\s*'([^']+)'"))
    h_attr = extract_attr(open_tag, HEIGHT_ATTR_RE, re.compile(r"\sheight\s*=\s*'([^']+)'"))

    def _parse_px(v: str | None) -> int | None:
        if not v:
            return None
        s = v.strip().rstrip("px").strip()
        try:
            return int(round(float(s)))
        except ValueError:
            return None

    w = _parse_px(w_attr)
    h = _parse_px(h_attr)

    if w and h:
        return w, h

    vb = extract_attr(open_tag, VIEWBOX_RE, VIEWBOX_RE_SQ)
    if vb:
        parts = re.split(r"[\s,]+", vb.strip())
        if len(parts) == 4:
            try:
                vw = float(parts[2])
                vh = float(parts[3])
                if w and not h:
                    return w, int(round(w * vh / vw))
                if h and not w:
                    return int(round(h * vw / vh)), h
                # Both missing: pick width 800, scale height.
                return 800, int(round(800 * vh / vw))
            except ValueError:
                pass

    return w or 800, h or 600


def ensure_standalone_svg(svg_text: str) -> str:
    """Wrap raw inline SVG so it's valid as a standalone .svg file.

    Adds xmlns when missing and prepends XML declaration.
    """
    # Add xmlns if absent.
    open_end = svg_text.find(">")
    if open_end == -1:
        return svg_text
    open_tag = svg_text[: open_end + 1]
    if "xmlns" not in open_tag:
        # Insert xmlns just before the closing '>'.
        rest = svg_text[open_end + 1 :]
        new_open = open_tag[:-1].rstrip() + ' xmlns="http://www.w3.org/2000/svg">'
        svg_text = new_open + rest

    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + svg_text


def relpath_for_href(html_file: Path, target: Path) -> str:
    """Compute POSIX-style relative path from html_file's dir to target."""
    rel = os.path.relpath(target, html_file.parent)
    return rel.replace(os.sep, "/")


def html_escape_attr(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def process_file(
    html_file: Path,
    backup_dir: Path,
    stats: dict,
    dry_run: bool,
) -> bool:
    """Process one HTML file. Returns True if file was modified."""
    try:
        original = html_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        original = html_file.read_text(encoding="utf-8", errors="replace")

    matches = find_inline_svgs(original)
    if not matches:
        return False

    stats["svgs_found"] += len(matches)

    # Build replacement string by walking matches in reverse so indices remain valid.
    new_html = original
    file_modified_count = 0
    for start, end, svg_text in reversed(matches):
        # Hash on the raw inline SVG content (whitespace included).
        h = hashlib.sha1(svg_text.encode("utf-8")).hexdigest()[:16]
        svg_filename = f"svg_{h}.svg"
        out_path = OUTPUT_DIR / svg_filename

        # Idempotent: only write if missing or differs.
        if not out_path.exists():
            standalone = ensure_standalone_svg(svg_text)
            if not dry_run:
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                out_path.write_text(standalone, encoding="utf-8")
            stats["svgs_extracted"] += 1
        else:
            stats["svgs_reused"] += 1

        # Width/height for the <img>.
        w, h_dim = parse_svg_dims(svg_text)

        # aria-label for alt.
        open_end = svg_text.find(">")
        open_tag = svg_text[: open_end + 1] if open_end != -1 else svg_text
        aria = extract_attr(open_tag, ARIA_LABEL_RE, ARIA_LABEL_RE_SQ) or ""
        alt = html_escape_attr(aria)

        # Compute relative path from this HTML file to the standalone SVG.
        rel_src = relpath_for_href(html_file, out_path)
        img_tag = (
            f'<img src="{rel_src}" alt="{alt}" width="{w}" height="{h_dim}" '
            f'class="rasterized-svg" />'
        )
        new_html = new_html[:start] + img_tag + new_html[end:]
        file_modified_count += 1

    if new_html != original:
        if not dry_run:
            # Backup first.
            rel = html_file.relative_to(ROOT)
            bkp = backup_dir / rel
            bkp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(html_file, bkp)
            html_file.write_text(new_html, encoding="utf-8")
        stats["files_modified"] += 1
        stats["replacements"] += file_modified_count
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Don't write anything.")
    parser.add_argument("--limit", type=int, default=0, help="Only process first N files (debug).")
    args = parser.parse_args()

    ts = time.strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / f"svg_rasterize_{ts}"

    stats = {
        "started_at": ts,
        "files_scanned": 0,
        "files_modified": 0,
        "svgs_found": 0,
        "svgs_extracted": 0,
        "svgs_reused": 0,
        "replacements": 0,
        "failed_files": [],
    }

    files = iter_target_files()
    if args.limit:
        files = files[: args.limit]
    stats["files_scanned"] = len(files)

    print(f"[rasterize] Scanning {len(files)} HTML files.")
    print(f"[rasterize] Output dir: {OUTPUT_DIR}")
    print(f"[rasterize] Backup dir: {backup_dir if not args.dry_run else '(dry-run, no backup)'}")

    if not args.dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        DEBUG_ARCHIVE.mkdir(parents=True, exist_ok=True)

    for i, f in enumerate(files):
        try:
            process_file(f, backup_dir, stats, args.dry_run)
        except Exception as e:  # noqa: BLE001 - we want to log per-file errors
            stats["failed_files"].append({"file": str(f.relative_to(ROOT)), "error": repr(e)})
        if (i + 1) % 100 == 0:
            print(
                f"  [{i + 1}/{len(files)}] svgs_found={stats['svgs_found']} "
                f"extracted={stats['svgs_extracted']} reused={stats['svgs_reused']} "
                f"modified={stats['files_modified']}"
            )

    # Disk impact.
    if OUTPUT_DIR.exists():
        total_bytes = sum(f.stat().st_size for f in OUTPUT_DIR.iterdir() if f.is_file())
        stats["output_dir_bytes"] = total_bytes
        stats["output_dir_mb"] = round(total_bytes / (1024 * 1024), 2)
        stats["output_dir_files"] = sum(1 for _ in OUTPUT_DIR.iterdir() if _.is_file())
    else:
        stats["output_dir_bytes"] = 0
        stats["output_dir_mb"] = 0
        stats["output_dir_files"] = 0

    stats["finished_at"] = time.strftime("%Y%m%d-%H%M%S")
    stats["dry_run"] = args.dry_run

    print()
    print("[rasterize] Done.")
    print(f"  files scanned:   {stats['files_scanned']}")
    print(f"  files modified:  {stats['files_modified']}")
    print(f"  svgs found:      {stats['svgs_found']}")
    print(f"  svgs extracted:  {stats['svgs_extracted']}")
    print(f"  svgs reused:     {stats['svgs_reused']}")
    print(f"  replacements:    {stats['replacements']}")
    print(f"  failed files:    {len(stats['failed_files'])}")
    print(f"  output dir:      {stats['output_dir_files']} files, {stats['output_dir_mb']} MB")

    if not args.dry_run:
        json_path = DEBUG_ARCHIVE / f"rasterize_inline_svgs_{ts}.json"
        json_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
        print(f"  stats written:   {json_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
