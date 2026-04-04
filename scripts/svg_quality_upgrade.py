#!/usr/bin/env python3
"""TASK-011: Systematic SVG quality improvement across LLMCourse.

Finds all HTML files containing inline SVGs and applies a set of
quality improvements to bring them to a consistent professional standard.

Improvements applied (only when missing):
  a. role="img" on <svg>
  b. aria-label from nearest figcaption if missing
  c. font-family upgraded to "Segoe UI, system-ui, sans-serif"
  d. Minimum font-size of 11px on text elements
  e. stroke-linecap="round" on stroked elements
  f. rx="6" ry="6" on rect elements >= 20px (skip tiny rects)
  g. Standard gradient <defs> if none present
  h. Standard drop-shadow filter if none present
"""

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")

EXCLUDE_DIRS = {
    "_scripts_archive", "node_modules", ".claude", "scripts",
    "templates", "styles", "agents", "_lab_fragments", "vendor",
}

# Counter for unique filter/gradient IDs across SVGs in a single file
_id_counter = 0


def next_id(prefix: str) -> str:
    global _id_counter
    _id_counter += 1
    return f"{prefix}{_id_counter}"


def collect_html_files(root: Path, single: Path | None = None) -> list[Path]:
    if single:
        return [single]
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                results.append(Path(dirpath) / fn)
    return sorted(results)


def extract_figcaption_text(html: str, svg_start: int) -> str | None:
    """Try to find a figcaption near the SVG (within the same <figure>)."""
    # Look backwards for <figure and forwards for </figure> from svg_start
    chunk_before = html[max(0, svg_start - 500):svg_start]
    chunk_after = html[svg_start:svg_start + 5000]

    # Check if we are inside a <figure>
    if "<figure" not in chunk_before:
        return None

    # Look for figcaption in the figure block after the SVG
    m = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", chunk_after, re.DOTALL)
    if m:
        # Strip HTML tags from caption
        caption = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        # Truncate to reasonable length for aria-label
        if len(caption) > 120:
            caption = caption[:117] + "..."
        return caption
    return None


def upgrade_svg_tag(tag: str, caption: str | None) -> tuple[str, list[str]]:
    """Upgrade the opening <svg ...> tag. Returns (new_tag, list_of_changes)."""
    changes = []
    new = tag

    # (a) Add role="img"
    if 'role=' not in new:
        new = new.replace("<svg ", '<svg role="img" ', 1)
        changes.append("added role=img")

    # (b) Add aria-label from figcaption
    if 'aria-label=' not in new and caption:
        safe_caption = caption.replace('"', "&quot;")
        new = new.replace("<svg ", f'<svg aria-label="{safe_caption}" ', 1)
        changes.append("added aria-label")

    return new, changes


def upgrade_font_family(svg: str) -> tuple[str, list[str]]:
    """Replace bare Arial/Helvetica with Segoe UI stack in font-family attrs."""
    changes = []
    target = "Segoe UI, system-ui, sans-serif"

    # Handle font-family attribute on elements
    def fix_font_attr(m):
        val = m.group(1)
        # If it already has Segoe UI, skip
        if "Segoe UI" in val and "system-ui" in val:
            return m.group(0)
        # Replace bare Arial or Helvetica
        if re.match(r"^\s*(Arial|Helvetica)\s*$", val):
            changes.append("upgraded font-family")
            return f'font-family="{target}"'
        return m.group(0)

    svg = re.sub(r'font-family="([^"]*)"', fix_font_attr, svg)

    # Also fix font-family in style attribute on <svg> tag
    def fix_style_font(m):
        style = m.group(1)
        if "Segoe UI" in style and "system-ui" in style:
            return m.group(0)
        # Replace font-family inside style
        new_style = re.sub(
            r"font-family:\s*['\"]?(Arial|Helvetica)['\"]?",
            f"font-family: '{target}'",
            style
        )
        if new_style != style:
            changes.append("upgraded style font-family")
        return f'style="{new_style}"'

    svg = re.sub(r'style="([^"]*font-family[^"]*)"', fix_style_font, svg)

    return svg, changes


