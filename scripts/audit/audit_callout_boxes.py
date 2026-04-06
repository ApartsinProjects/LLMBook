#!/usr/bin/env python3
"""
audit_callout_boxes.py - Audit callout box markup across the LLM Course textbook.

Finds:
1. Non-standard callout classes (not in the approved list)
2. Non-standard inner markup (missing callout-title div, using p.callout-label, etc.)
3. Inline style attributes on callout divs
4. Potential callout-like divs that don't use the standard callout class pattern
"""

import os
import re
from collections import defaultdict
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
ROOT = Path(r"E:/Projects/LLMCourse")
REPORT_FILE = ROOT / "scripts" / "audit" / "callout_audit_report.txt"

STANDARD_CALLOUT_TYPES = {
    "key-insight",
    "practical-example",
    "library-shortcut",
    "tip",
    "note",
    "warning",
    "research-frontier",
    "big-picture",
    "self-check",
    "lab",
    "fun-note",
    "exercise",
}

# Patterns that look like callout boxes but aren't using the standard class
SUSPECT_CLASS_PATTERNS = [
    r"info-box", r"sidebar", r"panel", r"alert", r"highlight-box",
    r"tip-box", r"note-box", r"warning-box", r"example-box", r"hint",
    r"admonition", r"notice", r"banner", r"infobox", r"aside",
    r"callout-box", r"important", r"caution", r"danger",
]


# ── File discovery ─────────────────────────────────────────────────────────
def find_html_files(root: Path) -> list[Path]:
    """Find all section-*.html in part-*/ and appendices/, excluding _archive."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "_archive" and not d.startswith(".")]
        dp = Path(dirpath)
        rel = dp.relative_to(root).as_posix()
        if not (rel.startswith("part-") or rel.startswith("appendices/")):
            if rel != "appendices":
                continue
        for fn in sorted(filenames):
            if fn.startswith("section-") and fn.endswith(".html"):
                results.append(dp / fn)
    return sorted(results)


# ── Analysis ───────────────────────────────────────────────────────────────
def analyze_file(filepath: Path) -> dict:
    """Analyze a single HTML file for callout issues."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    issues = []
    rel = filepath.relative_to(ROOT).as_posix()

    # Find all div elements with class containing "callout"
    # Match: <div class="callout something" ...>
    callout_div_re = re.compile(
        r'<div\b([^>]*\bclass\s*=\s*"[^"]*callout[^"]*"[^>]*)>',
        re.IGNORECASE
    )

    for m in callout_div_re.finditer(text):
        tag_attrs = m.group(1)
        pos = m.start()
        line_num = text[:pos].count("\n") + 1
        # Extract class value
        cls_match = re.search(r'class\s*=\s*"([^"]*)"', tag_attrs)
        if not cls_match:
            continue
        cls_value = cls_match.group(1).strip()
        classes = cls_value.split()

        # Check 1: Is "callout" present?
        if "callout" not in classes:
            continue

        # Determine the callout type (second class after "callout")
        callout_type = None
        extra_classes = []
        for c in classes:
            if c == "callout":
                continue
            if callout_type is None:
                callout_type = c
            else:
                extra_classes.append(c)

        # Issue: non-standard callout type
        if callout_type and callout_type not in STANDARD_CALLOUT_TYPES:
            issues.append({
                "type": "NON_STANDARD_CLASS",
                "line": line_num,
                "detail": f'class="{cls_value}" (unknown type: {callout_type})',
            })

        # Issue: no callout type at all
        if callout_type is None:
            issues.append({
                "type": "MISSING_TYPE",
                "line": line_num,
                "detail": f'class="{cls_value}" (no callout type specified)',
            })

        # Issue: extra unexpected classes
        if extra_classes:
            issues.append({
                "type": "EXTRA_CLASSES",
                "line": line_num,
                "detail": f'class="{cls_value}" (extra: {", ".join(extra_classes)})',
            })

        # Check 3: Inline style on callout div
        if re.search(r'\bstyle\s*=\s*"[^"]*"', tag_attrs):
            style_val = re.search(r'style\s*=\s*"([^"]*)"', tag_attrs).group(1)
            issues.append({
                "type": "INLINE_STYLE",
                "line": line_num,
                "detail": f'class="{cls_value}" has style="{style_val}"',
            })

        # Check 2: Inner markup - look for content after this div
        # Get a chunk of text after the opening div to check inner structure
        chunk_start = m.end()
        chunk = text[chunk_start:chunk_start + 500]

        # Check for <p class="callout-label"> (non-standard)
        if re.search(r'<p\s+class\s*=\s*"callout-label"', chunk[:300]):
            issues.append({
                "type": "NON_STANDARD_INNER",
                "line": line_num,
                "detail": f'Uses <p class="callout-label"> instead of <div class="callout-title">',
            })

        # Check for missing callout-title entirely
        has_title = re.search(r'<div\s+class\s*=\s*"callout-title"', chunk[:300])
        # Also check for <h4 class="callout-title"> or <span class="callout-title">
        has_alt_title = re.search(r'<(?:h[2-6]|span|strong|p)\s+class\s*=\s*"callout-title"', chunk[:300])
        # Check if next significant content is a nested div (not callout-title)
        first_tag = re.search(r'<(div|p|h[2-6]|span|ul|ol|strong)\b[^>]*>', chunk[:200])

        if has_alt_title and not has_title:
            tag_type = re.search(r'<(h[2-6]|span|strong|p)', has_alt_title.group()).group(1)
            issues.append({
                "type": "WRONG_TITLE_ELEMENT",
                "line": line_num,
                "detail": f'Uses <{tag_type} class="callout-title"> instead of <div class="callout-title">',
            })
        elif not has_title and not has_alt_title:
            # Only flag if there's no callout-title at all in the first 300 chars
            if "callout-title" not in chunk[:300]:
                issues.append({
                    "type": "MISSING_TITLE",
                    "line": line_num,
                    "detail": f'class="{cls_value}" has no callout-title element',
                })

    # Check for callout-like divs that DON'T use the standard pattern
    suspect_re = re.compile(
        r'<div\b[^>]*\bclass\s*=\s*"([^"]*(?:' +
        "|".join(SUSPECT_CLASS_PATTERNS) +
        r')[^"]*)"[^>]*>',
        re.IGNORECASE
    )
    for m in suspect_re.finditer(text):
        cls_value = m.group(1)
        # Skip if it already has "callout" class
        if "callout" in cls_value.split():
            continue
        line_num = text[:m.start()].count("\n") + 1
        issues.append({
            "type": "SUSPECT_NON_CALLOUT",
            "line": line_num,
            "detail": f'Possible callout using non-standard class="{cls_value}"',
        })

    return {"file": rel, "issues": issues}


