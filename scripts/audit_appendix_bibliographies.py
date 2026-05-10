#!/usr/bin/env python3
"""Audit all appendix section bibliographies.

Scans appendices/appendix-*/section-*.html for bibliography sections,
checks entry counts, hyperlinks, and author/title/year presence.
Saves a report to scripts/appendix_bibliography_report.txt.
"""

import glob
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APPENDICES_DIR = BASE_DIR / "appendices"
REPORT_PATH = BASE_DIR / "scripts" / "appendix_bibliography_report.txt"


def find_section_files():
    """Find all appendix section HTML files."""
    pattern = str(APPENDICES_DIR / "appendix-*" / "section-*.html")
    return sorted(glob.glob(pattern))


def extract_bibliography(html: str):
    """Extract bibliography block from HTML content.

    Looks for <section class="bibliography"> or <div class="bibliography">.
    Returns the matched block text or None.
    """
    # Try <section class="bibliography">
    m = re.search(
        r'<section\s+class="bibliography"[^>]*>.*?</section>',
        html, re.DOTALL | re.IGNORECASE,
    )
    if m:
        return m.group(0)
    # Try <div class="bibliography">
    m = re.search(
        r'<div\s+class="bibliography"[^>]*>.*?</div>\s*(?=<(?:nav|footer|/body|/html|div\s+class="(?:nav|footer)))',
        html, re.DOTALL | re.IGNORECASE,
    )
    if m:
        return m.group(0)
    return None


def count_entries(bib_block: str):
    """Count bibliography entries in a block.

    Looks for bib-entry, bib-entry-card divs, or <li> items.
    """
    card_count = len(re.findall(r'<div\s+class="bib-entry-card"', bib_block, re.IGNORECASE))
    entry_count = len(re.findall(r'<div\s+class="bib-entry"', bib_block, re.IGNORECASE))
    li_count = len(re.findall(r'<li\b', bib_block, re.IGNORECASE))
    # Use whichever pattern yields the most entries
    return max(card_count, entry_count, li_count)


def check_entries(bib_block: str):
    """Check individual entries for links, author, title, year.

    Returns a list of issue strings.
    """
    issues = []

    # Extract each entry card or entry div
    entries = re.findall(
        r'<div\s+class="bib-entry(?:-card)?"[^>]*>(.*?)</div>',
        bib_block, re.DOTALL | re.IGNORECASE,
    )
    # Also check <li> based entries
    li_entries = re.findall(
        r'<li\b[^>]*>(.*?)</li>',
        bib_block, re.DOTALL | re.IGNORECASE,
    )
    all_entries = entries + li_entries

    for i, entry_html in enumerate(all_entries, 1):
        # Check for hyperlink
        has_link = bool(re.search(r'<a\s+href="https?://', entry_html, re.IGNORECASE))
        if not has_link:
            issues.append(f"  Entry {i}: missing hyperlink (no <a href> with URL)")

        # Strip HTML tags for text analysis
        text = re.sub(r'<[^>]+>', ' ', entry_html)
        text = re.sub(r'\s+', ' ', text).strip()

        # Check for year (4-digit number between 1900 and 2099)
        has_year = bool(re.search(r'\b(19|20)\d{2}\b', text))
        if not has_year:
            issues.append(f"  Entry {i}: missing year")

        # Check for quoted or italicized title
        has_title = bool(
            re.search(r'[""\u201c\u201d]', entry_html)  # quoted title
            or re.search(r'<em>', entry_html, re.IGNORECASE)  # italicized title
            or re.search(r'<i>', entry_html, re.IGNORECASE)
        )
        if not has_title:
            issues.append(f"  Entry {i}: missing title markup (no quotes or <em>)")

        # Check for author pattern: looks for "Lastname, F." or similar
        # Relaxed: just check there is some text before the year
        has_author = bool(re.search(r'[A-Z][a-z]+', text))
        if not has_author:
            issues.append(f"  Entry {i}: missing author name")

    return issues


def audit():
    """Run the full audit and return report lines."""
    files = find_section_files()
    lines = []
    lines.append("=" * 72)
    lines.append("APPENDIX BIBLIOGRAPHY AUDIT REPORT")
    lines.append("=" * 72)
    lines.append("")

    with_bib = []
    without_bib = []
    low_count = []
    malformed = {}

    for fpath in files:
        rel = os.path.relpath(fpath, BASE_DIR).replace("\\", "/")
        with open(fpath, encoding="utf-8", errors="replace") as f:
            html = f.read()

        bib_block = extract_bibliography(html)
        if bib_block is None:
            without_bib.append(rel)
        else:
            entry_count = count_entries(bib_block)
            with_bib.append((rel, entry_count))
            if entry_count < 3:
                low_count.append((rel, entry_count))
            entry_issues = check_entries(bib_block)
            if entry_issues:
                malformed[rel] = entry_issues

    # Summary
    lines.append(f"Total appendix sections scanned: {len(files)}")
    lines.append(f"Sections WITH bibliographies:    {len(with_bib)}")
    lines.append(f"Sections WITHOUT bibliographies:  {len(without_bib)}")
    lines.append(f"Sections with < 3 entries:        {len(low_count)}")
    lines.append(f"Sections with malformed entries:  {len(malformed)}")
    lines.append("")

    # Sections with bibliographies
    lines.append("-" * 72)
    lines.append("SECTIONS WITH BIBLIOGRAPHIES")
    lines.append("-" * 72)
    for rel, count in with_bib:
        lines.append(f"  [{count:>2} entries] {rel}")
    lines.append("")

    # Sections without bibliographies
    lines.append("-" * 72)
    lines.append("SECTIONS WITHOUT BIBLIOGRAPHIES (need attention)")
    lines.append("-" * 72)
    if without_bib:
        for rel in without_bib:
            lines.append(f"  {rel}")
    else:
        lines.append("  (none)")
    lines.append("")

    # Low entry count
    lines.append("-" * 72)
    lines.append("SECTIONS WITH FEWER THAN 3 ENTRIES (may need expansion)")
    lines.append("-" * 72)
    if low_count:
        for rel, count in low_count:
            lines.append(f"  [{count} entries] {rel}")
    else:
        lines.append("  (none)")
    lines.append("")

    # Malformed entries
    lines.append("-" * 72)
    lines.append("MALFORMED ENTRIES (missing links, author, title, or year)")
    lines.append("-" * 72)
    if malformed:
        for rel, issues in malformed.items():
            lines.append(f"  {rel}")
            for issue in issues:
                lines.append(f"    {issue}")
            lines.append("")
    else:
        lines.append("  (none)")
    lines.append("")

    lines.append("=" * 72)
    lines.append("END OF REPORT")
    lines.append("=" * 72)

    return lines


def main():
    report_lines = audit()
    report_text = "\n".join(report_lines)

    # Print to stdout
    print(report_text)

    # Save to file
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
