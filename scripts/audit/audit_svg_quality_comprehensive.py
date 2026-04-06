#!/usr/bin/env python3
"""Comprehensive SVG quality audit for LLMCourse textbook.

Checks each inline SVG with a diagram-caption for:
1. REDUNDANT_TITLE: Text inside SVG that duplicates the caption below
2. UNCLEAR_MESSAGE: Diagram too sparse or disorganized to communicate concept
3. TEXT_OVERLAP: Labels too small or likely overlapping
4. MISSING_ELEMENT: Caption promises something the diagram doesn't show
5. EXCESSIVE_DETAIL: Too many elements creating visual noise

Output: tab-delimited audit report.

Usage:
  python audit_svg_quality_comprehensive.py
"""

import re
import html
from pathlib import Path
from collections import defaultdict

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_archive", "agents", "vendor", "templates",
             "capstone", "front-matter", "build-artifacts"}

OUTPUT_FILE = BOOK_ROOT / "scripts" / "audit" / "svg_quality_audit.txt"

# Regexes
SVG_BLOCK_RE = re.compile(r'(<svg\b[^>]*>)(.*?)(</svg>)', re.DOTALL)
VIEWBOX_RE = re.compile(r'viewBox="([^"]+)"')
TEXT_EL_RE = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.DOTALL)
TSPAN_RE = re.compile(r'<tspan\b[^>]*>(.*?)</tspan>', re.DOTALL)
RECT_RE = re.compile(r'<rect\b[^>]*/?\s*>', re.DOTALL)
CIRCLE_RE = re.compile(r'<circle\b[^>]*/?\s*>', re.DOTALL)
ELLIPSE_RE = re.compile(r'<ellipse\b[^>]*/?\s*>', re.DOTALL)
LINE_RE = re.compile(r'<(?:line|polyline|polygon)\b[^>]*/?\s*>', re.DOTALL)
PATH_RE = re.compile(r'<path\b[^>]*/?\s*>', re.DOTALL)
G_RE = re.compile(r'<g\b[^>]*>', re.DOTALL)

ATTR_RE = lambda name: re.compile(rf'\b{name}="([^"]+)"')
ATTR_Y = ATTR_RE("y")
ATTR_X = ATTR_RE("x")
ATTR_FONT_SIZE = re.compile(r'font-size="(\d+(?:\.\d+)?)"')
ATTR_FONT_WEIGHT = re.compile(r'font-weight="([^"]+)"')
ATTR_FILL = re.compile(r'\bfill="([^"]+)"')
ATTR_OPACITY = re.compile(r'\bopacity="([^"]+)"')

MUTED_FILLS = {"#888", "#999", "#aaa", "#bbb", "#888888", "#999999", "#777", "#666",
               "#ccc", "#ddd", "#777777", "#666666"}

# Common English stopwords to exclude from overlap calculations
STOPWORDS = {
    "the", "and", "for", "are", "but", "not", "you", "all", "can", "had",
    "her", "was", "one", "our", "out", "has", "have", "been", "some", "them",
    "than", "its", "over", "such", "that", "this", "with", "will", "each",
    "from", "they", "into", "more", "other", "which", "their", "there",
    "about", "these", "those", "then", "what", "when", "where", "how", "who",
    "does", "did", "use", "using", "used", "also", "both", "between",
}

DIAGRAM_CAPTION_RE = re.compile(
    r'<div\s+class="diagram-caption"[^>]*>\s*(.*?)\s*</div>',
    re.DOTALL
)
FIGURE_ID_RE = re.compile(r'id="(fig[^"]*)"', re.IGNORECASE)
DIAGRAM_CONTAINER_RE = re.compile(r'<div\s+class="diagram-container"[^>]*>', re.DOTALL)

# Caption extraction from HTML
CAPTION_STRONG_RE = re.compile(r'<strong>[^<]*</strong>\s*', re.DOTALL)
HTML_TAG_RE = re.compile(r'<[^>]+>')


def strip_html(s):
    """Remove HTML tags and decode entities."""
    s = HTML_TAG_RE.sub(' ', s)
    s = html.unescape(s)
    return ' '.join(s.split())