# ── Report generation ──────────────────────────────────────────────────────
def generate_report(results: list[dict]) -> str:
    lines = []
    lines.append("=" * 78)
    lines.append("CALLOUT BOX AUDIT REPORT")
    lines.append("=" * 78)
    lines.append("")

    # Summary stats
    total_files = len(results)
    files_with_issues = sum(1 for r in results if r["issues"])
    total_issues = sum(len(r["issues"]) for r in results)

    by_type = defaultdict(list)
    for r in results:
        for iss in r["issues"]:
            by_type[iss["type"]].append((r["file"], iss["line"], iss["detail"]))

    lines.append(f"Files scanned:      {total_files}")
    lines.append(f"Files with issues:  {files_with_issues}")
    lines.append(f"Total issues:       {total_issues}")
    lines.append("")

    lines.append("ISSUE BREAKDOWN:")
    type_labels = {
        "NON_STANDARD_CLASS": "Non-standard callout class",
        "MISSING_TYPE": "Missing callout type",
        "EXTRA_CLASSES": "Extra CSS classes on callout",
        "INLINE_STYLE": "Inline style on callout",
        "NON_STANDARD_INNER": "Non-standard inner markup (p.callout-label)",
        "WRONG_TITLE_ELEMENT": "Wrong element for callout-title",
        "MISSING_TITLE": "Missing callout-title div",
        "SUSPECT_NON_CALLOUT": "Suspect non-standard callout-like div",
    }
    for itype in [
        "NON_STANDARD_CLASS", "MISSING_TYPE", "EXTRA_CLASSES",
        "INLINE_STYLE", "NON_STANDARD_INNER", "WRONG_TITLE_ELEMENT",
        "MISSING_TITLE", "SUSPECT_NON_CALLOUT",
    ]:
        if itype in by_type:
            lines.append(f"  {type_labels.get(itype, itype):50s} {len(by_type[itype]):4d}")

    lines.append("")
    lines.append("-" * 78)

    # Detailed findings by issue type
    for itype in [
        "NON_STANDARD_CLASS", "MISSING_TYPE", "EXTRA_CLASSES",
        "INLINE_STYLE", "NON_STANDARD_INNER", "WRONG_TITLE_ELEMENT",
        "MISSING_TITLE", "SUSPECT_NON_CALLOUT",
    ]:
        if itype not in by_type:
            continue
        lines.append("")
        lines.append(f"### {type_labels.get(itype, itype)} ({len(by_type[itype])} occurrences)")
        lines.append("")
        for filepath, line_num, detail in sorted(by_type[itype]):
            lines.append(f"  {filepath}:{line_num}")
            lines.append(f"    {detail}")
        lines.append("")

    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    html_files = find_html_files(ROOT)
    print(f"Scanning {len(html_files)} HTML files...")

    results = []
    for f in html_files:
        results.append(analyze_file(f))

    report = generate_report(results)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"Report saved to: {REPORT_FILE}")
    print()
    print(report)


if __name__ == "__main__":
    main()
