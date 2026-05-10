#!/usr/bin/env python3
"""Fix broken internal hyperlinks caused by zero-padded section/module numbers.

Scans all HTML files in the book, finds href attributes with zero-padded
references (e.g., section-06.1.html, module-07-*), checks whether the
unpadded version exists on disk, and rewrites the href in-place.

Preserves #fragment anchors and only touches links where the fix target exists.
"""

import glob
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories to scan
GLOB_PATTERNS = [
    "part-*/module-*/section-*.html",
    "part-*/module-*/index.html",
    "part-*/index.html",
    "appendices/appendix-*/section-*.html",
    "appendices/appendix-*/index.html",
    "appendices/index.html",
    "front-matter/*.html",
    "front-matter/pathways/*.html",
    "front-matter/syllabi/*.html",
    "toc.html",
    "index.html",
]

# Regex to match zero-padded section filenames: section-0X.Y.html
# Note: module directories ARE zero-padded on disk, so we only fix section filenames.
# Captures the digit(s) after the leading zero so we can reconstruct without padding.
PADDED_SECTION_RE = re.compile(r"section-0(\d+\.\d+\.html)")


def discover_files():
    """Return sorted list of HTML files to scan."""
    files = set()
    for pattern in GLOB_PATTERNS:
        for match in glob.glob(str(ROOT / pattern)):
            files.add(Path(match).resolve())
    return sorted(files)


def unpad_href(href: str) -> str:
    """Remove zero-padding from section and module references in an href.

    Examples:
        section-06.1.html -> section-6.1.html
        module-07-foo/section-08.3.html -> module-07-foo/section-8.3.html
        section-00.2.html#anchor -> section-0.2.html#anchor
    """
    result = PADDED_SECTION_RE.sub(r"section-\1", href)
    return result


def resolve_href(source_file: Path, href: str) -> Path:
    """Resolve an href relative to the source file, ignoring fragments."""
    path_part = href.split("#")[0] if "#" in href else href
    if not path_part:
        return None
    return (source_file.parent / path_part).resolve()


SKIP_PREFIXES = ("http://", "https://", "mailto:", "javascript:", "#")
HREF_RE = re.compile(r'''(href\s*=\s*["'])([^"']*?)(["'])''', re.IGNORECASE)


def fix_file(filepath: Path) -> tuple[int, list[str]]:
    """Fix zero-padded hrefs in a single file. Returns (count_fixed, details)."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return 0, []

    fixed_count = 0
    details = []

    def replace_href(match):
        nonlocal fixed_count
        prefix = match.group(1)   # href="
        href = match.group(2)     # the URL
        suffix = match.group(3)   # closing quote

        # Skip external links and pure anchors
        if any(href.startswith(p) for p in SKIP_PREFIXES):
            return match.group(0)

        # Check if the current target exists
        target = resolve_href(filepath, href)
        if target is None or target.is_file():
            return match.group(0)

        # Try unpadding
        new_href = unpad_href(href)
        if new_href == href:
            return match.group(0)

        # Check if the unpadded target exists
        new_target = resolve_href(filepath, new_href)
        if new_target is None or not new_target.is_file():
            return match.group(0)

        fixed_count += 1
        rel = filepath.relative_to(ROOT)
        details.append(f"  {rel}: {href} -> {new_href}")
        return f"{prefix}{new_href}{suffix}"

    new_text = HREF_RE.sub(replace_href, text)

    if fixed_count > 0:
        filepath.write_text(new_text, encoding="utf-8")

    return fixed_count, details


def main():
    files = discover_files()
    print(f"Scanning {len(files)} HTML files for broken zero-padded links...\n")

    total_fixed = 0
    files_modified = 0
    all_details = []

    for filepath in files:
        count, details = fix_file(filepath)
        if count > 0:
            files_modified += 1
            total_fixed += count
            all_details.extend(details)

    print(f"Files modified: {files_modified}")
    print(f"Links fixed: {total_fixed}")
    print()

    if all_details:
        print("Details:")
        for d in all_details:
            print(d)
    else:
        print("No broken zero-padded links found.")


if __name__ == "__main__":
    main()
