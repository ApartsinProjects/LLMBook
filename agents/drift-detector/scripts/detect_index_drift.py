#!/usr/bin/env python3
"""Detect drift between part/chapter index pages and actual section files."""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import (
    BOOK_ROOT, DriftReport, read_file, extract_h1, extract_all_links,
    resolve_href, find_index_files,
)
import glob as globmod


def _section_files_in_dir(directory):
    """Find all section-*.html files in a directory."""
    return sorted(Path(directory).glob("section-*.html"))


def _subdir_indices(directory):
    """Find index.html in immediate subdirectories."""
    results = []
    for d in sorted(Path(directory).iterdir()):
        if d.is_dir() and (d / "index.html").exists():
            results.append(d / "index.html")
    return results


def main():
    report = DriftReport("INDEX PAGES vs ACTUAL SECTIONS")
    index_files = find_index_files()

    for idx_path in index_files:
        idx_path = Path(idx_path)
        idx_html = read_file(idx_path)
        idx_dir = idx_path.parent
        links = extract_all_links(idx_html)

        # Collect internal link targets
        linked_files = set()
        for href, link_text in links:
            if href.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
                continue
            resolved = resolve_href(idx_path, href)
            if resolved is None:
                continue

            linked_files.add(resolved)

            # Check target exists
            if not resolved.exists():
                report.error(idx_path, f"Link target missing: {href}")
                continue

            # Check title match
            if resolved.name.startswith("section-") or resolved.name == "index.html":
                file_html = read_file(resolved)
                h1 = extract_h1(file_html)
                if h1 and link_text:
                    h1_clean = " ".join(h1.split())
                    link_clean = " ".join(link_text.split())
                    h1_core = re.sub(r"^[\d.]+\s*", "", h1_clean).strip()
                    link_core = re.sub(r"^[\d.]+\s*", "", link_clean).strip()
                    # Skip very short link text (nav labels like "Part 1")
                    if len(link_core) > 5 and len(h1_core) > 5:
                        if h1_core.lower() != link_core.lower():
                            report.warn(
                                idx_path,
                                f"Title mismatch for {href}",
                                expected=f"Index: {link_clean}",
                                actual=f"h1: {h1_clean}",
                            )

        # Check for unlisted section files in same directory
        sections_on_disk = _section_files_in_dir(idx_dir)
        for sf in sections_on_disk:
            if sf.resolve() not in linked_files:
                report.warn(
                    idx_path,
                    f"Section not linked from index: {sf.name}",
                )

        # For part indices, check for unlisted module subdirectories
        if "part-" in str(idx_dir.name) or idx_dir.name in ("front-matter", "appendices"):
            sub_indices = _subdir_indices(idx_dir)
            for si in sub_indices:
                if si.resolve() not in linked_files:
                    # Check if any link in the index points into this subdir
                    subdir_name = si.parent.name
                    any_link_to_subdir = any(
                        subdir_name in str(resolve_href(idx_path, h) or "")
                        for h, _ in links
                        if not h.startswith(("http", "mailto", "#"))
                    )
                    if not any_link_to_subdir:
                        report.warn(
                            idx_path,
                            f"Subdirectory not linked: {subdir_name}/",
                        )

    report.print_report()


if __name__ == "__main__":
    main()
