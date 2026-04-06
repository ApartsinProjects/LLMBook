"""
Audit SVG diagrams in HTML files for overlapping elements.
Detects: text-on-rect, text-on-text, annotation lines on rects, text on arrows.
"""

import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

BASE = Path(r"E:/Projects/LLMCourse")

# Directories to scan
SCAN_DIRS = [
    BASE / "part-1-foundations",
    BASE / "part-2-understanding-llms",
    BASE / "part-3-working-with-llms",
    BASE / "part-4-training-adapting",
    BASE / "part-5-retrieval-conversation",
    BASE / "part-6-agentic-ai",
    BASE / "part-7-multimodal-applications",
    BASE / "part-8-evaluation-production",
    BASE / "part-9-safety-strategy",
    BASE / "part-10-frontiers",
    BASE / "part-11-idea-to-product",
    BASE / "appendices",
    BASE / "front-matter",
]


def find_html_files():
    files = []
    for d in SCAN_DIRS:
        if not d.exists():
            continue
        for f in d.rglob("section-*.html"):
            files.append(f)
        for f in d.rglob("index.html"):
            files.append(f)
    return sorted(set(files))


def extract_svgs_from_html(html_text):
    """Extract SVG blocks and their surrounding figure caption if any."""
    results = []
    # Find all <svg ...>...</svg> blocks
    pattern = re.compile(r'(<svg[^>]*>.*?</svg>)', re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(html_text):
        svg_text = m.group(1)
        start = m.start()
        # Look for figure caption nearby (within 500 chars after svg end)
        caption = ""
        after = html_text[m.end():m.end()+500]
        cap_m = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', after, re.DOTALL)
        if cap_m:
            caption = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip()
        # Also check before
        if not caption:
            before = html_text[max(0,start-500):start]
            cap_m = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', before, re.DOTALL)
            if cap_m:
                caption = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip()
        results.append((svg_text, caption))
    return results


def parse_float(val):
    if val is None:
        return None
    try:
        # Handle percentage or other suffixes
        val = val.strip().replace('px', '')
        return float(val)
    except (ValueError, TypeError):
        return None


def get_text_content(elem):
    """Get all text content from an element and its children."""
    parts = []
    if elem.text:
        parts.append(elem.text.strip())
    for child in elem:
        t = get_text_content(child)
        if t:
            parts.append(t)
        if child.tail:
            parts.append(child.tail.strip())
    return ' '.join(parts)


def parse_transform_translate(transform_str):
    """Extract translate(x,y) from a transform attribute."""
    if not transform_str:
        return 0, 0
    m = re.search(r'translate\(\s*([-\d.]+)\s*[,\s]\s*([-\d.]+)\s*\)', transform_str)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r'translate\(\s*([-\d.]+)\s*\)', transform_str)
    if m:
        return float(m.group(1)), 0
    return 0, 0


