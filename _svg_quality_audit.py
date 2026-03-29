#!/usr/bin/env python3
"""SVG Quality Audit for LLMCourse textbook.

Scans all HTML files for inline SVGs and checks each for common quality issues:
  - Missing viewBox attribute
  - Hard-coded width/height without viewBox (not responsive)
  - Missing accessibility (no role="img" or aria-label)
  - Very small or very large coordinate systems
  - Missing stroke/fill on graphical elements that need them
  - TASK-026: text labels without dashed annotation lines (stroke-dasharray)

Reports a quality score per SVG and identifies the 13 worst-quality SVGs.
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict

# ── Configuration ──────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
HTML_GLOB = "**/*.html"
TOP_N_WORST = 13

# Elements that normally need stroke or fill to be visible
GRAPHICAL_ELEMENTS = {"rect", "circle", "ellipse", "line", "polyline", "polygon", "path"}

# ── Helpers ────────────────────────────────────────────────────────────────

def extract_inline_svgs(html_path: Path):
    """Yield (start_line, svg_source) for every inline <svg>...</svg> in a file."""
    text = html_path.read_text(encoding="utf-8", errors="replace")
    # Match balanced <svg ...> ... </svg> (non-greedy, DOTALL)
    for m in re.finditer(r"<svg\b[^>]*>.*?</svg>", text, re.DOTALL):
        start = text[:m.start()].count("\n") + 1
        yield start, m.group(0)


def parse_svg_tag_attrs(svg_source: str):
    """Return dict of attributes on the opening <svg> tag."""
    m = re.match(r"<svg\b([^>]*)>", svg_source, re.DOTALL)
    if not m:
        return {}
    attr_str = m.group(1)
    attrs = {}
    for am in re.finditer(r'(\w[\w-]*)=["\']([^"\']*)["\']', attr_str):
        attrs[am.group(1)] = am.group(2)
    return attrs


def count_elements(svg_source: str, tag_names: set):
    """Count occurrences of given element tags inside the SVG."""
    total = 0
    for tag in tag_names:
        total += len(re.findall(rf"<{tag}\b", svg_source))
    return total


def count_text_elements(svg_source: str):
    """Count <text> elements."""
    return len(re.findall(r"<text\b", svg_source))


def has_dasharray(svg_source: str):
    """Check whether the SVG contains any stroke-dasharray attribute."""
    return "stroke-dasharray" in svg_source


def elements_missing_stroke_fill(svg_source: str):
    """Return count of graphical elements that have neither stroke nor fill set."""
    missing = 0
    for tag in GRAPHICAL_ELEMENTS:
        for m in re.finditer(rf"<{tag}\b([^>]*)/?>" , svg_source):
            attr_str = m.group(1)
            has_stroke = "stroke=" in attr_str or "stroke:" in attr_str
            has_fill = "fill=" in attr_str or "fill:" in attr_str
            if not has_stroke and not has_fill:
                missing += 1
    return missing


def viewbox_dimensions(viewbox_str: str):
    """Parse viewBox and return (width, height) or None."""
    parts = viewbox_str.strip().replace(",", " ").split()
    if len(parts) == 4:
        try:
            return float(parts[2]), float(parts[3])
        except ValueError:
            return None
    return None


def check_parent_accessibility(html_path: Path, svg_start_line: int):
    """Check whether the SVG or a parent wrapper has role='img' / aria-label."""
    text = html_path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    # Look at the 5 lines before the SVG start for wrapper attributes
    context_start = max(0, svg_start_line - 6)
    context = "\n".join(lines[context_start:svg_start_line + 2])
    has_role = 'role="img"' in context or "role='img'" in context
    has_aria = "aria-label=" in context
    has_title = "<title>" in context or "<title " in context
    return has_role, has_aria, has_title


# ── Main Audit ─────────────────────────────────────────────────────────────

def audit_svg(html_path: Path, start_line: int, svg_source: str):
    """Audit a single inline SVG and return (score, issues_list, metadata)."""
    issues = []
    attrs = parse_svg_tag_attrs(svg_source)

    # 1. viewBox check
    has_viewbox = "viewBox" in attrs or "viewbox" in attrs
    viewbox_val = attrs.get("viewBox", attrs.get("viewbox", ""))
    if not has_viewbox:
        issues.append(("CRITICAL", "Missing viewBox attribute"))

    # 2. Hard-coded dimensions without viewBox
    has_width = "width" in attrs
    has_height = "height" in attrs
    if (has_width or has_height) and not has_viewbox:
        issues.append(("HIGH", "Hard-coded width/height without viewBox (not responsive)"))

    # 3. Coordinate system size
    if has_viewbox and viewbox_val:
        dims = viewbox_dimensions(viewbox_val)
        if dims:
            w, h = dims
            if w < 50 or h < 50:
                issues.append(("MEDIUM", f"Very small viewBox ({w}x{h}), may lack detail"))
            if w > 2000 or h > 2000:
                issues.append(("MEDIUM", f"Very large viewBox ({w}x{h}), may cause performance issues"))

    # 4. Accessibility
    has_role, has_aria, has_title = check_parent_accessibility(html_path, start_line)
    svg_has_role = 'role="img"' in svg_source[:200]
    svg_has_aria = "aria-label=" in svg_source[:300]
    svg_has_title_el = "<title>" in svg_source[:500]
    if not (has_role or svg_has_role):
        issues.append(("HIGH", "Missing role='img' on SVG or wrapper"))
    if not (has_aria or svg_has_aria) and not (has_title or svg_has_title_el):
        issues.append(("HIGH", "Missing aria-label or <title> for screen readers"))

    # 5. Missing stroke/fill
    missing_sf = elements_missing_stroke_fill(svg_source)
    if missing_sf > 0:
        issues.append(("MEDIUM", f"{missing_sf} graphical element(s) missing both stroke and fill"))

    # 6. Element counts
    n_graphical = count_elements(svg_source, GRAPHICAL_ELEMENTS)
    n_text = count_text_elements(svg_source)

    # 7. TASK-026: text labels without dashed annotation lines
    has_dashed = has_dasharray(svg_source)
    needs_annotation = n_text >= 2 and n_graphical >= 2  # has labels and shapes
    if needs_annotation and not has_dashed:
        issues.append(("LOW", "TASK-026: Has text labels + shapes but no dashed annotation lines (stroke-dasharray)"))

    # 8. SVG size (character count, proxy for complexity)
    svg_len = len(svg_source)

    # ── Scoring ──
    # Start at 100, deduct per issue severity
    score = 100
    severity_deductions = {"CRITICAL": 30, "HIGH": 20, "MEDIUM": 10, "LOW": 5}
    for sev, _ in issues:
        score -= severity_deductions.get(sev, 5)
    score = max(0, score)

    metadata = {
        "file": str(html_path.relative_to(PROJECT_ROOT)),
        "line": start_line,
        "viewBox": viewbox_val if has_viewbox else None,
        "graphical_elements": n_graphical,
        "text_elements": n_text,
        "has_dasharray": has_dashed,
        "char_count": svg_len,
    }

    return score, issues, metadata


def main():
    print("=" * 80)
    print("SVG QUALITY AUDIT for LLMCourse Textbook")
    print("=" * 80)
    print()

    html_files = sorted(PROJECT_ROOT.glob(HTML_GLOB))
    print(f"Scanning {len(html_files)} HTML files for inline SVGs...")
    print()

    all_results = []
    files_with_svgs = 0
    total_svgs = 0

    severity_totals = defaultdict(int)
    issue_type_counts = defaultdict(int)

    for html_path in html_files:
        svgs = list(extract_inline_svgs(html_path))
        if not svgs:
            continue
        files_with_svgs += 1
        for start_line, svg_src in svgs:
            total_svgs += 1
            score, issues, meta = audit_svg(html_path, start_line, svg_src)
            all_results.append((score, issues, meta))
            for sev, desc in issues:
                severity_totals[sev] += 1
                issue_type_counts[desc.split(":")[0] if "TASK-026" not in desc else "TASK-026"] += 1

    print(f"Found {total_svgs} inline SVGs across {files_with_svgs} HTML files.")
    print()

    # ── Summary Statistics ──
    print("-" * 80)
    print("ISSUE SEVERITY SUMMARY")
    print("-" * 80)
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = severity_totals.get(sev, 0)
        print(f"  {sev:10s}: {count:4d}")
    print()

    print("-" * 80)
    print("ISSUE TYPE BREAKDOWN")
    print("-" * 80)
    for desc, count in sorted(issue_type_counts.items(), key=lambda x: -x[1]):
        print(f"  [{count:4d}] {desc}")
    print()

    # ── Score Distribution ──
    scores = [r[0] for r in all_results]
    if scores:
        avg_score = sum(scores) / len(scores)
        buckets = {"90-100 (Good)": 0, "70-89 (Fair)": 0, "50-69 (Poor)": 0, "0-49 (Bad)": 0}
        for s in scores:
            if s >= 90:
                buckets["90-100 (Good)"] += 1
            elif s >= 70:
                buckets["70-89 (Fair)"] += 1
            elif s >= 50:
                buckets["50-69 (Poor)"] += 1
            else:
                buckets["0-49 (Bad)"] += 1

        print("-" * 80)
        print("SCORE DISTRIBUTION")
        print("-" * 80)
        print(f"  Average score: {avg_score:.1f}/100")
        for bucket, count in buckets.items():
            bar = "#" * (count // 2)
            print(f"  {bucket:20s}: {count:4d}  {bar}")
        print()

    # ── Top 13 Worst SVGs ──
    all_results.sort(key=lambda r: r[0])
    worst = all_results[:TOP_N_WORST]

    print("=" * 80)
    print(f"TOP {TOP_N_WORST} WORST-QUALITY SVGs")
    print("=" * 80)
    for rank, (score, issues, meta) in enumerate(worst, 1):
        print(f"\n  #{rank}  Score: {score}/100")
        print(f"       File: {meta['file']}  (line {meta['line']})")
        print(f"       viewBox: {meta['viewBox'] or 'MISSING'}")
        print(f"       Elements: {meta['graphical_elements']} graphical, {meta['text_elements']} text, {meta['char_count']} chars")
        print(f"       Has dasharray: {meta['has_dasharray']}")
        for sev, desc in issues:
            print(f"       [{sev}] {desc}")

    # ── TASK-026 Report: SVGs needing dashed annotation lines ──
    task026 = [
        (s, iss, m) for s, iss, m in all_results
        if any("TASK-026" in d for _, d in iss)
    ]
    print()
    print("=" * 80)
    print(f"TASK-026: SVGs WITH TEXT LABELS BUT NO DASHED ANNOTATION LINES ({len(task026)} found)")
    print("=" * 80)
    # Show first 25, then just counts per directory
    for i, (score, issues, meta) in enumerate(task026[:25]):
        print(f"  [{score}/100] {meta['file']}:{meta['line']}  "
              f"({meta['text_elements']} text, {meta['graphical_elements']} shapes)")
    if len(task026) > 25:
        print(f"  ... and {len(task026) - 25} more.")
    print()

    # Group by part directory
    part_counts = defaultdict(int)
    for _, _, m in task026:
        parts = m["file"].split(os.sep)
        top = parts[0] if parts else "other"
        part_counts[top] += 1
    print("  By top-level directory:")
    for d, c in sorted(part_counts.items(), key=lambda x: -x[1]):
        print(f"    {d}: {c}")

    # ── Standalone SVG files ──
    print()
    print("-" * 80)
    print("STANDALONE .svg FILES (icons, etc.)")
    print("-" * 80)
    svg_files = sorted(PROJECT_ROOT.glob("**/*.svg"))
    for sf in svg_files:
        rel = sf.relative_to(PROJECT_ROOT)
        text = sf.read_text(encoding="utf-8", errors="replace")
        attrs = parse_svg_tag_attrs(text)
        has_vb = "viewBox" in attrs or "viewbox" in attrs
        has_aria = "aria-label=" in text[:300]
        issues_list = []
        if not has_vb:
            issues_list.append("no viewBox")
        if not has_aria:
            issues_list.append("no aria-label")
        status = ", ".join(issues_list) if issues_list else "OK"
        print(f"  {rel}: {status}")

    # ── Save JSON report ──
    json_report = {
        "total_inline_svgs": total_svgs,
        "files_with_svgs": files_with_svgs,
        "average_score": round(avg_score, 1) if scores else 0,
        "severity_totals": dict(severity_totals),
        "worst_13": [
            {
                "rank": i + 1,
                "score": score,
                "file": meta["file"],
                "line": meta["line"],
                "issues": [{"severity": s, "description": d} for s, d in issues],
                "metadata": meta,
            }
            for i, (score, issues, meta) in enumerate(worst)
        ],
        "task026_count": len(task026),
    }
    report_path = PROJECT_ROOT / "_svg_quality_report.json"
    report_path.write_text(json.dumps(json_report, indent=2), encoding="utf-8")
    print(f"\nJSON report saved to: {report_path}")
    print()


if __name__ == "__main__":
    main()
