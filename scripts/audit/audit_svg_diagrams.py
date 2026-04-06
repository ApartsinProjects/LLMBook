#!/usr/bin/env python3
"""Audit inline SVG diagrams and classify them as Mermaid conversion candidates.

Scans all section-*.html and index.html files (excluding _archive) across all
parts and appendices, extracts inline <svg> blocks, and classifies each into
categories indicating whether it is a good, possible, or poor candidate for
Mermaid diagram conversion.

Categories:
  GOOD candidates:  flowchart, architecture, sequence, tree
  POSSIBLE:         comparison, matrix_table
  KEEP as SVG:      math_diagram, line_graph, neural_network,
                    icon_decorative, complex_visual

Outputs results to console and a JSON report.
"""

import json
import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
REPORT_PATH = BOOK_ROOT / "scripts" / "audit" / "svg_diagram_report.json"

# Directories to scan
SCAN_DIRS = [
    BOOK_ROOT / "part-1-foundations",
    BOOK_ROOT / "part-2-understanding-llms",
    BOOK_ROOT / "part-3-working-with-llms",
    BOOK_ROOT / "part-4-training-adapting",
    BOOK_ROOT / "part-5-retrieval-conversation",
    BOOK_ROOT / "part-6-agentic-ai",
    BOOK_ROOT / "part-7-multimodal-applications",
    BOOK_ROOT / "part-8-evaluation-production",
    BOOK_ROOT / "part-9-safety-strategy",
    BOOK_ROOT / "part-10-frontiers",
    BOOK_ROOT / "part-11-idea-to-product",
    BOOK_ROOT / "appendices",
    BOOK_ROOT / "front-matter",
]

# ── Helpers ──────────────────────────────────────────────────────────────

def find_html_files():
    """Collect all section-*.html and index.html files, excluding _archive."""
    files = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for html_file in scan_dir.rglob("*.html"):
            if "_archive" in str(html_file):
                continue
            name = html_file.name
            if name.startswith("section-") or name == "index.html":
                files.append(html_file)
    return sorted(files)


def extract_svgs(html_content, file_path):
    """Extract all <svg...>...</svg> blocks from HTML content.

    Returns list of dicts with svg_text, start_pos, and surrounding context
    for figcaption extraction.
    """
    results = []
    # Use a non-greedy match that handles nested tags by matching balanced svg
    # Simple regex approach: find <svg and then match to the corresponding </svg>
    pattern = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL | re.IGNORECASE)
    for match in pattern.finditer(html_content):
        svg_text = match.group(0)
        start = match.start()
        end = match.end()

        # Look for surrounding <figure> and <figcaption>
        # Search backwards up to 500 chars for <figure, and forward 500 chars for </figcaption>
        context_before = html_content[max(0, start - 500):start]
        context_after = html_content[end:end + 500]

        figcaption = None
        # Check before (caption above SVG)
        cap_match = re.search(
            r'<figcaption[^>]*>(.*?)</figcaption>',
            context_before, re.DOTALL | re.IGNORECASE
        )
        if cap_match:
            figcaption = re.sub(r'<[^>]+>', '', cap_match.group(1)).strip()

        # Check after (caption below SVG)
        if not figcaption:
            cap_match = re.search(
                r'<figcaption[^>]*>(.*?)</figcaption>',
                context_after, re.DOTALL | re.IGNORECASE
            )
            if cap_match:
                figcaption = re.sub(r'<[^>]+>', '', cap_match.group(1)).strip()

        results.append({
            "svg_text": svg_text,
            "figcaption": figcaption,
        })
    return results


def parse_svg_dimensions(svg_text):
    """Extract viewBox or width/height from the SVG opening tag."""
    dims = {}
    vb = re.search(r'viewBox\s*=\s*"([^"]*)"', svg_text)
    if vb:
        dims["viewBox"] = vb.group(1)
        parts = vb.group(1).split()
        if len(parts) == 4:
            dims["width"] = float(parts[2])
            dims["height"] = float(parts[3])
    w = re.search(r'\bwidth\s*=\s*"([^"]*)"', svg_text)
    h = re.search(r'\bheight\s*=\s*"([^"]*)"', svg_text)
    if w:
        try:
            dims.setdefault("width", float(re.sub(r'[^0-9.]', '', w.group(1))))
        except ValueError:
            pass
    if h:
        try:
            dims.setdefault("height", float(re.sub(r'[^0-9.]', '', h.group(1))))
        except ValueError:
            pass
    return dims