def analyze_svg(svg_text):
    """Analyze one SVG for overlapping elements. Returns list of issue strings."""
    issues = []

    # Clean up namespaces that might break ET
    svg_text = re.sub(r'xmlns\s*=\s*"[^"]*"', '', svg_text, count=1)
    svg_text = re.sub(r'xmlns:\w+\s*=\s*"[^"]*"', '', svg_text)

    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError:
        return issues

    # Collect all rects with absolute positions
    rects = []
    texts = []
    lines = []

    def collect_elements(elem, parent_tx=0, parent_ty=0):
        # Check for transform on this element
        transform = elem.get('transform', '')
        tx, ty = parse_transform_translate(transform)
        abs_tx = parent_tx + tx
        abs_ty = parent_ty + ty

        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

        if tag == 'rect':
            x = parse_float(elem.get('x', '0')) or 0
            y = parse_float(elem.get('y', '0')) or 0
            w = parse_float(elem.get('width'))
            h = parse_float(elem.get('height'))
            if w and h and w > 5 and h > 5:  # skip tiny rects (decorative)
                fill = elem.get('fill', '')
                stroke = elem.get('stroke', '')
                rects.append({
                    'x': x + abs_tx, 'y': y + abs_ty,
                    'w': w, 'h': h,
                    'fill': fill, 'stroke': stroke
                })

        elif tag == 'text':
            x = parse_float(elem.get('x', '0')) or 0
            y = parse_float(elem.get('y', '0')) or 0
            content = get_text_content(elem)
            if content.strip():
                # Estimate text width: ~7px per char at typical SVG font size
                font_size = 14
                fs_attr = elem.get('font-size', '')
                if fs_attr:
                    fs = parse_float(fs_attr)
                    if fs:
                        font_size = fs
                # Check style attribute for font-size
                style = elem.get('style', '')
                fs_m = re.search(r'font-size:\s*([\d.]+)', style)
                if fs_m:
                    font_size = float(fs_m.group(1))

                char_width = font_size * 0.6
                text_width = len(content) * char_width
                text_height = font_size

                anchor = elem.get('text-anchor', 'start')
                actual_x = x + abs_tx
                if anchor == 'middle':
                    actual_x -= text_width / 2
                elif anchor == 'end':
                    actual_x -= text_width

                texts.append({
                    'x': actual_x,
                    'y': y + abs_ty - text_height,  # text y is baseline
                    'w': text_width,
                    'h': text_height,
                    'baseline_y': y + abs_ty,
                    'content': content[:60],
                    'font_size': font_size,
                    'anchor': anchor,
                    'raw_x': x + abs_tx,
                    'raw_y': y + abs_ty,
                })

        elif tag == 'line':
            x1 = parse_float(elem.get('x1', '0')) or 0
            y1 = parse_float(elem.get('y1', '0')) or 0
            x2 = parse_float(elem.get('x2', '0')) or 0
            y2 = parse_float(elem.get('y2', '0')) or 0
            is_annotation = elem.get('data-annotation-line') is not None
            marker = elem.get('marker-end', '') or elem.get('marker-start', '')
            lines.append({
                'x1': x1 + abs_tx, 'y1': y1 + abs_ty,
                'x2': x2 + abs_tx, 'y2': y2 + abs_ty,
                'is_annotation': is_annotation,
                'has_marker': bool(marker),
            })

        for child in elem:
            collect_elements(child, abs_tx, abs_ty)

    collect_elements(root)

    # Skip SVGs with very few elements (likely decorative)
    if len(rects) < 1 and len(texts) < 2:
        return issues

    # CHECK 1: Text overlapping rect (text NOT a label inside the rect)
    # A text is "inside" a rect if its position falls within rect bounds.
    # We flag texts that partially overlap a rect boundary (edge cases).
    # Actually, many texts ARE intentional labels inside boxes.
    # Flag when: text center is inside rect BUT text extends beyond rect bounds
    # (indicating misplacement), OR text is clearly not centered in the rect.

    # Better approach: find texts whose bounding box overlaps a rect but
    # the text is not well-centered (label) inside that rect.
    # For simplicity, skip this check and focus on text-text overlap which is
    # more reliably detectable.

    # CHECK 2: Text overlapping text
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            t1 = texts[i]
            t2 = texts[j]

            # Check if y ranges overlap (within ~font height)
            y_overlap = not (t1['y'] + t1['h'] < t2['y'] or t2['y'] + t2['h'] < t1['y'])

            if not y_overlap:
                continue

            # Check y proximity (within 12px of each other's baseline)
            y_dist = abs(t1['baseline_y'] - t2['baseline_y'])
            if y_dist > max(t1['font_size'], t2['font_size']) * 1.0:
                continue

            # Check x range overlap
            x1_start, x1_end = t1['x'], t1['x'] + t1['w']
            x2_start, x2_end = t2['x'], t2['x'] + t2['w']

            x_overlap_amount = min(x1_end, x2_end) - max(x1_start, x2_start)

            if x_overlap_amount > 5:  # meaningful overlap
                # Skip if one text is clearly a sub-element (tspan content)
                if t1['content'] in t2['content'] or t2['content'] in t1['content']:
                    continue
                issues.append(
                    f"  TEXT-TEXT OVERLAP: \"{t1['content']}\" (x={t1['raw_x']:.0f}, y={t1['raw_y']:.0f}) "
                    f"overlaps \"{t2['content']}\" (x={t2['raw_x']:.0f}, y={t2['raw_y']:.0f}), "
                    f"x-overlap={x_overlap_amount:.0f}px, y-dist={y_dist:.0f}px"
                )

    # CHECK 3: Text positioned directly on top of a rect edge (not centered inside)
    for t in texts:
        for r in rects:
            # Text baseline is near the top or bottom edge of a rect
            # and text horizontally overlaps the rect
            t_cx = t['raw_x']
            t_cy = t['raw_y']

            # Is text horizontally within rect bounds?
            if t_cx < r['x'] - 5 or t_cx > r['x'] + r['w'] + 5:
                continue

            # Is text baseline right on rect top or bottom edge (within 3px)?
            on_top_edge = abs(t_cy - r['y']) < 4
            on_bottom_edge = abs(t_cy - (r['y'] + r['h'])) < 4

            if on_top_edge or on_bottom_edge:
                edge = "top" if on_top_edge else "bottom"
                issues.append(
                    f"  TEXT-ON-RECT-EDGE: \"{t['content']}\" at ({t['raw_x']:.0f},{t['raw_y']:.0f}) "
                    f"sits on {edge} edge of rect at ({r['x']:.0f},{r['y']:.0f}, {r['w']:.0f}x{r['h']:.0f})"
                )

    # CHECK 4: Annotation lines overlapping rects
    for l in lines:
        if not l['is_annotation']:
            continue
        for r in rects:
            # Check if line segment intersects rect
            lx_min = min(l['x1'], l['x2'])
            lx_max = max(l['x1'], l['x2'])
            ly_min = min(l['y1'], l['y2'])
            ly_max = max(l['y1'], l['y2'])

            rx_min = r['x']
            rx_max = r['x'] + r['w']
            ry_min = r['y']
            ry_max = r['y'] + r['h']

            # Bounding box overlap check
            if lx_max >= rx_min and lx_min <= rx_max and ly_max >= ry_min and ly_min <= ry_max:
                issues.append(
                    f"  ANNOTATION-LINE-ON-RECT: line ({l['x1']:.0f},{l['y1']:.0f})-({l['x2']:.0f},{l['y2']:.0f}) "
                    f"overlaps rect at ({r['x']:.0f},{r['y']:.0f}, {r['w']:.0f}x{r['h']:.0f})"
                )

    # CHECK 5: Text on arrow lines
    for t in texts:
        for l in lines:
            if not l['has_marker']:
                continue
            # Check if text position is very close to the line
            # Point-to-line-segment distance
            t_cx = t['raw_x']
            t_cy = t['raw_y']

            dx = l['x2'] - l['x1']
            dy = l['y2'] - l['y1']
            line_len_sq = dx*dx + dy*dy
            if line_len_sq < 1:
                continue

            # Project point onto line
            param = ((t_cx - l['x1'])*dx + (t_cy - l['y1'])*dy) / line_len_sq
            param = max(0, min(1, param))

            closest_x = l['x1'] + param * dx
            closest_y = l['y1'] + param * dy

            dist = ((t_cx - closest_x)**2 + (t_cy - closest_y)**2)**0.5

            if dist < 5:  # within 5px of the arrow line
                issues.append(
                    f"  TEXT-ON-ARROW: \"{t['content']}\" at ({t_cx:.0f},{t_cy:.0f}) "
                    f"sits on arrow ({l['x1']:.0f},{l['y1']:.0f})-({l['x2']:.0f},{l['y2']:.0f}), dist={dist:.1f}px"
                )

    return issues


