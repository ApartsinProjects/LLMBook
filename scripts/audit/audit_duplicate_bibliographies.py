#!/usr/bin/env python3
"""Audit HTML files for duplicate bibliography sections and other once-per-file blocks.

Scans all .html files under part-*/ and appendices/ (skipping _archive) and reports
any file containing more than one instance of:
  - <section class="bibliography">
  - <div class="whats-next">
  - <div class="callout big-picture">
  - <div class="prerequisites">
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Patterns that should appear at most once per file
ONCE_PATTERNS = {
    "bibliography": re.compile(r'<section\s+class="bibliography">', re.IGNORECASE),
    "whats-next": re.compile(r'<div\s+class="whats-next">', re.IGNORECASE),
    "big-picture": re.compile(r'<div\s+class="callout\s+big-picture">', re.IGNORECASE),
    "prerequisites": re.compile(r'<div\s+class="prerequisites">', re.IGNORECASE),
}

# For bibliography blocks, grab the heading/title that follows
BIB_HEADING_RE = re.compile(
    r'<section\s+class="bibliography">'
    r'(.*?)'
    r'(?:</section>|\Z)',
    re.DOTALL | re.IGNORECASE,
)

BIB_TITLE_RE = re.compile(
    r'<(?:div|h[1-6])\s+class="bibliography-title"[^>]*>(.*?)</(?:div|h[1-6])>',
    re.IGNORECASE,
)


def collect_html_files():
    """Collect all .html files under part-*/ and appendices/, skipping _archive."""
    files = []
    for pattern in ["part-*/**/*.html", "appendices/**/*.html", "front-matter/**/*.html"]:
        for f in BOOK_ROOT.glob(pattern):
            if "_archive" in f.parts:
                continue
            files.append(f)
    return sorted(files)


def find_occurrences(text, pattern):
    """Return list of (line_number, matched_text) for each match."""
    results = []
    for i, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line):
            results.append((i, line.strip()))
    return results


def get_bib_block_info(text, line_num):
    """Get the title/heading of a bibliography block starting near line_num."""
    lines = text.splitlines()
    # Look at the next 10 lines after the match to find the title
    start = line_num - 1  # 0-indexed
    snippet = "\n".join(lines[start:start + 15])
    m = BIB_TITLE_RE.search(snippet)
    if m:
        return m.group(1).strip()
    # Check if it looks like a TODO/placeholder
    snippet_lower = snippet.lower()
    if "todo" in snippet_lower or snippet.count("<p") < 2:
        return "[Placeholder / TODO]"
    return "[No title found]"


def count_bib_entries(text, start_line):
    """Count <p class="bib-ref"> entries in a bibliography block."""
    lines = text.splitlines()
    count = 0
    in_bib = False
    for i in range(start_line - 1, len(lines)):
        line = lines[i]
        if '<section class="bibliography">' in line.lower():
            in_bib = True
            continue
        if in_bib:
            if '</section>' in line:
                break
            if 'bib-ref' in line:
                count += 1
    return count


def audit():
    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files...\n")

    issues = {}  # {pattern_name: [(file, occurrences)]}
    for name in ONCE_PATTERNS:
        issues[name] = []

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        for name, pat in ONCE_PATTERNS.items():
            occs = find_occurrences(text, pat)
            if len(occs) >= 2:
                issues[name].append((f, occs, text))

    total_issues = sum(len(v) for v in issues.values())

    for name, file_list in issues.items():
        if not file_list:
            continue
        print(f"{'=' * 70}")
        print(f"DUPLICATE: {name}  ({len(file_list)} files affected)")
        print(f"{'=' * 70}")
        for f, occs, text in file_list:
            rel = f.relative_to(BOOK_ROOT)
            print(f"\n  File: {rel}")
            print(f"  Count: {len(occs)} occurrences")
            for line_num, line_text in occs:
                print(f"    Line {line_num}: {line_text[:100]}")
                if name == "bibliography":
                    title = get_bib_block_info(text, line_num)
                    entries = count_bib_entries(text, line_num)
                    print(f"      Title: {title}")
                    print(f"      Entries (bib-ref count): {entries}")
        print()

    # Stats summary
    print(f"\n{'=' * 70}")
    print("STATISTICS")
    print(f"{'=' * 70}")
    bib_count = 0
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        bib_count += len(ONCE_PATTERNS["bibliography"].findall(text))
    files_with_bib = sum(
        1 for f in files
        if ONCE_PATTERNS["bibliography"].search(
            f.read_text(encoding="utf-8", errors="replace")
        )
    )
    print(f"  Total HTML files scanned: {len(files)}")
    print(f"  Files with bibliography:  {files_with_bib}")
    print(f"  Total bibliography blocks: {bib_count}")

    if total_issues == 0:
        print("\nNo duplicate blocks found. All files are clean.")
    else:
        print(f"\nSUMMARY: {total_issues} files with duplicate blocks across all patterns.")

    return issues


if __name__ == "__main__":
    audit()