def count_elements(svg_text):
    """Count key SVG elements."""
    counts = {}
    for tag in ("rect", "text", "line", "path", "circle", "ellipse",
                "polygon", "polyline", "marker", "g", "use",
                "linearGradient", "radialGradient", "image", "foreignObject"):
        counts[tag] = len(re.findall(rf'<{tag}\b', svg_text, re.IGNORECASE))
    return counts


def has_arrow_markers(svg_text):
    """Check if SVG defines arrow markers (strong signal for flowcharts)."""
    return bool(re.search(r'<marker\b', svg_text, re.IGNORECASE))


def has_axis_pattern(svg_text):
    """Check for axis-like patterns: long lines with tick marks or axis labels."""
    # Look for common axis patterns: "x-axis", "y-axis", "axis" in text,
    # or repeated short perpendicular lines suggesting tick marks
    has_axis_text = bool(re.search(r'(?:x.axis|y.axis|axis|Epoch|Loss|Accuracy|Score)',
                                    svg_text, re.IGNORECASE))
    # Many short lines in a row suggest tick marks
    line_count = len(re.findall(r'<line\b', svg_text, re.IGNORECASE))
    has_many_lines = line_count > 15
    return has_axis_text and has_many_lines


def has_grid_pattern(counts):
    """Check for grid/matrix layout: many rects in a regular pattern."""
    return counts.get("rect", 0) > 12 and counts.get("text", 0) > 12


def has_neural_network_pattern(svg_text, counts):
    """Detect neural network diagrams: many circles with many connections."""
    circles = counts.get("circle", 0) + counts.get("ellipse", 0)
    lines = counts.get("line", 0) + counts.get("path", 0)
    has_layer_text = bool(re.search(
        r'(?:hidden|input|output)\s*layer|neuron|activation|softmax|dense|relu',
        svg_text, re.IGNORECASE
    ))
    return circles > 8 and lines > circles * 2 and (has_layer_text or circles > 15)


def has_gradient_complexity(svg_text, counts):
    """Check for complex visual styling that Mermaid cannot reproduce."""
    gradients = counts.get("linearGradient", 0) + counts.get("radialGradient", 0)
    has_filters = bool(re.search(r'<filter\b', svg_text, re.IGNORECASE))
    has_clip_path = bool(re.search(r'<clipPath\b', svg_text, re.IGNORECASE))
    return gradients > 3 or has_filters or (has_clip_path and gradients > 1)


def has_flowchart_signals(svg_text, counts):
    """Detect flowchart-like patterns."""
    rects = counts.get("rect", 0)
    texts = counts.get("text", 0)
    arrows = has_arrow_markers(svg_text)
    paths = counts.get("path", 0) + counts.get("line", 0)
    # Flowcharts: boxes + labels + arrows/connections
    return arrows and rects >= 3 and texts >= 3 and paths >= 2


def has_sequence_signals(svg_text, dims):
    """Detect sequence diagram patterns."""
    # Sequence diagrams are typically wide, have vertical dashed lines, horizontal arrows
    width = dims.get("width", 0)
    height = dims.get("height", 0)
    has_dashed = bool(re.search(r'stroke-dasharray', svg_text, re.IGNORECASE))
    has_lifeline_text = bool(re.search(
        r'(?:User|Client|Server|API|Service|Agent|System|Request|Response)',
        svg_text, re.IGNORECASE
    ))
    wide_aspect = width > 0 and height > 0 and width / height > 1.5
    return has_dashed and has_lifeline_text and wide_aspect


def has_tree_signals(svg_text, counts):
    """Detect tree/hierarchy patterns."""
    has_tree_text = bool(re.search(r'(?:root|parent|child|leaf|node|branch)',
                                    svg_text, re.IGNORECASE))
    # Trees: moderate circles/rects connected by paths, more vertical layout
    nodes = counts.get("circle", 0) + counts.get("rect", 0)
    connections = counts.get("path", 0) + counts.get("line", 0)
    return has_tree_text and nodes >= 4 and connections >= 3


