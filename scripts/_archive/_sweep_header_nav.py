"""
Sweep: Replace standalone book-title-bar with header-nav inside chapter-header.
Also standardizes content order on chapter index pages.

Changes per file:
1. Remove <div class="book-title-bar">...</div>
2. Insert <nav class="header-nav"> as first child of <header class="chapter-header">
3. Compute correct relative path to root index.html based on file depth
"""

import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
BOOK_TITLE = "Building Conversational AI with LLMs and Agents"

# Skip non-book HTML files
SKIP_DIRS = {"agents", "_scripts_archive", "_lab_fragments", "skills-backup-2026-03-27",
             "skills-backup-2026-03-27-v2", "node_modules", ".git", "avatars"}

def get_toc_path(filepath: Path) -> str:
    """Compute relative path from file to root index.html"""
    rel = filepath.relative_to(ROOT).parent
    parts = rel.parts
    if len(parts) == 0:
        return "index.html"
    elif len(parts) == 1:
        return "../index.html"
    elif len(parts) == 2:
        return "../../index.html"
    elif len(parts) == 3:
        return "../../../index.html"
    return "../../index.html"  # fallback

def build_header_nav(toc_path: str) -> str:
    return (
        f'    <nav class="header-nav">\n'
        f'        <a href="{toc_path}" class="book-title-link">{BOOK_TITLE}</a>\n'
        f'        <a href="{toc_path}" class="toc-link" title="Table of Contents">'
        f'<span class="toc-icon">&#9776;</span> Contents</a>\n'
        f'    </nav>\n'
    )

def process_file(filepath: Path) -> bool:
    """Process a single HTML file. Returns True if modified."""
    text = filepath.read_text(encoding="utf-8")
    original = text
    toc_path = get_toc_path(filepath)
    nav_html = build_header_nav(toc_path)

    # Step 1: Remove standalone book-title-bar div (various formats)
    # Pattern: <div class="book-title-bar">...<a ...>...</a>...</div> possibly with newlines
    text = re.sub(
        r'<div\s+class="book-title-bar">\s*\n?\s*<a[^>]*>[^<]*</a>\s*\n?\s*</div>\s*\n?',
        '',
        text,
        flags=re.DOTALL
    )

    # Step 2: Check if header-nav already exists inside chapter-header
    if 'class="header-nav"' in text:
        # Already has header-nav, just ensure book-title-bar was removed
        if text != original:
            filepath.write_text(text, encoding="utf-8")
            return True
        return False

    # Step 3: Insert header-nav as first child of <header class="chapter-header">
    # Match the opening tag and insert nav right after
    pattern = r'(<header\s+class="chapter-header">\s*\n)'
    match = re.search(pattern, text)
    if match:
        insert_pos = match.end()
        text = text[:insert_pos] + nav_html + text[insert_pos:]
    else:
        # Try without newline
        pattern2 = r'(<header\s+class="chapter-header">)'
        match2 = re.search(pattern2, text)
        if match2:
            insert_pos = match2.end()
            text = text[:insert_pos] + '\n' + nav_html + text[insert_pos:]

    if text != original:
        filepath.write_text(text, encoding="utf-8")
        return True
    return False

def main():
    html_files = []
    for f in ROOT.rglob("*.html"):
        # Skip non-book directories
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        html_files.append(f)

    modified = 0
    skipped = 0
    errors = []

    for f in sorted(html_files):
        try:
            if process_file(f):
                modified += 1
                print(f"  MODIFIED: {f.relative_to(ROOT)}")
            else:
                skipped += 1
        except Exception as e:
            errors.append((f, str(e)))
            print(f"  ERROR: {f.relative_to(ROOT)}: {e}")

    print(f"\n=== Summary ===")
    print(f"Total files scanned: {len(html_files)}")
    print(f"Modified: {modified}")
    print(f"Skipped (no change needed): {skipped}")
    print(f"Errors: {len(errors)}")
    for f, e in errors:
        print(f"  {f.relative_to(ROOT)}: {e}")

if __name__ == "__main__":
    main()
