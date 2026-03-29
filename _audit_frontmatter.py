#!/usr/bin/env python3
"""Audit all front-matter HTML files for consistency issues."""
import os
import re
import json

BASE = r"E:\Projects\LLMCourse\front-matter"
issues = {}

def add_issue(filepath, issue):
    rel = os.path.relpath(filepath, r"E:\Projects\LLMCourse")
    issues.setdefault(rel, []).append(issue)

def audit_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    rel = os.path.relpath(filepath, BASE)
    depth = rel.count(os.sep)  # 0 = direct in front-matter/, 1 = in subdirectory

    # Expected CSS prefix
    if depth == 0:
        expected_prefix = "../"
    else:
        expected_prefix = "../../"

    # Check CSS/JS paths
    expected_css = f'{expected_prefix}styles/book.css'
    expected_katex_css = f'{expected_prefix}vendor/katex/katex.min.css'
    expected_prism_css = f'{expected_prefix}vendor/prism/prism-theme.css'

    if expected_css not in content:
        add_issue(filepath, f"Missing or wrong CSS path (expected {expected_css})")
    if expected_katex_css not in content:
        add_issue(filepath, f"Missing or wrong KaTeX CSS path (expected {expected_katex_css})")
    if expected_prism_css not in content:
        add_issue(filepath, f"Missing or wrong Prism CSS path (expected {expected_prism_css})")

    # Check header structure
    if '<header class="chapter-header">' not in content:
        add_issue(filepath, "Missing <header class='chapter-header'>")

    if 'class="book-title-link"' not in content:
        add_issue(filepath, "Missing book-title-link in header nav")

    if 'class="toc-link"' not in content:
        add_issue(filepath, "Missing toc-link in header nav")

    if 'class="header-nav"' not in content:
        add_issue(filepath, "Missing header-nav")

    # Check part-label
    if '<div class="part-label">' not in content and '<div class="part-label"' not in content:
        add_issue(filepath, "Missing part-label div")
    else:
        # Check that part-label contains "Front Matter"
        part_label_match = re.search(r'<div class="part-label">(.*?)</div>', content, re.DOTALL)
        if part_label_match:
            pl_content = part_label_match.group(1)
            if "Front Matter" not in pl_content:
                add_issue(filepath, f"part-label does not contain 'Front Matter': {pl_content.strip()}")
            # Check if it's a link (should be for non-index pages)
            basename = os.path.basename(filepath)
            if basename != "index.html" and "<a " not in pl_content:
                add_issue(filepath, "part-label should be a link to index.html for non-index pages")

    # Check chapter-nav
    if '<nav class="chapter-nav">' not in content:
        add_issue(filepath, "Missing <nav class='chapter-nav'>")
    else:
        # Check for inline styles in nav
        nav_match = re.search(r'<nav class="chapter-nav">(.*?)</nav>', content, re.DOTALL)
        if nav_match:
            nav_content = nav_match.group(1)
            if 'style="' in nav_content:
                add_issue(filepath, f"Inline styles found in chapter-nav")
            if 'class="prev"' not in nav_content:
                add_issue(filepath, "Missing prev class in chapter-nav")
            if 'class="up"' not in nav_content:
                add_issue(filepath, "Missing up class in chapter-nav")
            if 'class="next"' not in nav_content:
                add_issue(filepath, "Missing next class in chapter-nav")

    # Check footer
    if "<footer>" not in content:
        add_issue(filepath, "Missing <footer>")
    else:
        footer_match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)
        if footer_match:
            fc = footer_match.group(1)
            if "Fifth Edition" not in fc:
                add_issue(filepath, f"Footer missing 'Fifth Edition': {fc.strip()[:100]}")
            if "2026" not in fc:
                add_issue(filepath, f"Footer missing '2026': {fc.strip()[:100]}")

    # Stale references
    for i, line in enumerate(lines, 1):
        if "7 parts" in line.lower():
            add_issue(filepath, f"Line {i}: Stale '7 parts' reference (should be 10)")
        if "31 chapters" in line.lower():
            add_issue(filepath, f"Line {i}: Stale '31 chapters' reference (should be 36)")
        if re.search(r'\b28\s+chapters?\b', line, re.IGNORECASE):
            add_issue(filepath, f"Line {i}: Stale '28 chapters' reference")
        if "Fourth Edition" in line:
            add_issue(filepath, f"Line {i}: Stale 'Fourth Edition' (should be Fifth)")
        if "Third Edition" in line:
            add_issue(filepath, f"Line {i}: Stale 'Third Edition' (should be Fifth)")

for root, dirs, files in os.walk(BASE):
    for fn in sorted(files):
        if fn.endswith(".html"):
            audit_file(os.path.join(root, fn))

# Print results
total_issues = sum(len(v) for v in issues.values())
print(f"=== FRONT MATTER AUDIT: {total_issues} issues in {len(issues)} files ===\n")
for filepath in sorted(issues):
    print(f"\n--- {filepath} ---")
    for issue in issues[filepath]:
        print(f"  * {issue}")