def has_comparison_signals(svg_text, counts):
    """Detect side-by-side comparison layouts."""
    has_vs = bool(re.search(r'(?:\bvs\.?\b|\bversus\b|compared|before.*after|left.*right)',
                             svg_text, re.IGNORECASE))
    rects = counts.get("rect", 0)
    texts = counts.get("text", 0)
    return has_vs and rects >= 2 and texts >= 4


def has_math_signals(svg_text):
    """Detect mathematical diagrams."""
    math_patterns = bool(re.search(
        r'(?:sin|cos|tan|log|exp|sigmoid|tanh|relu|softmax|probability|gradient|'
        r'derivative|integral|matrix|vector|scalar|norm|dot.product|cross.product|'
        r'eigenvalue|distribution|gaussian|normal\s+dist|loss\s+function|'
        r'convergence|divergence|contour|manifold|hyperplane)',
        svg_text, re.IGNORECASE
    ))
    # Coordinate axes
    has_coords = bool(re.search(r'(?:x[12]?\s*=\s*"0"|(?:0,0).*(?:\d{2,3},\d{2,3}))',
                                 svg_text))
    return math_patterns


def is_small_decorative(svg_text, counts, dims):
    """Check if SVG is a small decorative icon."""
    char_count = len(svg_text)
    total_elements = sum(counts.values())
    width = dims.get("width", 999)
    height = dims.get("height", 999)
    return (char_count < 1500 and total_elements < 10) or (width < 50 and height < 50)


# ── Main classification ─────────────────────────────────────────────────

