#!/usr/bin/env python3
"""Detect drift between toc.html and actual files on disk."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import (
    BOOK_ROOT, DriftReport, read_file, extract_h1, extract_all_links,
    resolve_href, find_section_files, find_index_files,
)


def main():
    report = DriftReport("TOC vs ACTUAL FILES")
    toc_path = BOOK_ROOT / "toc.html"

    if not toc_path.exists():
        report.error(toc_path, "toc.html not found")
        report.print_report()
        return

    toc_html = read_file(toc_path)
    links = extract_all_links(toc_html)

    # Track which files the ToC references
    toc_targets = set()

    for href, link_text in links:
        if href.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
            continue

        resolved = resolve_href(toc_path, href)
        if resolved is None:
            continue

        toc_targets.add(resolved)

        # Check file exists
        if not resolved.exists():
            report.error(toc_path, f"Link target missing: {href}", expected="File exists", actual="Not found")
            continue

        # Check title match for section files
        if resolved.name.startswith("section-") or resolved.name == "index.html":
            file_html = read_file(resolved)
            h1 = extract_h1(file_html)
            if h1 and link_text:
                # Normalize whitespace
                h1_clean = " ".join(h1.split())
                link_clean = " ".join(link_text.split())
                # Strip leading section numbers for comparison
                import re
                h1_core = re.sub(r"^\d+[\d.]*\s*", "", h1_clean).strip()
                link_core = re.sub(r"^\d+[\d.]*\s*", "", link_clean).strip()
                if h1_core and link_core and h1_core.lower() != link_core.lower():
                    report.warn(
                        resolved, "Title mismatch with ToC",
                        expected=f"ToC: {link_clean}",
                        actual=f"h1: {h1_clean}",
                    )

    # Check for unlisted section files
    all_sections = find_section_files()
    all_indices = find_index_files()
    all_files = set(Path(f).resolve() for f in all_sections + all_indices)

    for f in all_files:
        if f.resolve() not in toc_targets:
            # Only flag section files, not every index
            if f.name.startswith("section-"):
                rel = f.relative_to(BOOK_ROOT)
                report.warn(f, f"Section file not listed in ToC: {rel}")

    report.print_report()


if __name__ == "__main__":
    main()
