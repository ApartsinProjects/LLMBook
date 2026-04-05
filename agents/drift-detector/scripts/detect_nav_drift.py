#!/usr/bin/env python3
"""Detect navigation link drift: broken prev/next/up, bidirectional mismatches, orphans."""

import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import (
    BOOK_ROOT, DriftReport, read_file, extract_nav_links,
    resolve_href, find_all_html,
)


def main():
    report = DriftReport("NAVIGATION LINKS (prev/next/up)")
    all_html = find_all_html()

    # Build a map: file -> {prev, up, next} resolved paths
    nav_map = {}
    files_with_nav = set()
    files_without_nav = set()

    for fpath in all_html:
        html = read_file(fpath)
        nav = extract_nav_links(html)

        if nav is None:
            # Only flag section files missing nav
            if fpath.name.startswith("section-"):
                files_without_nav.add(fpath)
            continue

        files_with_nav.add(fpath)
        resolved = {}
        for direction, href in nav.items():
            target = resolve_href(fpath, href)
            if target is None:
                continue
            resolved[direction] = target

            # Check target exists
            if not target.exists():
                # Skip template placeholders
                if "{{" in href:
                    continue
                report.error(fpath, f"Broken {direction} link: {href}")

        nav_map[fpath.resolve()] = resolved

    # Check bidirectional consistency
    for fpath_resolved, nav in nav_map.items():
        # If A.next = B, then B.prev should = A
        if "next" in nav:
            next_target = nav["next"].resolve()
            if next_target in nav_map:
                other_nav = nav_map[next_target]
                if "prev" in other_nav:
                    prev_back = other_nav["prev"].resolve()
                    if prev_back != fpath_resolved:
                        report.error(
                            fpath_resolved,
                            f"Bidirectional mismatch: this.next -> {_rel(next_target)}, "
                            f"but that page's prev -> {_rel(prev_back)}",
                            expected=f"prev should point back to {_rel(fpath_resolved)}",
                            actual=f"prev points to {_rel(prev_back)}",
                        )

    # Check for orphaned pages (no incoming next or prev)
    all_targets = set()
    for nav in nav_map.values():
        for direction in ("prev", "next"):
            if direction in nav:
                all_targets.add(nav[direction].resolve())

    for fpath in files_with_nav:
        if fpath.resolve() not in all_targets:
            # First and last pages are expected to have no incoming link
            nav = nav_map.get(fpath.resolve(), {})
            has_prev = "prev" in nav
            has_next = "next" in nav
            # If it has both prev and next but nothing points to it, it's orphaned
            if has_prev and has_next:
                report.warn(fpath, "Orphaned page: has nav links but nothing points to it")

    # Report missing nav
    for fpath in sorted(files_without_nav):
        report.warn(fpath, "No chapter-nav block found")

    report.print_report()


def _rel(p):
    try:
        return str(Path(p).relative_to(BOOK_ROOT))
    except ValueError:
        return str(p)


if __name__ == "__main__":
    main()