def classify_svg(svg_text):
    """Classify an SVG into a category with confidence."""
    counts = count_elements(svg_text)
    dims = parse_svg_dimensions(svg_text)
    char_count = len(svg_text)

    # Small decorative icons
    if is_small_decorative(svg_text, counts, dims):
        return "icon_decorative", "high", counts, dims

    # Neural network
    if has_neural_network_pattern(svg_text, counts):
        return "neural_network", "high", counts, dims

    # Line graph / chart with axes
    if has_axis_pattern(svg_text):
        return "line_graph", "high", counts, dims

    # Math diagram
    if has_math_signals(svg_text) and not has_flowchart_signals(svg_text, counts):
        confidence = "high" if has_axis_pattern(svg_text) else "medium"
        return "math_diagram", confidence, counts, dims

    # Complex visual (heavy gradients, filters)
    if has_gradient_complexity(svg_text, counts):
        return "complex_visual", "medium", counts, dims

    # Sequence diagram
    if has_sequence_signals(svg_text, dims):
        return "sequence", "medium", counts, dims

    # Tree / hierarchy
    if has_tree_signals(svg_text, counts):
        return "tree", "medium", counts, dims

    # Flowchart (strong signal: arrows + boxes + labels)
    if has_flowchart_signals(svg_text, counts):
        # Distinguish architecture from flowchart
        has_arch_text = bool(re.search(
            r'(?:layer|component|module|encoder|decoder|embedding|attention|'
            r'feed.forward|input|output|stack|block|head)',
            svg_text, re.IGNORECASE
        ))
        rects = counts.get("rect", 0)
        if has_arch_text and rects >= 6:
            return "architecture", "medium", counts, dims
        return "flowchart", "high", counts, dims

    # Comparison
    if has_comparison_signals(svg_text, counts):
        return "comparison", "medium", counts, dims

    # Matrix / table
    if has_grid_pattern(counts):
        return "matrix_table", "medium", counts, dims

    # Fallback: if it has boxes and text but no clear arrows, it might be architecture
    rects = counts.get("rect", 0)
    texts = counts.get("text", 0)
    paths = counts.get("path", 0) + counts.get("line", 0)
    if rects >= 4 and texts >= 4 and paths >= 2:
        # Large and connected: architecture
        if char_count > 5000:
            return "architecture", "low", counts, dims
        return "flowchart", "low", counts, dims

    # Very large SVGs with many elements are probably complex visuals
    if char_count > 8000:
        return "complex_visual", "low", counts, dims

    # Default: keep as SVG
    return "complex_visual", "low", counts, dims


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    html_files = find_html_files()
    print(f"Scanning {len(html_files)} HTML files for inline SVG diagrams...\n")

    all_entries = []

    for html_file in html_files:
        rel_path = str(html_file.relative_to(BOOK_ROOT)).replace("\\", "/")
        try:
            content = html_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  WARNING: Could not read {rel_path}: {e}")
            continue

        svgs = extract_svgs(content, html_file)
        if not svgs:
            continue

        for i, svg_info in enumerate(svgs, 1):
            svg_text = svg_info["svg_text"]
            figcaption = svg_info["figcaption"]
            category, confidence, counts, dims = classify_svg(svg_text)

            entry = {
                "file": rel_path,
                "svg_index": i,
                "figcaption": figcaption,
                "dimensions": dims,
                "char_count": len(svg_text),
                "element_counts": {
                    "rect": counts.get("rect", 0),
                    "text": counts.get("text", 0),
                    "line": counts.get("line", 0),
                    "path": counts.get("path", 0),
                    "circle": counts.get("circle", 0),
                    "ellipse": counts.get("ellipse", 0),
                    "marker": counts.get("marker", 0),
                    "polygon": counts.get("polygon", 0),
                    "polyline": counts.get("polyline", 0),
                    "g": counts.get("g", 0),
                    "gradient": counts.get("linearGradient", 0) + counts.get("radialGradient", 0),
                },
                "category": category,
                "confidence": confidence,
            }
            all_entries.append(entry)

    # ── Summary ──────────────────────────────────────────────────────────
    GOOD = {"flowchart", "architecture", "sequence", "tree"}
    POSSIBLE = {"comparison", "matrix_table"}
    KEEP = {"math_diagram", "line_graph", "neural_network",
            "icon_decorative", "complex_visual"}

    cat_counts = {}
    for e in all_entries:
        cat_counts[e["category"]] = cat_counts.get(e["category"], 0) + 1

    good_list = [e for e in all_entries if e["category"] in GOOD]
    possible_list = [e for e in all_entries if e["category"] in POSSIBLE]
    keep_list = [e for e in all_entries if e["category"] in KEEP]

    # Print results
    print("=" * 80)
    print(f"  SVG DIAGRAM AUDIT REPORT")
    print(f"  Total SVGs found: {len(all_entries)}")
    print("=" * 80)

    print(f"\n  Category breakdown:")
    for cat in sorted(cat_counts.keys()):
        tier = "GOOD" if cat in GOOD else ("POSSIBLE" if cat in POSSIBLE else "KEEP")
        print(f"    {cat:<20s}  {cat_counts[cat]:>4d}  [{tier}]")

    print(f"\n{'-' * 80}")
    print(f"  GOOD candidates for Mermaid conversion ({len(good_list)}):")
    print(f"{'-' * 80}")
    for e in good_list:
        cap = (e["figcaption"] or "(no caption)")[:80]
        print(f"  [{e['confidence']:>6s}] {e['category']:<14s} {e['file']}")
        print(f"           {cap}")
        print(f"           {e['char_count']} chars, "
              f"rects={e['element_counts']['rect']}, "
              f"texts={e['element_counts']['text']}, "
              f"paths={e['element_counts']['path']}, "
              f"markers={e['element_counts']['marker']}")
        print()

    print(f"{'-' * 80}")
    print(f"  POSSIBLE candidates ({len(possible_list)}):")
    print(f"{'-' * 80}")
    for e in possible_list:
        cap = (e["figcaption"] or "(no caption)")[:80]
        print(f"  [{e['confidence']:>6s}] {e['category']:<14s} {e['file']}")
        print(f"           {cap}")
        print()

    print(f"{'-' * 80}")
    print(f"  KEEP as SVG ({len(keep_list)}):")
    print(f"{'-' * 80}")
    for e in keep_list:
        cap = (e["figcaption"] or "(no caption)")[:60]
        print(f"  [{e['confidence']:>6s}] {e['category']:<16s} {e['file']}  {cap}")

    # ── JSON report ──────────────────────────────────────────────────────
    report = {
        "total_svgs": len(all_entries),
        "category_counts": cat_counts,
        "good_candidates_count": len(good_list),
        "possible_candidates_count": len(possible_list),
        "keep_count": len(keep_list),
        "good_candidates": good_list,
        "possible_candidates": possible_list,
        "keep_as_svg": keep_list,
        "all_entries": all_entries,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n  JSON report written to: {REPORT_PATH}")
    print(f"  Done.\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