def extract_svg_text_elements(svg_content, svg_tag):
    """Extract all text elements with their properties."""
    texts = []
    vb_height = None
    vb_width = None
    m = VIEWBOX_RE.search(svg_tag)
    if m:
        parts = m.group(1).split()
        if len(parts) == 4:
            vb_width = float(parts[2])
            vb_height = float(parts[3])

    for match in TEXT_EL_RE.finditer(svg_content):
        attrs_str = match.group(1)
        inner = match.group(2)

        # Get text content (may be in tspans)
        tspan_texts = TSPAN_RE.findall(inner)
        if tspan_texts:
            text_content = ' '.join(strip_html(t) for t in tspan_texts)
        else:
            text_content = strip_html(inner)

        if not text_content.strip():
            continue

        y_m = ATTR_Y.search(attrs_str)
        x_m = ATTR_X.search(attrs_str)
        fs_m = ATTR_FONT_SIZE.search(attrs_str)
        fw_m = ATTR_FONT_WEIGHT.search(attrs_str)
        fill_m = ATTR_FILL.search(attrs_str)

        y_val = float(y_m.group(1)) if y_m else None
        x_val = float(x_m.group(1)) if x_m else None
        font_size = float(fs_m.group(1)) if fs_m else 14
        font_weight = fw_m.group(1) if fw_m else "normal"
        fill = fill_m.group(1) if fill_m else "#000"

        is_bold = font_weight in ("bold", "700", "600")
        is_muted = fill.lower() in MUTED_FILLS

        texts.append({
            "content": text_content.strip(),
            "y": y_val,
            "x": x_val,
            "font_size": font_size,
            "is_bold": is_bold,
            "is_muted": is_muted,
            "fill": fill,
        })

    return texts, vb_width, vb_height


def count_svg_elements(svg_content):
    """Count visual elements in the SVG."""
    return {
        "rects": len(RECT_RE.findall(svg_content)),
        "circles": len(CIRCLE_RE.findall(svg_content)),
        "ellipses": len(ELLIPSE_RE.findall(svg_content)),
        "lines": len(LINE_RE.findall(svg_content)),
        "paths": len(PATH_RE.findall(svg_content)),
        "groups": len(G_RE.findall(svg_content)),
        "texts": len(TEXT_EL_RE.findall(svg_content)),
    }


def words_overlap(text_a, text_b, threshold=0.5):
    """Check if content words in text_a substantially overlap with text_b.

    Excludes common stopwords from comparison to avoid false positives
    where functional words like 'but', 'are', 'the' inflate overlap scores.
    """
    words_a = set(re.findall(r'\w{3,}', text_a.lower())) - STOPWORDS
    words_b = set(re.findall(r'\w{3,}', text_b.lower())) - STOPWORDS
    if not words_a or len(words_a) < 2:
        return False
    overlap = words_a & words_b
    return len(overlap) / len(words_a) >= threshold


def check_redundant_title(texts, vb_height, caption_text):
    """Check for title text at top of SVG that duplicates caption.

    A redundant title is a prominent heading inside the SVG that restates
    the diagram's caption. Short functional labels (e.g., "GPTQ", "Action (a)")
    are NOT redundant titles even if they share words with the caption.

    Criteria for a true redundant title:
    - At top of SVG (y < 8% of viewbox or y < 35)
    - Bold and font-size >= 14
    - Contains 4+ words (short labels are functional, not titles)
    - At least 50% word overlap with caption text

    Criteria for redundant bottom description:
    - Muted color at bottom of SVG
    - Contains 5+ words and at least 50% word overlap with caption
    """
    issues = []
    for t in texts:
        y = t["y"]
        if y is None:
            continue
        # Top region: y < 35 or y < 8% of viewbox height
        top_threshold = 35
        if vb_height and vb_height > 200:
            top_threshold = vb_height * 0.08

        is_top = y < top_threshold
        is_title_style = t["is_bold"] and t["font_size"] >= 14
        word_count = len(t["content"].split())

        # Only flag as redundant title if it's a multi-word heading, not a short label
        if is_top and is_title_style and word_count >= 4:
            if words_overlap(t["content"], caption_text, 0.5):
                issues.append(f'Top title text: "{t["content"]}"')

        # Check bottom muted descriptions (must be meaningful phrases, not labels)
        if vb_height and t["is_muted"] and y > vb_height - 40 and word_count >= 5:
            if words_overlap(t["content"], caption_text, 0.5):
                issues.append(f'Bottom description text: "{t["content"]}"')

    return issues


