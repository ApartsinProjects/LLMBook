"""
Fix header navigation across the entire book.

Root cause: WAVE 7 agent replaced the working header-nav pattern with
book-title-bar, which is explicitly set to display:none in book.css.
This script standardizes ALL HTML files to use the correct header-nav pattern.

Canonical pattern (inside <header class="chapter-header">):
    <nav class="header-nav">
        <a href="[root]/index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="[root]/toc.html" class="toc-link" title="Table of Contents">
            <span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
"""

import re
import os
import glob
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
BOOK_TITLE = "Building Conversational AI with LLMs and Agents"

# Counters
fixed_title_bar = 0
fixed_missing_nav = 0
fixed_title_text = 0
skipped = 0
total = 0


def get_relative_root(filepath: Path) -> str:
    """Determine the relative path to the book root from a given file."""
    rel = filepath.relative_to(BOOK_ROOT)
    depth = len(rel.parts) - 1  # subtract the filename itself
    if depth == 0:
        return "."
    return "/".join([".."] * depth)


def make_nav_block(root_path: str) -> str:
    """Create the canonical header-nav HTML block."""
    return (
        f'<nav class="header-nav">\n'
        f'        <a href="{root_path}/index.html" class="book-title-link">{BOOK_TITLE}</a>\n'
        f'        <a href="{root_path}/toc.html" class="toc-link" title="Table of Contents">'
        f'<span class="toc-icon">&#9776;</span> Contents</a>\n'
        f'    </nav>'
    )


def fix_file(filepath: Path) -> str:
    """Fix the header in a single HTML file. Returns status string."""
    global fixed_title_bar, fixed_missing_nav, fixed_title_text, skipped, total
    total += 1

    content = filepath.read_text(encoding="utf-8")
    original = content
    root_path = get_relative_root(filepath)
    nav_block = make_nav_block(root_path)

    # Case 1: File has book-title-bar (needs full replacement)
    # Pattern: <div class="book-title-bar">.....</div> possibly followed by newline
    title_bar_pattern = re.compile(
        r'<div class="book-title-bar">.*?</div>\s*',
        re.DOTALL
    )

    if 'book-title-bar' in content:
        # Remove the book-title-bar div
        content = title_bar_pattern.sub('', content)

        # Check if header-nav already exists (shouldn't, but be safe)
        if 'header-nav' not in content:
            # Insert nav block right after <header class="chapter-header">
            content = content.replace(
                '<header class="chapter-header">',
                f'<header class="chapter-header">\n    {nav_block}',
                1
            )
        fixed_title_bar += 1

    # Case 2: File has header-nav but wrong title text
    elif 'header-nav' in content:
        # Fix title text variations
        wrong_titles = [
            "Building Conversational AI using LLM and Agents",
            "Building Conversational AI with LLM and Agents",
            "Building Conversational AI Using LLMs and Agents",
        ]
        changed = False
        for wrong in wrong_titles:
            if wrong in content:
                content = content.replace(wrong, BOOK_TITLE)
                changed = True
        if changed:
            fixed_title_text += 1
        else:
            skipped += 1
            return "ok"

    # Case 3: No header-nav at all (shouldn't happen, but handle)
    elif '<header class="chapter-header">' in content and 'header-nav' not in content:
        content = content.replace(
            '<header class="chapter-header">',
            f'<header class="chapter-header">\n    {nav_block}',
            1
        )
        fixed_missing_nav += 1

    else:
        skipped += 1
        return "skip"

    # Also fix any root path issues in existing nav
    # Some files may have wrong relative paths
    # Fix paths like href="../../index.html" when it should be href="../index.html" etc.
    # This is tricky, so only fix if we're inserting new nav (the make_nav_block handles it)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return "fixed"
    else:
        skipped += 1
        return "ok"


def main():
    global fixed_title_bar, fixed_missing_nav, fixed_title_text, skipped, total

    # Collect all HTML files in parts and appendices
    patterns = [
        "part-*/index.html",
        "part-*/module-*/index.html",
        "part-*/module-*/section-*.html",
        "appendices/appendix-*/index.html",
        "appendices/appendix-*/section-*.html",
        "front-matter/*.html",
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(BOOK_ROOT.glob(pattern))

    all_files = sorted(set(all_files))
    print(f"Scanning {len(all_files)} HTML files...")

    for f in all_files:
        status = fix_file(f)
        if status == "fixed":
            print(f"  FIXED: {f.relative_to(BOOK_ROOT)}")

    print(f"\n=== Summary ===")
    print(f"Total files scanned: {total}")
    print(f"Fixed book-title-bar -> header-nav: {fixed_title_bar}")
    print(f"Fixed missing header-nav: {fixed_missing_nav}")
    print(f"Fixed wrong title text: {fixed_title_text}")
    print(f"Already correct / skipped: {skipped}")

    # Verification pass
    print(f"\n=== Verification ===")
    missing_nav = []
    has_title_bar = []
    for f in all_files:
        content = f.read_text(encoding="utf-8")
        if 'book-title-bar' in content:
            has_title_bar.append(f.relative_to(BOOK_ROOT))
        if '<header class="chapter-header">' in content and 'header-nav' not in content:
            missing_nav.append(f.relative_to(BOOK_ROOT))

    if has_title_bar:
        print(f"WARNING: {len(has_title_bar)} files still have book-title-bar:")
        for f in has_title_bar[:10]:
            print(f"  {f}")
    else:
        print("OK: No files have book-title-bar")

    if missing_nav:
        print(f"WARNING: {len(missing_nav)} files missing header-nav:")
        for f in missing_nav[:10]:
            print(f"  {f}")
    else:
        print("OK: All chapter-header files have header-nav")


if __name__ == "__main__":
    main()
