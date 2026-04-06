"""
HTML Structure Validator for LLMCourse textbook.
Checks all section-*.html and index.html files for structural issues.
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(r"E:\Projects\LLMCourse")

VALID_CALLOUT_TYPES = {
    "big-picture", "key-insight", "note", "warning", "practical-example",
    "fun-note", "research-frontier", "algorithm", "tip", "exercise",
    "pathway", "prerequisites", "objectives", "mental-model",
}


def find_html_files():
    """Find all section-*.html and index.html files under part-*, appendices, front-matter, capstone dirs."""
    files = []
    for root, dirs, fnames in os.walk(BASE_DIR):
        rel = os.path.relpath(root, BASE_DIR).replace("\\", "/")
        # Skip root directory (cover page), styles, images, _lab_fragments, hidden dirs
        if rel == ".":
            continue
        if any(seg.startswith(".") or seg.startswith("_") or seg == "styles" or seg == "images" for seg in rel.split("/")):
            continue
        for f in fnames:
            if f.endswith(".html") and (f.startswith("section-") or f == "index.html"):
                files.append(os.path.join(root, f))
    return sorted(files)


def read_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.readlines()


def check_file(filepath, lines):
    """Run all checks on a single file. Returns list of (category, line_num, issue)."""
    issues = []
    text = "".join(lines)
    rel_path = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")

    # --- 1. Missing <main class="content"> or <div class="content"> wrapper ---
    has_main_content = bool(re.search(r'<main\s[^>]*class="content"', text))
    has_div_content = bool(re.search(r'<div\s+class="content"', text))
    if not has_main_content and not has_div_content:
        issues.append(("missing_content_wrapper", 0, "No <main class=\"content\"> or <div class=\"content\"> wrapper found"))

    # --- 2. Epigraph/prerequisites outside content wrapper ---
    content_open_line = None
    for i, line in enumerate(lines, 1):
        if re.search(r'<main\s[^>]*class="content"', line) or re.search(r'<div\s+class="content"', line):
            content_open_line = i
            break

    if content_open_line is not None:
        for i, line in enumerate(lines, 1):
            if i >= content_open_line:
                break
            if '<blockquote class="epigraph"' in line:
                issues.append(("epigraph_outside_content", i,
                               "Epigraph appears before content wrapper (should be inside)"))
            if 'class="prerequisites"' in line or 'class="prereqs"' in line:
                issues.append(("prerequisites_outside_content", i,
                               "Prerequisites block appears before content wrapper (should be inside)"))

    # --- 3. Missing <header class="chapter-header"> ---
    if '<header class="chapter-header">' not in text:
        issues.append(("missing_chapter_header", 0, 'No <header class="chapter-header"> found'))

    # --- 4. Missing <nav class="header-nav"> ---
    if '<nav class="header-nav">' not in text:
        issues.append(("missing_header_nav", 0, 'No <nav class="header-nav"> found'))

    # --- 5. Missing footer ---
    if "<footer" not in text:
        issues.append(("missing_footer", 0, "No <footer> element found"))

    # --- 6. Missing <nav class="chapter-nav"> ---
    if '<nav class="chapter-nav">' not in text:
        issues.append(("missing_chapter_nav", 0, 'No <nav class="chapter-nav"> found'))

    # --- 7. Unclosed main tags ---
    main_opens = len(re.findall(r"<main[\s>]", text))
    main_closes = text.count("</main>")
    if main_opens != main_closes:
        issues.append(("unclosed_tags", 0,
                        f"Mismatched <main> tags: {main_opens} opens vs {main_closes} closes"))

    # --- 8. Duplicate callout-title divs within a callout block ---
    # Strategy: find callout container divs only (class="callout <type>")
    # and scan the block for callout-title counts
    callout_container_re = re.compile(r'<div\s+class="callout\s+[\w-]+"')
    for i, line in enumerate(lines, 1):
        if callout_container_re.search(line):
            # Scan forward to find end of this callout block (track div nesting)
            nesting = 0
            block_lines = []
            for j in range(i - 1, min(i + 80, len(lines))):
                block_lines.append(lines[j])
                nesting += lines[j].count("<div") - lines[j].count("</div>")
                if nesting <= 0 and j > i - 1:
                    break
            block_text = "".join(block_lines)
            title_count = block_text.count('class="callout-title"')
            if title_count > 1:
                issues.append(("duplicate_callout_title", i,
                               f"Callout has {title_count} callout-title divs (expected 1)"))

    # --- 9. Missing callout type class ---
    for i, line in enumerate(lines, 1):
        # Match exactly class="callout" with no additional classes
        if re.search(r'<div\s+class="callout"', line):
            issues.append(("missing_callout_type", i,
                           'Callout has no type class (just "callout")'))

    # --- 10. Non-standard callout types ---
    for i, line in enumerate(lines, 1):
        m = re.search(r'<div\s+class="callout\s+([\w-]+)"', line)
        if m:
            ctype = m.group(1)
            if ctype not in VALID_CALLOUT_TYPES:
                issues.append(("non_standard_callout_type", i,
                               f'Non-standard callout type: "{ctype}"'))

    # --- 11. Empty <h2> or <h3> tags ---
    for i, line in enumerate(lines, 1):
        if re.search(r"<h2>\s*</h2>", line):
            issues.append(("empty_heading", i, "Empty <h2> tag"))
        if re.search(r"<h3>\s*</h3>", line):
            issues.append(("empty_heading", i, "Empty <h3> tag"))

    # --- 12. Broken relative links ---
    file_dir = os.path.dirname(filepath)
    for i, line in enumerate(lines, 1):
        for href_match in re.finditer(r'href="([^"#]+?)(?:#[^"]*)?(?:")', line):
            href = href_match.group(1)
            if href.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "//")):
                continue
            target = os.path.normpath(os.path.join(file_dir, href))
            if not os.path.exists(target):
                issues.append(("broken_link", i,
                               f'Broken relative link: "{href}" (resolved to: {os.path.relpath(target, BASE_DIR).replace(chr(92), "/")})'))

    # --- 13. <style> blocks ---
    for i, line in enumerate(lines, 1):
        if re.search(r"<style[\s>]", line):
            issues.append(("inline_style_block", i,
                           "File contains a <style> block (should use book.css only)"))

    # --- 14. Missing book.css link ---
    if "book.css" not in text:
        issues.append(("missing_book_css", 0, "No <link> to book.css found"))

    # --- 15. Double </div></div> after callout blocks ---
    # Look for patterns where after a callout's closing </div> there is an extra stray </div>
    # Heuristic: three consecutive </div> on a single line or across two lines near a callout
    for i, line in enumerate(lines, 1):
        if re.search(r"</div>\s*</div>\s*</div>", line):
            context_start = max(0, i - 30)
            context = "".join(lines[context_start:i])
            if 'class="callout' in context:
                issues.append(("double_close_after_callout", i,
                               "Possible triple </div> near callout block (copy-paste error)"))

    return issues


def main():
    html_files = find_html_files()
    print(f"Scanning {len(html_files)} HTML files...\n")

    all_issues = defaultdict(list)
    file_count_with_issues = 0

    for filepath in html_files:
        lines = read_file(filepath)
        file_issues = check_file(filepath, lines)
        if file_issues:
            file_count_with_issues += 1
        rel_path = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")
        for category, line_num, issue in file_issues:
            all_issues[category].append({
                "file": rel_path,
                "line": line_num,
                "issue": issue,
            })

    # Build JSON report
    report = {}
    for cat in sorted(all_issues.keys()):
        report[cat] = all_issues[cat]

    report_path = BASE_DIR / "_validation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary table
    print("=" * 72)
    print("  HTML STRUCTURE VALIDATION REPORT")
    print(f"  Files scanned: {len(html_files)}")
    print(f"  Files with issues: {file_count_with_issues}")
    print("=" * 72)
    print()
    print(f"  {'Category':<40} {'Count':>6}")
    print(f"  {'-'*40} {'-'*6}")

    total = 0
    for cat in sorted(all_issues.keys()):
        count = len(all_issues[cat])
        total += count
        label = cat.replace("_", " ").title()
        print(f"  {label:<40} {count:>6}")

    print(f"  {'-'*40} {'-'*6}")
    print(f"  {'TOTAL':<40} {total:>6}")
    print()
    print(f"  Report saved to: {report_path}")
    print()

    # Print sample issues per category (first 5 each)
    print("=" * 72)
    print("  SAMPLE ISSUES BY CATEGORY (first 5 each)")
    print("=" * 72)
    for cat in sorted(all_issues.keys()):
        label = cat.replace("_", " ").title()
        print(f"\n  [{label}]")
        for entry in all_issues[cat][:5]:
            line_info = f"line {entry['line']}" if entry['line'] > 0 else "file-level"
            print(f"    {entry['file']} ({line_info})")
            print(f"      -> {entry['issue']}")
        remaining = len(all_issues[cat]) - 5
        if remaining > 0:
            print(f"    ... and {remaining} more")


if __name__ == "__main__":
    main()