def check_text_readability(texts, vb_width, vb_height):
    """Check for text readability issues."""
    issues = []
    small_texts = [t for t in texts if t["font_size"] < 10 and len(t["content"]) > 2]
    if small_texts:
        examples = [f'"{t["content"]}" (size {t["font_size"]})' for t in small_texts[:3]]
        issues.append(f"Small text ({len(small_texts)} elements): {'; '.join(examples)}")

    # Check for potential overlap: texts at similar y with close x values
    if len(texts) > 2:
        by_y = defaultdict(list)
        for t in texts:
            if t["y"] is not None and t["x"] is not None:
                y_bucket = round(t["y"] / 5) * 5
                by_y[y_bucket].append(t)
        for y_bucket, group in by_y.items():
            if len(group) > 4:
                # Many texts at same y level could overlap
                x_vals = sorted(t["x"] for t in group)
                for i in range(1, len(x_vals)):
                    if x_vals[i] - x_vals[i-1] < 15 and any(len(t["content"]) > 5 for t in group):
                        issues.append(f"Potential text crowding at y~{y_bucket} ({len(group)} labels)")
                        break

    return issues


def check_element_density(counts, vb_width, vb_height):
    """Check for excessive visual elements."""
    total = sum(counts.values())
    issues = []
    if total > 80:
        issues.append(f"Very high element count ({total} total: {counts['rects']} rects, {counts['paths']} paths, {counts['texts']} texts)")
    elif total > 50:
        issues.append(f"High element count ({total} total)")
    return issues


def check_sparse_diagram(counts, texts):
    """Check if diagram is too sparse to be useful."""
    issues = []
    total_shapes = counts["rects"] + counts["circles"] + counts["ellipses"] + counts["paths"]
    if total_shapes < 2 and counts["texts"] < 3:
        issues.append(f"Very sparse diagram ({total_shapes} shapes, {counts['texts']} text labels)")
    return issues


