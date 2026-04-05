#!/usr/bin/env python3
"""Detect broken cross-references: internal links to missing files or missing #fragments."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import (
    BOOK_ROOT, DriftReport, read_file, extract_all_links,
    resolve_href, href_fragment, id_exists_in_html, find_all_html,
)


def main():
    report = DriftReport("CROSS-REFERENCES AND HYPERLINKS")
    all_html = find_all_html()

    # Cache file contents for fragment checking
    file_cache = {}

    for fpath in all_html:
        html = read_file(fpath)
        links = extract_all_links(html)

        for href, link_text in links:
            # Skip external links
            if href.startswith(("http://", "https://", "mailto:", "javascript:")):
                continue

            # Check for template placeholders
            if "{{" in href:
                report.warn(fpath, f"Template placeholder in link: {href}")
                continue

            # Pure fragment link (same page)
            if href.startswith("#"):
                frag = href[1:]
                if frag and not id_exists_in_html(html, frag):
                    report.error(fpath, f"Broken same-page fragment: {href}")
                continue

            # Resolve file path
            resolved = resolve_href(fpath, href)
            if resolved is None:
                continue

            if not resolved.exists():
                report.error(fpath, f"Broken file link: {href}")
                continue

            # Check fragment if present
            frag = href_fragment(href)
            if frag:
                resolved_str = str(resolved)
                if resolved_str not in file_cache:
                    file_cache[resolved_str] = read_file(resolved)
                target_html = file_cache[resolved_str]
                if not id_exists_in_html(target_html, frag):
                    report.error(fpath, f"Broken fragment: {href} (#{frag} not found in target)")

    report.print_report()


if __name__ == "__main__":
    main()