def upgrade_font_size(svg: str) -> tuple[str, list[str]]:
    """Ensure minimum font-size of 11px on text elements."""
    changes = []

    def fix_text_element(m):
        text_tag = m.group(0)
        fs_match = re.search(r'font-size="(\d+(?:\.\d+)?)', text_tag)
        if fs_match:
            size = float(fs_match.group(1))
            if size < 11:
                old = fs_match.group(0)
                new = f'font-size="11'
                text_tag = text_tag.replace(old, new, 1)
                changes.append(f"font-size {size}->{11}")
        return text_tag

    svg = re.sub(r"<text\b[^>]*>", fix_text_element, svg)
    return svg, changes


def upgrade_stroke_linecap(svg: str) -> tuple[str, list[str]]:
    """Add stroke-linecap='round' to elements that have stroke but no linecap."""
    changes = []
    stroke_tags = ["line", "path", "polyline", "polygon", "circle", "ellipse", "rect"]
    tag_pattern = "|".join(stroke_tags)

    def fix_stroke(m):
        tag = m.group(0)
        if 'stroke="' in tag and 'stroke="none"' not in tag and 'stroke-linecap=' not in tag:
            # Insert before the closing >
            tag = tag[:-1] + ' stroke-linecap="round">'
            changes.append("added stroke-linecap")
        return tag

    svg = re.sub(rf"<({tag_pattern})\b[^>]*>", fix_stroke, svg)
    return svg, changes


def upgrade_rect_corners(svg: str) -> tuple[str, list[str]]:
    """Add rx=6 ry=6 to rect elements without rx/ry (skip small rects)."""
    changes = []

    def fix_rect(m):
        rect = m.group(0)
        if "rx=" in rect or "ry=" in rect:
            return rect
        w_m = re.search(r'width="(\d+(?:\.\d+)?)', rect)
        h_m = re.search(r'height="(\d+(?:\.\d+)?)', rect)
        if w_m and h_m:
            w, h = float(w_m.group(1)), float(h_m.group(1))
            if w < 20 or h < 20:
                return rect
        elif w_m:
            if float(w_m.group(1)) < 20:
                return rect
        elif h_m:
            if float(h_m.group(1)) < 20:
                return rect
        # Add rounded corners
        rect = rect[:-1] + ' rx="6" ry="6">'
        # Handle self-closing
        if rect.endswith(' rx="6" ry="6">>'):
            rect = rect[:-1]
        changes.append("added rx/ry=6")
        return rect

    svg = re.sub(r"<rect\b[^>]*/?>", fix_rect, svg)
    return svg, changes


def upgrade_gradient(svg: str) -> tuple[str, list[str]]:
    """Add a standard subtle gradient definition if none present."""
    changes = []
    if re.search(r"<(linearGradient|radialGradient)\b", svg):
        return svg, changes

    gid = next_id("stdGrad")
    gradient_def = (
        f'<linearGradient id="{gid}" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" style="stop-color:#f8f9fa;stop-opacity:0.7"/>'
        f'<stop offset="100%" style="stop-color:#e9ecef;stop-opacity:0.3"/>'
        f'</linearGradient>'
    )

    # If there is a <defs> block, insert into it
    if "<defs>" in svg:
        svg = svg.replace("<defs>", f"<defs>{gradient_def}", 1)
    elif "<defs " in svg:
        # <defs with attributes
        defs_m = re.search(r"(<defs\b[^>]*>)", svg)
        if defs_m:
            svg = svg.replace(defs_m.group(0), defs_m.group(0) + gradient_def, 1)
    else:
        # Insert a new <defs> block right after the opening <svg...> tag
        svg_tag_m = re.match(r"<svg\b[^>]*>", svg)
        if svg_tag_m:
            insert_at = svg_tag_m.end()
            svg = svg[:insert_at] + f"<defs>{gradient_def}</defs>" + svg[insert_at:]

    changes.append("added standard gradient")
    return svg, changes