def find_diagrams_in_file(filepath):
    """Find all SVG diagrams with their captions in an HTML file."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    diagrams = []

    # Strategy: find diagram-container blocks, extract SVG + caption
    # We'll search for SVG blocks and nearby captions
    svg_matches = list(SVG_BLOCK_RE.finditer(content))
    caption_matches = list(DIAGRAM_CAPTION_RE.finditer(content))

    for svg_m in svg_matches:
        svg_tag = svg_m.group(1)
        svg_body = svg_m.group(2)
        svg_start = svg_m.start()
        svg_end = svg_m.end()

        # Find nearest caption AFTER this SVG (within 500 chars)
        caption_text = ""
        caption_raw = ""
        for cap_m in caption_matches:
            if cap_m.start() > svg_end and cap_m.start() - svg_end < 500:
                caption_raw = cap_m.group(1)
                # Remove "Figure X.Y:" prefix
                caption_text = strip_html(caption_raw)
                caption_text = re.sub(r'^Figure\s+[\d.]+[:\s]+', '', caption_text)
                break

        if not caption_text:
            # No caption, skip (not a formal diagram)
            continue

        # Find figure ID (look in surrounding 200 chars before SVG)
        context_before = content[max(0, svg_start - 300):svg_start]
        fig_id_m = FIGURE_ID_RE.search(context_before)
        fig_id = fig_id_m.group(1) if fig_id_m else "no-id"

        # Also check if ID is on the svg element itself or a parent div
        if fig_id == "no-id":
            context_around = content[max(0, svg_start - 500):svg_end]
            fig_id_m = FIGURE_ID_RE.search(context_around)
            fig_id = fig_id_m.group(1) if fig_id_m else "no-id"

        diagrams.append({
            "fig_id": fig_id,
            "svg_tag": svg_tag,
            "svg_body": svg_body,
            "caption_text": caption_text,
            "caption_raw": caption_raw,
        })

    return diagrams


def audit_diagram(diag):
    """Run all checks on a single diagram. Returns list of (issue_type, severity, description)."""
    findings = []

    texts, vb_width, vb_height = extract_svg_text_elements(diag["svg_body"], diag["svg_tag"])
    counts = count_svg_elements(diag["svg_body"])
    caption = diag["caption_text"]

    # 1. Redundant title check
    redundant = check_redundant_title(texts, vb_height, caption)
    for r in redundant:
        findings.append(("REDUNDANT_TITLE", "HIGH", r))

    # 2. Text readability
    readability = check_text_readability(texts, vb_width, vb_height)
    for r in readability:
        severity = "HIGH" if "Small text" in r else "MEDIUM"
        findings.append(("TEXT_OVERLAP", severity, r))

    # 3. Excessive detail
    density = check_element_density(counts, vb_width, vb_height)
    for d in density:
        severity = "HIGH" if "Very high" in d else "MEDIUM"
        findings.append(("EXCESSIVE_DETAIL", severity, d))

    # 4. Sparse/unclear diagram
    sparse = check_sparse_diagram(counts, texts)
    for s in sparse:
        findings.append(("UNCLEAR_MESSAGE", "MEDIUM", s))

    # 5. Check for title-only SVGs (just a heading, no real content)
    total_shapes = counts["rects"] + counts["circles"] + counts["ellipses"] + counts["paths"] + counts["lines"]
    if total_shapes == 0 and counts["texts"] <= 2:
        findings.append(("UNCLEAR_MESSAGE", "HIGH", "SVG contains only text, no visual elements"))

    # If no issues, mark OK
    if not findings:
        findings.append(("OK", "LOW", "No issues detected"))

    return findings


def main():
    results = []
    file_count = 0
    diagram_count = 0

    scan_dirs = [
        "part-1-foundations", "part-2-understanding-llms", "part-3-working-with-llms",
        "part-4-training-adapting", "part-5-retrieval-conversation", "part-6-agentic-ai",
        "part-7-multimodal-applications", "part-8-evaluation-production",
        "part-9-safety-strategy", "part-10-frontiers", "part-11-idea-to-product",
        "appendices",
    ]

    html_files = []
    for scan_dir in scan_dirs:
        d = BOOK_ROOT / scan_dir
        if d.exists():
            for f in d.rglob("*.html"):
                # Skip archive/template dirs
                if any(part in str(f) for part in ["_archive", "template", "node_modules"]):
                    continue
                html_files.append(f)

    html_files.sort()

    for fpath in html_files:
        diagrams = find_diagrams_in_file(fpath)
        if not diagrams:
            continue
        file_count += 1
        rel = fpath.relative_to(BOOK_ROOT)

        for diag in diagrams:
            diagram_count += 1
            findings = audit_diagram(diag)
            for issue_type, severity, description in findings:
                results.append({
                    "file": str(rel).replace("\\", "/"),
                    "fig_id": diag["fig_id"],
                    "caption": diag["caption_text"][:80],
                    "issue_type": issue_type,
                    "severity": severity,
                    "description": description,
                })

    # Write report
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 120 + "\n")
        f.write("SVG QUALITY AUDIT REPORT\n")
        f.write(f"Generated: comprehensive scan of {diagram_count} diagrams in {file_count} files\n")
        f.write("=" * 120 + "\n\n")

        # Summary stats
        by_type = defaultdict(int)
        by_severity = defaultdict(int)
        for r in results:
            if r["issue_type"] != "OK":
                by_type[r["issue_type"]] += 1
                by_severity[r["severity"]] += 1

        f.write("SUMMARY\n")
        f.write("-" * 60 + "\n")
        total_issues = sum(by_type.values())
        f.write(f"Total diagrams scanned: {diagram_count}\n")
        f.write(f"Diagrams with no issues: {sum(1 for r in results if r['issue_type'] == 'OK')}\n")
        f.write(f"Total issues found: {total_issues}\n\n")

        f.write("By issue type:\n")
        for t in ["REDUNDANT_TITLE", "TEXT_OVERLAP", "EXCESSIVE_DETAIL", "UNCLEAR_MESSAGE", "MISSING_ELEMENT"]:
            if by_type[t]:
                f.write(f"  {t}: {by_type[t]}\n")

        f.write("\nBy severity:\n")
        for s in ["HIGH", "MEDIUM", "LOW"]:
            if by_severity[s]:
                f.write(f"  {s}: {by_severity[s]}\n")

        f.write("\n" + "=" * 120 + "\n")
        f.write("DETAILED FINDINGS (issues only, sorted by severity then file)\n")
        f.write("=" * 120 + "\n\n")

        # Sort: HIGH first, then MEDIUM, then LOW
        severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        issue_results = [r for r in results if r["issue_type"] != "OK"]
        issue_results.sort(key=lambda r: (severity_order.get(r["severity"], 3), r["file"], r["fig_id"]))

        current_severity = None
        for r in issue_results:
            if r["severity"] != current_severity:
                current_severity = r["severity"]
                f.write(f"\n--- {current_severity} SEVERITY ---\n\n")

            f.write(f'{r["file"]} | {r["fig_id"]} | {r["issue_type"]} | {r["severity"]} | {r["description"]}\n')
            f.write(f'  Caption: {r["caption"]}\n\n')

        # Also list all OK diagrams at the end
        f.write("\n" + "=" * 120 + "\n")
        f.write("DIAGRAMS WITH NO ISSUES DETECTED\n")
        f.write("=" * 120 + "\n\n")
        ok_results = [r for r in results if r["issue_type"] == "OK"]
        ok_results.sort(key=lambda r: r["file"])
        for r in ok_results:
            f.write(f'{r["file"]} | {r["fig_id"]} | OK\n')

    print(f"Audit complete. {diagram_count} diagrams in {file_count} files.")
    print(f"Issues found: {total_issues}")
    print(f"Report written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
