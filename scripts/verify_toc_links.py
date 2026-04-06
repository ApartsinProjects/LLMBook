#!/usr/bin/env python3
"""Verify that every href in toc.html points to a file that exists on disk.

Reports: total links checked, broken links (with line number and href),
and any duplicate hrefs.
"""

import os
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOC_FILE = REPO_ROOT / "toc.html"

HREF_RE = re.compile(r'<a\s[^>]*href="([^"]+)"', re.IGNORECASE)


def main():
    text = TOC_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    all_hrefs: list[tuple[int, str]] = []  # (line_number, href)

    for lineno, line in enumerate(lines, start=1):
        for match in HREF_RE.finditer(line):
            href = match.group(1)
            # Skip fragment-only and javascript: links
            if href.startswith("#") or href.lower().startswith("javascript:"):
                continue
            # Strip any fragment from the path
            path_part = href.split("#")[0]
            if not path_part:
                continue
            all_hrefs.append((lineno, path_part))

    # Check existence
    broken: list[tuple[int, str]] = []
    for lineno, href in all_hrefs:
        resolved = (REPO_ROOT / href).resolve()
        if not resolved.is_file():
            broken.append((lineno, href))

    # Find duplicates
    href_counts = Counter(h for _, h in all_hrefs)
    duplicates = {h: c for h, c in href_counts.items() if c > 1}

    # Report
    print(f"Total links checked: {len(all_hrefs)}")
    print(f"Unique hrefs:        {len(href_counts)}")
    print()

    if broken:
        print(f"BROKEN LINKS ({len(broken)}):")
        for lineno, href in broken:
            print(f"  Line {lineno}: {href}")
    else:
        print("No broken links found.")

    print()
    if duplicates:
        print(f"DUPLICATE HREFS ({len(duplicates)}):")
        for href, count in sorted(duplicates.items()):
            print(f"  {href}  (appears {count}x)")
    else:
        print("No duplicate hrefs.")


if __name__ == "__main__":
    main()