def main():
    html_files = find_html_files()
    print(f"Scanning {len(html_files)} HTML files for SVG overlap issues...\n")

    total_svgs = 0
    total_issues = 0
    files_with_issues = 0
    all_results = []

    for fpath in html_files:
        try:
            html_text = fpath.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            continue

        svgs = extract_svgs_from_html(html_text)
        if not svgs:
            continue

        file_issues = []
        for idx, (svg_text, caption) in enumerate(svgs):
            total_svgs += 1
            issues = analyze_svg(svg_text)
            if issues:
                file_issues.append((idx, caption, issues))
                total_issues += len(issues)

        if file_issues:
            files_with_issues += 1
            rel = fpath.relative_to(BASE)
            all_results.append((str(rel), file_issues))

    # Print results sorted by number of issues (most first)
    all_results.sort(key=lambda x: sum(len(fi[2]) for fi in x[1]), reverse=True)

    for rel_path, file_issues in all_results:
        total_file = sum(len(fi[2]) for fi in file_issues)
        print(f"{'='*80}")
        print(f"FILE: {rel_path} ({total_file} issues)")
        for idx, caption, issues in file_issues:
            cap_str = f" - \"{caption}\"" if caption else ""
            print(f"  SVG #{idx+1}{cap_str}")
            for issue in issues:
                print(f"    {issue}")
        print()

    print(f"{'='*80}")
    print(f"SUMMARY: {total_svgs} SVGs scanned across {len(html_files)} files")
    print(f"  {files_with_issues} files with issues")
    print(f"  {total_issues} total overlap issues found")


if __name__ == '__main__':
    main()