def upgrade_shadow(svg: str) -> tuple[str, list[str]]:
    """Add a standard drop-shadow filter if none present."""
    changes = []
    if re.search(r"<(filter|feDropShadow|feGaussianBlur)\b", svg):
        return svg, changes

    fid = next_id("stdShadow")
    shadow_def = (
        f'<filter id="{fid}" x="-4%" y="-4%" width="108%" height="116%">'
        f'<feDropShadow dx="1" dy="2" stdDeviation="2" flood-opacity="0.08"/>'
        f'</filter>'
    )

    if "<defs>" in svg:
        svg = svg.replace("<defs>", f"<defs>{shadow_def}", 1)
    elif "<defs " in svg:
        defs_m = re.search(r"(<defs\b[^>]*>)", svg)
        if defs_m:
            svg = svg.replace(defs_m.group(0), defs_m.group(0) + shadow_def, 1)
    else:
        svg_tag_m = re.match(r"<svg\b[^>]*>", svg)
        if svg_tag_m:
            insert_at = svg_tag_m.end()
            svg = svg[:insert_at] + f"<defs>{shadow_def}</defs>" + svg[insert_at:]

    changes.append("added drop-shadow filter")
    return svg, changes


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    """Process a single HTML file. Returns a report dict."""
    global _id_counter

    html = filepath.read_text(encoding="utf-8", errors="ignore")
    original_html = html

    # Find all SVG blocks with their positions
    svg_pattern = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL)
    matches = list(svg_pattern.finditer(html))

    if not matches:
        return {"file": str(filepath), "svgs": 0, "changes": []}

    all_changes = []
    # Process in reverse order so replacements don't shift positions
    for match in reversed(matches):
        svg_original = match.group(0)
        svg = svg_original
        svg_changes = []

        # Get figcaption for aria-label
        caption = extract_figcaption_text(html, match.start())

        # (a, b) Upgrade SVG tag
        svg_tag_m = re.match(r"<svg\b[^>]*>", svg)
        if svg_tag_m:
            new_tag, ch = upgrade_svg_tag(svg_tag_m.group(0), caption)
            svg = new_tag + svg[svg_tag_m.end():]
            svg_changes.extend(ch)

        # (c) Font family
        svg, ch = upgrade_font_family(svg)
        svg_changes.extend(ch)

        # (d) Font size
        svg, ch = upgrade_font_size(svg)
        svg_changes.extend(ch)

        # (e) Stroke linecap
        svg, ch = upgrade_stroke_linecap(svg)
        svg_changes.extend(ch)

        # (f) Rect corners
        svg, ch = upgrade_rect_corners(svg)
        svg_changes.extend(ch)

        # (g) Gradient
        svg, ch = upgrade_gradient(svg)
        svg_changes.extend(ch)

        # (h) Shadow filter
        svg, ch = upgrade_shadow(svg)
        svg_changes.extend(ch)

        if svg_changes:
            html = html[:match.start()] + svg + html[match.end():]
            all_changes.extend(svg_changes)

    if html != original_html and not dry_run:
        filepath.write_text(html, encoding="utf-8")

    return {
        "file": str(filepath.relative_to(ROOT)),
        "svgs": len(matches),
        "changes": all_changes,
        "modified": html != original_html,
    }


def main():
    global _id_counter

    parser = argparse.ArgumentParser(description="SVG quality upgrade for LLMCourse")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files")
    parser.add_argument("--path", type=str, help="Process a single file")
    args = parser.parse_args()

    single = Path(args.path) if args.path else None
    files = collect_html_files(ROOT, single)

    total_svgs = 0
    total_modified = 0
    total_changes = 0

    for f in files:
        _id_counter = 0  # Reset per file for stable IDs
        report = process_file(f, dry_run=args.dry_run)
        total_svgs += report["svgs"]
        if report.get("modified"):
            total_modified += 1
        if report["changes"]:
            total_changes += len(report["changes"])
            # Summarize changes per file
            from collections import Counter
            counts = Counter(report["changes"])
            summary = ", ".join(f"{v}x {k}" for k, v in counts.most_common())
            print(f"  {report['file']} ({report['svgs']} SVGs): {summary}")

    mode = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{mode}Summary: {total_svgs} SVGs in {len(files)} files, "
          f"{total_modified} files modified, {total_changes} total changes applied.")


if __name__ == "__main__":
    main()
